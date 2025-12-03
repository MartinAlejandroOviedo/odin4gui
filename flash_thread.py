# flash_thread.py
from PySide6.QtCore import QThread, Signal
import subprocess
# REMOVER: from runner import start_flash_process
from parser import parse_odin_output

class FlashThread(QThread):
    # Sinais para comunicar com a UI
    log_output = Signal(dict) # Envia o dicionário parsed_data
    flash_finished = Signal(str) # Envia 'PASS' ou 'FAIL'
    
    def __init__(self, cmd_list: list):
        super().__init__()
        self.cmd = cmd_list # A thread agora guarda o comando completo
        
    def run(self):
        print(f"Executando: {' '.join(self.cmd)}")
        try:
            # Novo bloco: Inicia o processo de forma não-bloqueante aqui mesmo!
            process = subprocess.Popen(
                self.cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        except FileNotFoundError:
            self.log_output.emit(parse_odin_output("ERRO: Binário odin4 não encontrado no PATH ou no pacote."))
            self.flash_finished.emit("FAIL")
            return
        except Exception as e:
            self.log_output.emit(parse_odin_output(f"ERRO ao iniciar subprocesso: {str(e)}"))
            self.flash_finished.emit("FAIL")
            return
            
        # Monitoramento do processo (código restante do run() é o mesmo)
        while True:
            # Captura STDOUT e STDERR
            output = process.stdout.readline()
            error_output = process.stderr.readline()
            # ... (código de log e verificação de fim de processo) ...
            
            if output:
                parsed = parse_odin_output(output.strip())
                self.log_output.emit(parsed) 
                
            if error_output:
                parsed = parse_odin_output(f"[STDERR] {error_output.strip()}")
                self.log_output.emit(parsed)
                
            if process.poll() is not None:
                if process.returncode == 0:
                    self.flash_finished.emit("PASS")
                else:
                    self.flash_finished.emit("FAIL")
                break
