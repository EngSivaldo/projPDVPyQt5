from PyQt5.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QGridLayout, QDateEdit, QComboBox, QMessageBox
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import QDate, Qt

class TelaFecharCaixa(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FECHAR CAIXA")
        self.setFixedSize(410, 440)
        self.setStyleSheet("background-color: #0073a6; color: white; font-family: Arial;")

        layout = QGridLayout()
        self.setLayout(layout)

        # Título
        titulo = QLabel("FECHAR CAIXA")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setFont(QFont("Arial", 18, QFont.Bold))
        layout.addWidget(titulo, 0, 0, 1, 3)

        # Subtítulo
        subtitulo = QLabel("SEJA BEM VINDO descricao DO FUNCIONARIO")
        subtitulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitulo, 1, 0, 1, 3)

        # Data
        label_data = QLabel("Data:")
        self.data = QDateEdit(calendarPopup=True)
        self.data.setDate(QDate.currentDate())
        self.data.setStyleSheet("color: black;")
        layout.addWidget(label_data, 2, 0)
        layout.addWidget(self.data, 3, 0)

        # Data Atual
        label_data_atual = QLabel("Data Atual:")
        data_atual = QLabel(QDate.currentDate().toString("dd/MM/yyyy"))
        data_atual.setStyleSheet("background-color: white; color: black; padding: 4px;")
        layout.addWidget(label_data_atual, 2, 2)
        layout.addWidget(data_atual, 3, 2)

        # Imagem do caixa
        caixa_img = QLabel()
        caixa_img.setPixmap(QPixmap("imagens/icone_caixa.png").scaled(160, 160, Qt.KeepAspectRatio))
        layout.addWidget(caixa_img, 4, 2, 4, 1)

        # Usuário
        layout.addWidget(QLabel("Usuário:"), 4, 0)
        self.combo_usuario = QComboBox()
        self.combo_usuario.addItem("ADMIN")
        self.combo_usuario.setStyleSheet("color: black;")
        layout.addWidget(self.combo_usuario, 5, 0)

        # Valor no Caixa
        layout.addWidget(QLabel("Valor no Caixa:"), 6, 0)
        self.valor_caixa = QLineEdit("0,00")
        self.valor_caixa.setStyleSheet("color: black; font-size: 16px; font-weight: bold;")
        layout.addWidget(self.valor_caixa, 7, 0)

        aviso = QLabel("VALOR DE DINHEIRO NA GAVETA")
        aviso.setStyleSheet("color: red; font-size: 10px;")
        layout.addWidget(aviso, 8, 0)

        # Senha
        layout.addWidget(QLabel("Senha:"), 9, 0)
        self.senha = QLineEdit()
        self.senha.setEchoMode(QLineEdit.Password)
        self.senha.setStyleSheet("color: black;")
        layout.addWidget(self.senha, 10, 0)

        # Botões
        botoes = QHBoxLayout()
        btn_voltar = QPushButton("VOLTAR")
        btn_voltar.setStyleSheet("background-color: #005b85; color: white; padding: 10px;")
        btn_voltar.clicked.connect(self.close)

        btn_fechar = QPushButton("FECHAR CAIXA")
        btn_fechar.setStyleSheet("background-color: orange; color: white; padding: 10px;")

        btn_relatorio = QPushButton("RELATÓRIO FINAL")
        btn_relatorio.setStyleSheet("background-color: #005b85; color: white; padding: 10px;")

        botoes.addWidget(btn_voltar)
        botoes.addWidget(btn_fechar)
        botoes.addWidget(btn_relatorio)

        layout.addLayout(botoes, 11, 0, 1, 3)

