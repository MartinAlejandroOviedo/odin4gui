# flash_thread.py
from PySide6.QtCore import QThread, Signal
import subprocess
# REMOVER: from runner import start_flash_process
from parser import parse_odin_output


class FlashService:
    """Wrapper para execução do odin4 em subprocesso."""

    def __init__(self, cmd_list: list):
        self.cmd = cmd_list
        self.process = None

    def start(self):
        self.process = subprocess.Popen(
            self.cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        return self.process

    def stop(self):
        if self.process is not None and self.process.poll() is None:
            try:
                self.process.terminate()
                self.process.wait(timeout=3)
            except Exception:
                try:
                    self.process.kill()
                except Exception:
                    pass

class FlashThread(QThread):
    # Sinais para comunicar com a UI
    log_output = Signal(dict) # Envia o dicionário parsed_data
    flash_finished = Signal(str) # Envia 'PASS' ou 'FAIL'
    
    def __init__(self, cmd_list: list):
        super().__init__()
        self.cmd = cmd_list # A thread agora guarda o comando completo
        self.service = FlashService(cmd_list)
        self._stop_requested = False
        
    def run(self):
        print(f"Executando: {' '.join(self.cmd)}")
        try:
            # Unifica stderr em stdout para evitar deadlocks por leitura bloqueante.
            self.process = self.service.start()
        except FileNotFoundError:
            self.log_output.emit(parse_odin_output("ERROR: Binario odin4 no encontrado en el PATH o en el paquete."))
            self.flash_finished.emit("FAIL")
            return
        except Exception as e:
            self.log_output.emit(parse_odin_output(f"ERROR al iniciar el subproceso: {str(e)}"))
            self.flash_finished.emit("FAIL")
            return
            
        # Monitoramento do processo (código restante do run() é o mesmo)
        # Lê linha a linha até o processo encerrar e o pipe fechar.
        if self.process.stdout is not None:
            for line in iter(self.process.stdout.readline, ''):
                if not line:
                    break
                parsed = parse_odin_output(line.strip())
                self.log_output.emit(parsed)

        return_code = self.process.wait()
        if self._stop_requested:
            self.flash_finished.emit("CANCELLED")
        elif return_code == 0:
            self.flash_finished.emit("PASS")
        else:
            self.flash_finished.emit("FAIL")

    def stop(self):
        """Solicita o encerramento do processo."""
        self._stop_requested = True
        self.service.stop()
