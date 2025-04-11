import os
import sys
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QApplication
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt
from tela_ativar_sistema import TelaAtivarSistema  # substitua pelo descricao correto se for diferente

import os
import shutil
from datetime import datetime

# 🔁 BACKUP AUTOMÁTICO AO INICIAR
def criar_backup_automatico():
    if not os.path.exists("backup"):
        os.makedirs("backup")
    if os.path.exists("sistema.db"):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        destino = f"backup/auto_backup_{timestamp}.db"
        try:
            shutil.copy2("sistema.db", destino)
            print(f"[Backup automático criado] {destino}")
        except Exception as e:
            print(f"Erro no backup automático: {e}")

# Executa o backup assim que o splash inicia
criar_backup_automatico()




def resource_path(rel_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, rel_path)

class SplashVisual(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SYSON PDV PRÓ - Splash")
        self.setFixedSize(600, 400)
        self.setStyleSheet("background-color: black;")

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Caminho da imagem
        imagem_path = resource_path("imagens/imgChatGPT.png")

        # Imagem ou erro
        self.label_imagem = QLabel()
        self.label_imagem.setAlignment(Qt.AlignCenter)
        if os.path.exists(imagem_path):
            pixmap = QPixmap(imagem_path)
            self.label_imagem.setPixmap(pixmap.scaledToWidth(300, Qt.SmoothTransformation))
        else:
            self.label_imagem.setText("Imagem não encontrada.")
            self.label_imagem.setStyleSheet("color: red; font-size: 16px;")

        # Título
        self.titulo = QLabel("SYSON PDV PRÓ")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setFont(QFont("Arial", 22, QFont.Bold))
        self.titulo.setStyleSheet("color: cyan;")

        # Subtítulo
        self.subtitulo = QLabel("Tecnologia além dos limites.")
        self.subtitulo.setAlignment(Qt.AlignCenter)
        self.subtitulo.setFont(QFont("Arial", 14))
        self.subtitulo.setStyleSheet("color: lightgray;")

        # Botão Entrar
        self.botao = QPushButton("Entrar no Sistema")
        self.botao.setCursor(Qt.PointingHandCursor)
        self.botao.setFixedWidth(180)
        self.botao.setFont(QFont("Arial", 10))
        self.botao.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                border: 2px solid turquoise;
                border-radius: 10px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: turquoise;
                color: black;
            }
        """)
        self.botao.clicked.connect(self.abrir_ativacao)

        # Adiciona ao layout
        layout.addStretch()
        layout.addWidget(self.label_imagem)
        layout.addSpacing(10)
        layout.addWidget(self.titulo)
        layout.addWidget(self.subtitulo)
        layout.addSpacing(15)
        layout.addWidget(self.botao, alignment=Qt.AlignCenter)
        layout.addStretch()

        self.setLayout(layout)

    def abrir_ativacao(self):
        self.accept()  # Fecha o splash
        ativar = TelaAtivarSistema()
        ativar.exec_()

# Se quiser testar sozinho:
if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash = SplashVisual()
    splash.setWindowIcon(QIcon(resource_path("imagens/favicon.ico")))
    if splash.exec_() == QDialog.Accepted:
        sys.exit(app.exec_())
