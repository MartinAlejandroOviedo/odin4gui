# main.py
import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from constants import (
    UI_TEXT,
    NO_DEVICE_TEXT,
    DETECTING_DEVICES_TEXT,
    ERROR_PREFIX,
    is_valid_firmware_path,
)
from gui_ui import OdinMainWindow
from flash_thread import FlashThread
from device_scanner import DeviceScannerThread
from parser import format_log
from runner import build_flash_command

class MainApp(OdinMainWindow):
    def __init__(self):
        super().__init__()
        
        # Conexões de Slots
        self.start_btn.clicked.connect(self.start_flash)
        self.stop_btn.clicked.connect(self.stop_flash)
        self.refresh_btn.clicked.connect(self.scan_devices)
        
        # Variáveis de Thread
        self.flash_thread = None
        self.scanner_thread = None
        
        # Inicia a busca de dispositivos ao carregar
        self.scan_devices()

    def set_controls_enabled(self, enabled: bool):
        """Habilita/desabilita controles enquanto o flash está em andamento."""
        for line_edit in self.file_fields.values():
            line_edit.setEnabled(enabled)
        self.nand_erase_checkbox.setEnabled(enabled)
        self.home_validation_checkbox.setEnabled(enabled)
        self.reboot_checkbox.setEnabled(enabled)
        self.device_combo.setEnabled(enabled)
        self.refresh_btn.setEnabled(enabled)

    def scan_devices(self):
        """Inicia a thread para listar dispositivos."""
        self.device_combo.clear()
        self.device_combo.addItem(DETECTING_DEVICES_TEXT)
        self.device_combo.setEnabled(False)
        self.status_label.setText(UI_TEXT["status_scanning"])
        
        self.scanner_thread = DeviceScannerThread()
        self.scanner_thread.device_list_found.connect(self.update_device_list)
        self.scanner_thread.start()

    def update_device_list(self, devices: list):
        """Atualiza o ComboBox com a lista de dispositivos encontrados."""
        self.device_combo.clear()
        if devices and not devices[0].startswith(ERROR_PREFIX):
            self.device_combo.addItems(devices)
            self.device_combo.setEnabled(True)
            self.status_label.setText(UI_TEXT["status_detected"].format(count=len(devices)))
        else:
            self.device_combo.addItem(NO_DEVICE_TEXT)
            self.device_combo.setEnabled(False)
            self.status_label.setText(UI_TEXT["status_detection_error"])

    def start_flash(self):
        """Inicia o processo de flash na thread."""
        self.log_text.clear()
        
        # 1. Coletar dados da UI
        firmware_set = {k: v.text() for k, v in self.file_fields.items() if v.text()}
        options = {
            'nand_erase': self.nand_erase_checkbox.isChecked(),
            'home_validation': self.home_validation_checkbox.isChecked(),
            'reboot': self.reboot_checkbox.isChecked(),
            'device_path': self.device_combo.currentText() if self.device_combo.isEnabled() and self.device_combo.currentText() != NO_DEVICE_TEXT else None,
        }
        
        if not firmware_set:
            QMessageBox.warning(self, UI_TEXT["warn_missing_firmware_title"], UI_TEXT["warn_missing_firmware_body"])
            return
        
        for path in firmware_set.values():
            if not is_valid_firmware_path(path):
                QMessageBox.warning(
                    self,
                    UI_TEXT["warn_invalid_firmware_title"],
                    UI_TEXT["warn_invalid_firmware_body"].format(path=path),
                )
                return

        # 2. Montar o comando
        try:
            cmd = build_flash_command(firmware_set, options)
        except Exception as e:
            self.log_text.append(f"Error al construir el comando: {str(e)}")
            return
            
        # 3. Iniciar a Thread
        self.status_label.setText(UI_TEXT["status_starting"])
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.set_controls_enabled(False)
        
        self.flash_thread = FlashThread(cmd)
        self.flash_thread.log_output.connect(self.update_log)
        self.flash_thread.flash_finished.connect(self.flash_finished)
        self.flash_thread.start()

    def update_log(self, parsed_data: dict):
        """Recebe o output processado da thread e atualiza a UI."""
        log_line = format_log(parsed_data)
        self.log_text.append(log_line)
        # Se você tiver uma barra de progresso, atualize-a aqui usando parsed_data['percentage']

    def flash_finished(self, status: str):
        """Processa o resultado final do flash."""
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.set_controls_enabled(True)
        if status == "PASS":
            self.status_label.setText(UI_TEXT["status_success"])
            QMessageBox.information(self, UI_TEXT["info_success_title"], UI_TEXT["info_success_body"])
        elif status == "CANCELLED":
            self.status_label.setText(UI_TEXT["status_cancelled"])
            QMessageBox.information(self, UI_TEXT["info_cancelled_title"], UI_TEXT["info_cancelled_body"])
        else:
            self.status_label.setText(UI_TEXT["status_fail"].format(status=status))
            QMessageBox.critical(self, UI_TEXT["error_fail_title"], UI_TEXT["error_fail_body"])
        
        # Reinicia a busca de dispositivos para o estado normal
        self.scan_devices()

    def stop_flash(self):
        """Solicita o cancelamento do flash."""
        if self.flash_thread is not None:
            self.status_label.setText(UI_TEXT["status_canceling"])
            self.stop_btn.setEnabled(False)
            self.flash_thread.stop()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
    
