# device_scanner.py
from PySide6.QtCore import QThread, Signal
from runner import run_device_list_command

class DeviceScannerThread(QThread):
    # Sinal para enviar a lista de dispositivos de volta para a UI
    device_list_found = Signal(list)
    
    def run(self):
        # Chama a função que executa 'odin4 -l'
        devices = run_device_list_command()
        self.device_list_found.emit(devices)
        