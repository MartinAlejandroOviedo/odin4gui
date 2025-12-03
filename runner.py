# runner.py
import subprocess
import os
import sys

# --- LÓGICA PARA SUPORTAR PYINSTALLER ---
def get_odin_path():
    """Determina o caminho do binário odin4, seja em desenvolvimento ou após o empacotamento."""
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # Estamos rodando como um binário PyInstaller.
        # O odin4 foi adicionado ao bundle e está no diretório temporário _MEIPASS.
        return os.path.join(sys._MEIPASS, "odin4")
    else:
        # Estamos rodando em ambiente de desenvolvimento (diretório atual).
        return "odin4"

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
        return ["ERRO: Binário odin4 não encontrado."]
    except subprocess.CalledProcessError as e:
        # O odin4 pode retornar um código de erro se nenhum dispositivo for encontrado
        # Captura o stderr para log
        return [f"ERRO ao listar (Código {e.returncode}): {e.stderr.strip() or 'Verifique permissões udev.'}"]
    except subprocess.TimeoutExpired:
        return ["ERRO: A varredura de dispositivos expirou (timeout)."]
    except Exception as e:
        return [f"ERRO inesperado: {type(e).__name__}: {str(e)}"]
