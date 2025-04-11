# splash_window.py
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QPixmap, QFont, QPalette, QLinearGradient, QColor, QBrush
from PyQt5.QtCore import Qt

class TelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SYSON PDV PRÓ - Interface Avançada")
        self.setFixedSize(1000, 700)
        self.setStyleSheet("background-color: #0f0f0f;")
        self.initUI()

    def initUI(self):
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor("#0f0f0f"))
        gradient.setColorAt(1.0, QColor("#1f1f1f"))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignCenter)

        # LOGO
        logo = QLabel()
        pixmap = QPixmap("imagens/imgChatGPT.png")
        if pixmap.isNull():
            logo.setText("Imagem não encontrada.")
            logo.setStyleSheet("color: red; font-size: 20px;")
        else:
            logo.setPixmap(pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet("padding: 10px;")
        layout.addWidget(logo)

        # TÍTULO
        titulo = QLabel("SYSON PDV PRÓ")
        titulo.setFont(QFont("Arial", 40, QFont.Bold))
        titulo.setStyleSheet("color: #00ffc3;")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        frase = QLabel("Tecnologia além dos limites.")
        frase.setFont(QFont("Arial", 18))
        frase.setStyleSheet("color: #aaaaaa; margin-bottom: 30px;")
        frase.setAlignment(Qt.AlignCenter)
        layout.addWidget(frase)

        self.setCentralWidget(central_widget)
