# gerar_etiquetas/modelo1_etiquetas.py
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QTextEdit, QTableWidget, QRadioButton, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

class TelaGerarEtiquetasModelo1(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerar Etiquetas - Modelo 1")
        self.setFixedSize(880, 587)
        self.setStyleSheet("background-color: #0077b6; color: white; font-family: Arial;")

        layout = QGridLayout()

        label_codigo = QLabel("Código [F5]:")
        label_codigo.setFont(QFont("Arial", 12, QFont.Bold))
        self.input_codigo = QLineEdit()
        self.input_codigo.setFixedWidth(200)
        lupa = QLabel()
        lupa.setPixmap(QPixmap("imagens/icone_lupa.png").scaled(24, 24, Qt.KeepAspectRatio))
        lupa.setFixedWidth(30)

        layout.addWidget(label_codigo, 0, 0)
        layout.addWidget(self.input_codigo, 0, 1)
        layout.addWidget(lupa, 0, 2)

        instrucao = QLabel("Insira o código do produto e pressione [Enter]")
        instrucao.setStyleSheet("font-size: 9pt; color: #ffffff;")
        layout.addWidget(instrucao, 1, 0, 1, 3)

        codigo_barra_1 = QLabel()
        codigo_barra_1.setPixmap(QPixmap("imagens/barcode1.png").scaled(400, 80, Qt.KeepAspectRatio))
        layout.addWidget(codigo_barra_1, 2, 0, 1, 3)

        layout.addWidget(QLabel("Quantidade"), 3, 0)
        self.input_qtd = QLineEdit("01")
        self.input_qtd.setFixedWidth(100)
        layout.addWidget(self.input_qtd, 3, 1)

        codigo_barra_2 = QLabel()
        codigo_barra_2.setPixmap(QPixmap("imagens/barcode2.png").scaled(400, 80, Qt.KeepAspectRatio))
        layout.addWidget(codigo_barra_2, 4, 0, 1, 3)

        botoes = QHBoxLayout()
        for descricao in ["Adicionar", "Cancelar", "Excluir", "Imprimir"]:
            btn = QPushButton(descricao)
            botoes.addWidget(btn)
        layout.addLayout(botoes, 5, 0, 1, 3)

        tabela = QTableWidget()
        layout.addWidget(tabela, 0, 3, 6, 2)

        grupo = QGroupBox("Modelos de Impressoras")
        grid = QGridLayout()
        impressoras = [
            "Deskjet Laser 38,1mm x 21,2mm", "Impressora Térmica Rolo 80mm x 40mm", "Impressora Rolo 95mm x 12mm",
            "Deskjet Laser 25,4mm x 63,5mm", "Impressora Térmica Rolo 100mm x 30mm", "Impressora Rolo 50mm x 30mm",
            "Deskjet Laser 63,5mm x 38,1mm", "Impressora Térmica Rolo 100mm x 50mm", "Impressora Rolo 35mm x 60mm x 3",
            "Deskjet Laser 17,0mm x 31,0mm", "Impressora Térmica Rolo 60mm x 30mm", "Impressora Térmica Rolo 70mm x 35mm",
        ]
        for i, texto in enumerate(impressoras):
            radio = QRadioButton(texto)
            grid.addWidget(radio, i // 3, i % 3)
        grupo.setLayout(grid)
        layout.addWidget(grupo, 6, 0, 1, 5)

        total = QLabel("Quantidades de Etiquetas: 0")
        total.setStyleSheet("color: white; font-weight: bold;")
        layout.addWidget(total, 7, 4)

        self.setLayout(layout)
