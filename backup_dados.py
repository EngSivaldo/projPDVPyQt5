# backup_dados.py
import os
import shutil
import sqlite3
from datetime import datetime
from PyQt5.QtWidgets import (
    QDialog, QTabWidget, QVBoxLayout, QWidget, QLabel, QPushButton,
    QFileDialog, QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class BackupWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Backup de Dados")
        self.setFixedSize(600, 400)
        self.setStyleSheet("background-color: #0077b6; color: white; font-family: Arial;")

        layout = QVBoxLayout()
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("QTabBar::tab { height: 30px; width: 150px; font-weight: bold; }")

        self.tabs.addTab(self.criar_backup_tab(), "Criar Backup")
        self.tabs.addTab(self.restaurar_backup_tab(), "Restaurar Backup")

        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def criar_backup_tab(self):
        aba = QWidget()
        layout = QVBoxLayout()

        imagem = QLabel()
        imagem.setPixmap(QPixmap("imagens/backup.png").scaledToHeight(150, Qt.SmoothTransformation))
        imagem.setAlignment(Qt.AlignCenter)

        btn_backup = QPushButton("Criar Backup Agora")
        btn_backup.setStyleSheet("padding: 10px; font-size: 14px;")
        btn_backup.clicked.connect(self.criar_backup)

        layout.addWidget(imagem)
        layout.addWidget(btn_backup)
        layout.addStretch()
        aba.setLayout(layout)
        return aba

    def restaurar_backup_tab(self):
        aba = QWidget()
        layout = QVBoxLayout()

        info = QLabel("Selecione um arquivo de backup para restaurar.\nO sistema será reiniciado após a restauração.")
        info.setAlignment(Qt.AlignCenter)

        btn_restore = QPushButton("Selecionar e Restaurar")
        btn_restore.setStyleSheet("padding: 10px; font-size: 14px;")
        btn_restore.clicked.connect(self.restaurar_backup)

        layout.addStretch()
        layout.addWidget(info)
        layout.addWidget(btn_restore)
        layout.addStretch()
        aba.setLayout(layout)
        return aba

    def criar_backup(self):
        if not os.path.exists("backup"):
            os.makedirs("backup")
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        origem = "sistema.db"
        destino = f"backup/backup_{timestamp}.db"
        try:
            shutil.copy2(origem, destino)
            QMessageBox.information(self, "Backup", f"Backup criado com sucesso:\n{destino}")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao criar backup:\n{str(e)}")

    def restaurar_backup(self):
        caminho, _ = QFileDialog.getOpenFileName(self, "Selecione um arquivo de backup", "backup/", "Arquivos DB (*.db)")
        if caminho:
            resposta = QMessageBox.question(self, "Restaurar Backup", "Tem certeza que deseja restaurar este backup?\nIsso substituirá os dados atuais.")
            if resposta == QMessageBox.Yes:
                try:
                    shutil.copy2(caminho, "sistema.db")
                    QMessageBox.information(self, "Restaurado", "Backup restaurado com sucesso.\nReinicie o sistema.")
                    self.close()
                except Exception as e:
                    QMessageBox.critical(self, "Erro", f"Erro ao restaurar backup:\n{str(e)}")
