# gui_ui.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QTextEdit, QLineEdit, QCheckBox, QLabel, QGroupBox, 
    QComboBox, QFileDialog
)
from PySide6.QtCore import Qt

class OdinMainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Odin4 Linux GUI - Flashing Tool")
        self.setGeometry(100, 100, 800, 600)
        self.layout = QVBoxLayout(self)
        
        # --- Painel de Arquivos (BL, AP, CP, CSC) ---
        file_group = QGroupBox("Arquivos de Firmware (.tar / .tar.md5)")
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
            line_edit.setPlaceholderText(f"Selecione o arquivo {label}...")
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
        options_group = QGroupBox("Opções")
        options_layout = QVBoxLayout()
        self.nand_erase_checkbox = QCheckBox("NAND Erase (Full Wipe)")
        self.home_validation_checkbox = QCheckBox("Home Binary Validation (-V)")
        self.reboot_checkbox = QCheckBox("Auto Reboot")
        
        options_layout.addWidget(self.nand_erase_checkbox)
        options_layout.addWidget(self.home_validation_checkbox)
        options_layout.addWidget(self.reboot_checkbox)
        options_group.setLayout(options_layout)
        control_layout.addWidget(options_group)
        
        # Dispositivos
        device_group = QGroupBox("Dispositivo")
        device_layout = QVBoxLayout()
        self.device_combo = QComboBox()
        self.device_combo.addItem("Detectando dispositivos...")
        self.device_combo.setEnabled(False)
        self.refresh_btn = QPushButton("Atualizar Lista")
        
        device_layout.addWidget(self.device_combo)
        device_layout.addWidget(self.refresh_btn)
        device_group.setLayout(device_layout)
        control_layout.addWidget(device_group)
        
        self.layout.addLayout(control_layout)

        # --- Botão Iniciar Flash ---
        self.start_btn = QPushButton("INICIAR FLASH")
        self.start_btn.setStyleSheet("font-size: 18pt; padding: 10px; background-color: #4CAF50; color: white;")
        self.layout.addWidget(self.start_btn)
        
        # --- Painel de Logs ---
        log_group = QGroupBox("Logs / Saída do Odin4")
        log_layout = QVBoxLayout()
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)
        log_group.setLayout(log_layout)
        self.layout.addWidget(log_group)
        
        self.status_label = QLabel("Status: Pronto.")
        self.layout.addWidget(self.status_label)

    # Função placeholder para seleção de arquivos
    def select_file(self, part_key):
        file_path, _ = QFileDialog.getOpenFileName(self, f"Selecionar Arquivo {part_key}", 
                                                   "", "Firmware Files (*.tar *.tar.md5);;All Files (*)")
        if file_path:
            self.file_fields[part_key].setText(file_path)
            