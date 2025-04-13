from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtGui import QFont

class TelaCancelarVenda(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cancelar Venda")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()

        label = QLabel("Tem certeza que deseja cancelar a venda?")
        label.setFont(QFont("Arial", 11))
        layout.addWidget(label)

        botoes = QHBoxLayout()

        btn_confirmar = QPushButton("Cancelar Venda")
        btn_confirmar.setStyleSheet("background-color: red; color: white; font-weight: bold;")
        btn_confirmar.clicked.connect(self.accept)
        botoes.addWidget(btn_confirmar)

        btn_voltar = QPushButton("Voltar")
        btn_voltar.clicked.connect(self.reject)
        botoes.addWidget(btn_voltar)

        layout.addLayout(botoes)
        self.setLayout(layout)
