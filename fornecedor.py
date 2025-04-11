from PyQt5.QtWidgets import (
    QDialog, QLabel, QLineEdit, QTextEdit, QPushButton, QComboBox,
    QVBoxLayout, QHBoxLayout, QGridLayout, QDateEdit, QMessageBox
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QDate, QSize
import sqlite3
import os

class TelaCadastroFornecedores(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cadastro de Fornecedores")
        self.setFixedSize(800, 680)
        self.setStyleSheet("background-color: #0077b6; color: white; font-size: 14px;")

        self.init_ui()
        self.criar_tabela()

    def init_ui(self):
        layout = QVBoxLayout()
        titulo = QLabel("CADASTRO DE FORNECEDORES")
        titulo.setStyleSheet("font-size: 24px; font-weight: bold;")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        grid = QGridLayout()
        grid.setSpacing(8)

        estilo_input = "background-color: white; color: black;"

        # Campos
        self.razao = QLineEdit()
        self.razao.setStyleSheet(estilo_input)
        self.fantasia = QLineEdit()
        self.fantasia.setStyleSheet(estilo_input)
        self.nome_vendedor = QLineEdit()
        self.nome_vendedor.setStyleSheet(estilo_input)
        self.endereco = QLineEdit()
        self.endereco.setStyleSheet(estilo_input)
        self.cidade = QLineEdit()
        self.cidade.setStyleSheet(estilo_input)
        self.telefone = QLineEdit()
        self.telefone.setStyleSheet(estilo_input)
        self.email = QLineEdit()
        self.email.setStyleSheet(estilo_input)
        self.tipo = QComboBox()
        self.tipo.addItems(["JURIDICA", "FISICA"])
        self.tipo.setStyleSheet(estilo_input)
        self.cpf_cnpj = QLineEdit()
        self.cpf_cnpj.setStyleSheet(estilo_input)
        self.tel_vendedor = QLineEdit()
        self.tel_vendedor.setStyleSheet(estilo_input)
        self.bairro = QLineEdit()
        self.bairro.setStyleSheet(estilo_input)
        self.cep = QLineEdit()
        self.cep.setStyleSheet(estilo_input)
        self.celular = QLineEdit()
        self.celular.setStyleSheet(estilo_input)
        self.data_cadastro = QDateEdit()
        self.data_cadastro.setDate(QDate.currentDate())
        self.data_cadastro.setCalendarPopup(True)
        self.data_cadastro.setStyleSheet(estilo_input)
        self.observacao = QTextEdit()
        self.observacao.setStyleSheet(estilo_input)

        # Adicionando ao grid (duas colunas de campos)
        campos = [
            ("Razão Social", self.razao), ("Tipo", self.tipo),
            ("descricao Fantasia", self.fantasia), ("CPF / CNPJ", self.cpf_cnpj),
            ("descricao Vendedor", self.nome_vendedor), ("Tel. Vendedor", self.tel_vendedor),
            ("Endereço", self.endereco), ("Bairro", self.bairro),
            ("Cidade", self.cidade), ("Cep", self.cep),
            ("Telefone", self.telefone), ("Celular", self.celular),
            ("E-mail", self.email), ("Data Cadastro", self.data_cadastro),
        ]

        for index, (label_text, widget) in enumerate(campos):
            row = index // 2
            col = (index % 2) * 2
            label = QLabel(label_text)
            grid.addWidget(label, row, col)
            grid.addWidget(widget, row, col + 1)

        layout.addLayout(grid)

        obs_label = QLabel("Observação")
        layout.addWidget(obs_label)
        layout.addWidget(self.observacao)

        # Botões
        botoes = QHBoxLayout()
        botoes.setSpacing(15)

        self.btn_novo = self.criar_botao("NOVO - F6", "imagens/novo.png", self.limpar_campos)
        self.btn_salvar = self.criar_botao("SALVAR - F5", "imagens/salvar.png", self.salvar)
        self.btn_editar = self.criar_botao("EDITAR - F7", "imagens/editar.png")
        self.btn_excluir = self.criar_botao("EXCLUIR - F8", "imagens/excluir.png")
        self.btn_lista = self.criar_botao("LISTA - F9", "imagens/lista.png")

        botoes.addWidget(self.btn_salvar)
        botoes.addWidget(self.btn_novo)
        botoes.addWidget(self.btn_editar)
        botoes.addWidget(self.btn_excluir)
        botoes.addWidget(self.btn_lista)

        layout.addLayout(botoes)
        self.setLayout(layout)

    def criar_botao(self, texto, imagem, funcao=None):
        btn = QPushButton(f"  {texto}")
        btn.setStyleSheet("background-color: white; color: black; font-weight: bold; height: 40px;")
        btn.setIconSize(QSize(32, 32))
        if os.path.exists(imagem):
            btn.setIcon(QIcon(QPixmap(imagem)))
        if funcao:
            btn.clicked.connect(funcao)
        return btn

    def limpar_campos(self):
        self.razao.clear()
        self.fantasia.clear()
        self.nome_vendedor.clear()
        self.endereco.clear()
        self.cidade.clear()
        self.telefone.clear()
        self.email.clear()
        self.cpf_cnpj.clear()
        self.tel_vendedor.clear()
        self.bairro.clear()
        self.cep.clear()
        self.celular.clear()
        self.observacao.clear()
        self.tipo.setCurrentIndex(0)
        self.data_cadastro.setDate(QDate.currentDate())

    def salvar(self):
        if self.razao.text() == "" or self.cpf_cnpj.text() == "":
            QMessageBox.warning(self, "Aviso", "Preencha pelo menos Razão Social e CPF/CNPJ.")
            return

        dados = (
            self.razao.text(), self.fantasia.text(), self.nome_vendedor.text(),
            self.endereco.text(), self.bairro.text(), self.cidade.text(),
            self.cep.text(), self.telefone.text(), self.celular.text(),
            self.email.text(), self.tipo.currentText(), self.cpf_cnpj.text(),
            self.tel_vendedor.text(), self.data_cadastro.date().toString("yyyy-MM-dd"),
            self.observacao.toPlainText()
        )
        try:
            con = sqlite3.connect("banco_dados.db")
            cur = con.cursor()
            cur.execute("""INSERT INTO fornecedores (
                razao, fantasia, nome_vendedor, endereco, bairro, cidade, cep,
                telefone, celular, email, tipo, cpf_cnpj, tel_vendedor, data_cadastro, observacao
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", dados)
            con.commit()
            con.close()
            QMessageBox.information(self, "Sucesso", "Fornecedor salvo com sucesso!")
            self.limpar_campos()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar: {str(e)}")

    def criar_tabela(self):
        try:
            con = sqlite3.connect("banco_dados.db")
            cur = con.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS fornecedores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                razao TEXT, fantasia TEXT, nome_vendedor TEXT, endereco TEXT, bairro TEXT,
                cidade TEXT, cep TEXT, telefone TEXT, celular TEXT, email TEXT,
                tipo TEXT, cpf_cnpj TEXT, tel_vendedor TEXT, data_cadastro TEXT,
                observacao TEXT
            )""")
            con.commit()
            con.close()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao criar tabela: {str(e)}")

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    janela = TelaCadastroFornecedores()
    janela.exec_()
