import sys
from PyQt5.QtWidgets import (
    QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication


class TelaImpressoras(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IMPRESSORAS")
        self.setFixedSize(520, 350)
        self.setStyleSheet("background-color: white;")
        self.setStyleSheet("background-color: #0f6cbf; color: white;")
        self.init_ui()


    def init_ui(self):
        layout = QVBoxLayout()

        # Imagem de topo
        imagem_topo = QLabel()
        imagem_topo.setPixmap(QPixmap("imagens/impressoras_topo.png").scaledToWidth(500, Qt.SmoothTransformation))
        imagem_topo.setAlignment(Qt.AlignCenter)
        layout.addWidget(imagem_topo)

        # Grade com botões de impressoras
        grid_layout = QGridLayout()
        botoes_info = [
            ("Impressora SAT", "imagens/icone_sat.png"),
            ("Impressora NFC-e", "imagens/icone_nfce.png"),
            ("Impressora Cupom", "imagens/icone_cupom.png"),
            ("Impressora Etiquetas", "imagens/icone_etiqueta.png"),
        ]

        for i, (descricao, icone) in enumerate(botoes_info):
            botao = QPushButton(descricao)
            botao.setIcon(QIcon(icone))
            botao.setIconSize(QSize(48, 48))
            botao.setFixedSize(200, 60)
            botao.setStyleSheet("""
                QPushButton {
                    background-color: gray;
                    color: white;
                    font-weight: bold;
                    font-size: 12px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: orange;
                }
            """)
            botao.clicked.connect(lambda _, descricao=descricao: self.mostrar_mensagem(descricao))
            grid_layout.addWidget(botao, i // 2, i % 2)

        layout.addLayout(grid_layout)

        # Rodapé
        rodape_layout = QHBoxLayout()
        rodape_layout.addStretch()

        btn_sair = QPushButton("Sair")
        btn_sair.setFixedSize(100, 40)
        btn_sair.setStyleSheet("""
            QPushButton {
                background-color: #A80000;
                color: white;
                font-weight: bold;
                font-size: 12px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: red;
            }
        """)
        btn_sair.clicked.connect(self.close)
        rodape_layout.addWidget(btn_sair)

        layout.addLayout(rodape_layout)
        self.setLayout(layout)

    def mostrar_mensagem(self, descricao):
        QMessageBox.information(self, "Impressora", f"Configuração da {descricao} ainda não implementada.")

# Teste individual
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TelaImpressoras()
    window.exec_()
