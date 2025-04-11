import os
import shutil
from datetime import datetime
from PyQt5.QtWidgets import (
    QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QTabWidget, QWidget, QProgressBar, QCheckBox, QTextEdit
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
import subprocess

class TelaBackup(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Backup de dados")
        self.setFixedSize(700, 530)
        self.setStyleSheet("background-color: #0a5e89; color: white; font-family: Arial;")

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("QTabBar::tab:selected { background-color: #ff6600; font-weight: bold; }")
        self.tab_criar = QWidget()
        self.tab_restaurar = QWidget()
        self.tab_baixar = QWidget()

        self.tabs.addTab(self.tab_criar, "Criar Backup")
        self.tabs.addTab(self.tab_restaurar, "Restaurar Backup")
        self.tabs.addTab(self.tab_baixar, "Baixar Backup")
        self.tabs.setTabEnabled(2, False)

        self.layout_principal = QVBoxLayout(self)

        self.banner = QLabel()
        self.banner.setPixmap(QPixmap("imagens/backup_banner.png").scaled(700, 150, Qt.KeepAspectRatio))
        self.layout_principal.addWidget(self.banner)
        self.layout_principal.addWidget(self.tabs)

        self.setup_tab_criar()

    def setup_tab_criar(self):
        layout = QVBoxLayout()

        icone = QLabel()
        icone.setPixmap(QPixmap("imagens/icon_hd.png").scaled(80, 80, Qt.KeepAspectRatio))
        layout.addWidget(icone, alignment=Qt.AlignLeft)

        self.botao_criar = QPushButton("Criar Backup")
        self.botao_criar.clicked.connect(self.criar_backup)
        layout.addWidget(self.botao_criar, alignment=Qt.AlignLeft)

        self.progress = QProgressBar()
        self.progress.setValue(0)
        layout.addWidget(self.progress)

        check_layout = QHBoxLayout()
        self.checkbox_diario = QCheckBox("BACKUP DIÁRIO ATIVADO")
        self.checkbox_diario.setChecked(True)
        check_layout.addWidget(self.checkbox_diario)

        self.botao_abrir = QPushButton("Abrir Pasta Backup")
        self.botao_abrir.clicked.connect(self.abrir_pasta_backup)
        check_layout.addWidget(self.botao_abrir)
        layout.addLayout(check_layout)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        layout.addWidget(self.log)

        self.tab_criar.setLayout(layout)

    def criar_backup(self):
        try:
            origem = "dados.db"
            if not os.path.exists("backup"):
                os.makedirs("backup")

            data_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            destino = os.path.join("backup", f"backup_{data_hora}.db")
            shutil.copy2(origem, destino)

            self.progress.setValue(100)
            self.log.append(f"Backup criado com sucesso: {destino}")
        except Exception as e:
            self.log.append(f"Erro ao criar backup: {e}")

    def abrir_pasta_backup(self):
        pasta = os.path.abspath("backup")
        if os.name == 'nt':
            os.startfile(pasta)
        elif os.name == 'posix':
            subprocess.call(['xdg-open', pasta])
