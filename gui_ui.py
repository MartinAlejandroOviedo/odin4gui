# gui_ui.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QTextEdit, QLineEdit, QCheckBox, QLabel, QGroupBox, 
    QComboBox, QFileDialog
)
from PySide6.QtCore import Qt
from constants import UI_TEXT, DETECTING_DEVICES_TEXT

class OdinMainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(UI_TEXT["window_title"])
        self.setGeometry(100, 100, 800, 600)
        self.layout = QVBoxLayout(self)
        
        # --- Painel de Arquivos (BL, AP, CP, CSC) ---
        file_group = QGroupBox(UI_TEXT["firmware_group"])
        file_layout = QVBoxLayout()

        self.file_fields = {
            "BL": QLineEdit(),
            "AP": QLineEdit(),
            "CP": QLineEdit(),
            "CSC": QLineEdit(),
        }
        
        for label, line_edit in self.file_fields.items():
            h_layout = QHBoxLayout()
            h_layout.addWidget(QLabel(f"{label}:"))
            line_edit.setPlaceholderText(f"Seleccione el archivo {label}...")
            h_layout.addWidget(line_edit)
            
            btn = QPushButton("...")
            btn.setFixedWidth(40)
            # Conecta o botão a uma função genérica para selecionar arquivos
            btn.clicked.connect(lambda checked, l=label: self.select_file(l))
            h_layout.addWidget(btn)
            file_layout.addLayout(h_layout)

        file_group.setLayout(file_layout)
        self.layout.addWidget(file_group)

        # --- Painel de Opções e Dispositivos ---
        control_layout = QHBoxLayout()
        
        # Opções
        options_group = QGroupBox(UI_TEXT["options_group"])
        options_layout = QVBoxLayout()
        self.nand_erase_checkbox = QCheckBox("Borrado NAND (Borrado completo)")
        self.home_validation_checkbox = QCheckBox("Validación binaria Home (-V)")
        self.reboot_checkbox = QCheckBox("Reinicio automático")
        
        options_layout.addWidget(self.nand_erase_checkbox)
        options_layout.addWidget(self.home_validation_checkbox)
        options_layout.addWidget(self.reboot_checkbox)
        options_group.setLayout(options_layout)
        control_layout.addWidget(options_group)
        
        # Dispositivos
        device_group = QGroupBox(UI_TEXT["device_group"])
        device_layout = QVBoxLayout()
        self.device_combo = QComboBox()
        self.device_combo.addItem(DETECTING_DEVICES_TEXT)
        self.device_combo.setEnabled(False)
        self.refresh_btn = QPushButton(UI_TEXT["refresh_devices"])
        
        device_layout.addWidget(self.device_combo)
        device_layout.addWidget(self.refresh_btn)
        device_group.setLayout(device_layout)
        control_layout.addWidget(device_group)
        
        self.layout.addLayout(control_layout)

        # --- Botões de Controle ---
        control_buttons = QHBoxLayout()
        self.start_btn = QPushButton(UI_TEXT["start_flash"])
        self.start_btn.setStyleSheet("font-size: 18pt; padding: 10px; background-color: #4CAF50; color: white;")
        self.stop_btn = QPushButton(UI_TEXT["stop_flash"])
        self.stop_btn.setStyleSheet("font-size: 18pt; padding: 10px; background-color: #E53935; color: white;")
        self.stop_btn.setEnabled(False)
        control_buttons.addWidget(self.start_btn)
        control_buttons.addWidget(self.stop_btn)
        self.layout.addLayout(control_buttons)
        
        # --- Painel de Logs ---
        log_group = QGroupBox(UI_TEXT["logs_group"])
        log_layout = QVBoxLayout()
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)
        log_group.setLayout(log_layout)
        self.layout.addWidget(log_group)
        
        self.status_label = QLabel(UI_TEXT["status_ready"])
        self.layout.addWidget(self.status_label)

    # Função placeholder para seleção de arquivos
    def select_file(self, part_key):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            UI_TEXT["select_file_title"].format(part_key=part_key),
            "",
            UI_TEXT["select_file_filter"],
        )
        if file_path:
            self.file_fields[part_key].setText(file_path)
            
