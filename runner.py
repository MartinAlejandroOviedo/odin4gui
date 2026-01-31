# runner.py
import subprocess
import sys
from pathlib import Path
from constants import ERROR_PREFIX

# --- LÓGICA PARA SUPORTAR PYINSTALLER ---
def get_odin_path():
    """Determina o caminho do binário odin4 em /bin, seja em desenvolvimento ou após o empacotamento."""
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_dir = Path(sys._MEIPASS)
    else:
        base_dir = Path(__file__).resolve().parent
    return str(base_dir / "bin" / "odin4")

ODIN_BIN_PATH = get_odin_path()
# --- FIM DA LÓGICA PYINSTALLER ---


def build_flash_command(firmware_set: dict, options: dict) -> list:
    """
    Monta a lista de comandos completa para o subprocesso 'odin4'.
    Usa o caminho correto do binário (ODIN_BIN_PATH) e mapeia os argumentos.
    """
    # Atenção: O comando não inclui 'sudo' aqui. Assume-se que o usuário 
    # executará o binário final (dist/odin4gui) com 'sudo'.
    cmd = [ODIN_BIN_PATH] 
    
    # 1. Adicionar Arquivos (-b, -a, -c, -s)
    if firmware_set.get('BL'): cmd += ["-b", firmware_set['BL']]
    if firmware_set.get('AP'): cmd += ["-a", firmware_set['AP']]
    if firmware_set.get('CP'): cmd += ["-c", firmware_set['CP']]
    if firmware_set.get('CSC'): cmd += ["-s", firmware_set['CSC']]
    # O UMS (-u) pode ser adicionado aqui se for usado na UI
    
    # 2. Adicionar Opções (-e, -V, --reboot, --redownload)
    if options.get('nand_erase'): cmd += ["-e"]
    if options.get('home_validation'): cmd += ["-V"]
    if options.get('reboot'): cmd += ["--reboot"]
    
    # 3. Adicionar Dispositivo (-d)
    if options.get('device_path'): cmd += ["-d", options['device_path']]
    
    return cmd

def run_device_list_command() -> list:
    """Executa 'odin4 -l' e retorna a lista de paths de dispositivos detectados."""
    try:
        # Comando para listar dispositivos
        cmd = [ODIN_BIN_PATH, "-l"] # Usa o caminho correto do binário
        
        # Rodar o comando e capturar a saída
        # A flag 'check=True' lança exceção se o código de retorno não for 0
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=10)
        
        # Divide a saída em linhas, removendo linhas vazias
        devices = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        return devices
        
    except FileNotFoundError:
        return [f"{ERROR_PREFIX}: Binario odin4 no encontrado."]
    except subprocess.CalledProcessError as e:
        # O odin4 pode retornar um código de erro se nenhum dispositivo for encontrado
        # Captura o stderr para log
        return [f"{ERROR_PREFIX} al listar (Código {e.returncode}): {e.stderr.strip() or 'Verifique permisos udev.'}"]
    except subprocess.TimeoutExpired:
        return [f"{ERROR_PREFIX}: La búsqueda de dispositivos expiró (timeout)."]
    except Exception as e:
        return [f"{ERROR_PREFIX} inesperado: {type(e).__name__}: {str(e)}"]
