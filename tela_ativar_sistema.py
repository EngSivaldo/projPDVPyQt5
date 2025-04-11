from PyQt5.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QApplication
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
import sys
from janela import MainPDVWindow  # Importa a janela principal

class TelaAtivarSistema(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ativar o Sistema pdv")
        self.setFixedSize(420, 240)
        self.setStyleSheet("background-color: navy; color: white;")
        self.initUI()

    def initUI(self):
        fonte_label = QFont("Arial", 10, QFont.Bold)
        fonte_input = QFont("Arial", 10)

        # Título
        titulo = QLabel("Ativar o Sistema pdv", self)
        titulo.setFont(QFont("Arial", 14, QFont.Bold))
        titulo.setStyleSheet("color: white; background-color: navy;")
        titulo.setAlignment(Qt.AlignCenter)

        # E-mail
        lbl_email = QLabel("E-mail:")
        lbl_email.setFont(fonte_label)
        self.input_email = QLineEdit()
        self.input_email.setFont(fonte_input)
        self.input_email.setStyleSheet("background-color: white; color: black;")

        # Chave
        lbl_chave = QLabel("Chave:")
        lbl_chave.setFont(fonte_label)
        self.input_chave = QLineEdit()
        self.input_chave.setFont(fonte_input)
        self.input_chave.setStyleSheet("background-color: white; color: black;")

        # Botão "ATIVAR ONLINE" (simulado)
        btn_ativar_online = QLabel("ATIVAR ONLINE ✅")
        btn_ativar_online.setFont(fonte_label)
        btn_ativar_online.setStyleSheet("color: white; background-color: navy; padding: 5px;")

        # Botões
        self.btn_teste = QPushButton("Usar Versão de Teste")
        self.btn_teste.setFont(fonte_label)
        self.btn_teste.setStyleSheet("background-color: red; color: white;")
        self.btn_teste.clicked.connect(self.usar_versao_teste)

        self.btn_ativar = QPushButton("ATIVAR")
        self.btn_ativar.setFont(fonte_label)
        self.btn_ativar.setStyleSheet("background-color: green; color: white;")
        self.btn_ativar.clicked.connect(self.ativar_sistema)

        # Layouts
        layout_main = QVBoxLayout()
        layout_main.addWidget(titulo)
        layout_main.addSpacing(10)
        layout_main.addWidget(lbl_email)
        layout_main.addWidget(self.input_email)
        layout_main.addSpacing(5)
        layout_main.addWidget(lbl_chave)
        layout_main.addWidget(self.input_chave)
        layout_main.addSpacing(10)
        layout_main.addWidget(btn_ativar_online)

        layout_botoes = QHBoxLayout()
        layout_botoes.addWidget(self.btn_teste)
        layout_botoes.addWidget(self.btn_ativar)
        layout_main.addLayout(layout_botoes)

        self.setLayout(layout_main)

    def ativar_sistema(self):
        usuario = self.input_email.text().strip()
        codigo = self.input_chave.text().strip()

        if not usuario or not codigo:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Erro", "Por favor, preencha o e-mail e a chave.")
            return

        self.accept()  # <- Adicione esta linha se estiver usando exec_()
        self.abrir_janela_principal(versao_teste=False, usuario_logado=usuario, codigo_usuario=codigo)




    def usar_versao_teste(self):
        self.accept()  # Fecha a tela
        self.abrir_janela_principal(versao_teste=True)

    def abrir_janela_principal(self, versao_teste=False, usuario_logado="Usuário", codigo_usuario="000"):
        self.janela = MainPDVWindow(
            versao_teste=versao_teste,
            usuario_logado=usuario_logado,
            codigo_usuario=codigo_usuario
        )
        self.janela.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TelaAtivarSistema()
    window.setWindowIcon(QIcon("imagens/liderMotocap.jpeg"))  # Opcional
    if window.exec_() == QDialog.Accepted:
        sys.exit(app.exec_())
