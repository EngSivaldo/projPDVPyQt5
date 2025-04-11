from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from etiquetas.modelo_tela_1 import TelaGerarEtiquetasModelo1

from etiquetas.modelo_tela_2 import TelaGerarEtiquetasModelo2


class SelecaoModeloEtiqueta(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Confirm")
        self.setFixedSize(380, 150)
        self.setStyleSheet("background-color: #0073a9; color: white; font: 10pt 'Segoe UI';")
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)

        layout = QVBoxLayout()
        
        # Label com ícone
        h_layout = QHBoxLayout()
        icon_label = QLabel()
        icon_label.setPixmap(QPixmap("imagens/question.png").scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        h_layout.addWidget(icon_label)

        texto = QLabel("Selecione o modelo da tela que deseja abrir?")
        h_layout.addWidget(texto)
        layout.addLayout(h_layout)

        # Botões
        botoes_layout = QHBoxLayout()

        botao1 = QPushButton("MODELO TELA 1")
        botao1.setStyleSheet("background-color: orange; color: white; padding: 5px;")
        botao1.clicked.connect(self.abrir_modelo_1)

        botao2 = QPushButton("MODELO TELA 2")
        botao2.setStyleSheet("background-color: transparent; color: white; border: 1px solid white; padding: 5px;")
        botao2.clicked.connect(self.abrir_modelo_2)

        botoes_layout.addWidget(botao1)
        botoes_layout.addWidget(botao2)
        layout.addLayout(botoes_layout)

        self.setLayout(layout)

    def abrir_modelo_1(self):
        self.close()
        janela = TelaGerarEtiquetasModelo1()
        janela.exec_()

    def abrir_modelo_2(self):
        self.close()
        janela = TelaGerarEtiquetasModelo2()
        janela.exec_()
