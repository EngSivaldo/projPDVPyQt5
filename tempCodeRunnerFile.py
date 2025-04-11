import sys
import os
import sqlite3
from PyQt5.QtWidgets import (QApplication, QDialog, QLabel, QLineEdit, QPushButton, QFileDialog, 
                             QVBoxLayout, QHBoxLayout, QFormLayout, QComboBox, QDateEdit, QTextEdit, QDoubleSpinBox, QCheckBox, QWidget, QGridLayout)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QDate

class CadastroClientes(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cadastro de Clientes")
        self.setStyleSheet("background-color: #007ACC; color: white;")
        self.setMinimumWidth(1000)

        self.conexao = sqlite3.connect("banco_daods.db")
        self.cursor = self.conexao.cursor()
        self.criar_tabela()
                # No início do __init__ (antes de criar widgets), adicione:
        # self.setStyleSheet("""
        #     QLabel {
        #         color: blue;
        #         font-size: 14px;
        #     }
        #     QLineEdit, QComboBox, QDateEdit, QDoubleSpinBox, QTextEdit {
        #         background-color: white;
        #         color: black;
        #         border: 1px solid gray;
        #         border-radius: 5px;
        #         padding: 3px;
        #         font-size: 13px;
        #     }
        #     QPushButton {
        #         font-weight: bold;
        #         font-size: 13px;
        #         border-radius: 6px;
        #         padding: 6px;
        #     }
        #     QPushButton:hover {
        #         background-color: #0055aa;
        #     }
        #     QTextEdit {
        #         background-color: white;
        #         border: 1px solid gray;
        #         border-radius: 5px;
        #     }
        # """)


        # ====== INPUTS EM GRELHA À ESQUERDA ======
        form_widget = QWidget()
        form_layout = QGridLayout()
        input_style = """
            background-color: white;
            color: black;
            min-height: 25px;
            max-width: 250px;
            border-radius: 4px;
            padding-left: 4px;
        """


        self.codigo_input = QLineEdit(); self.codigo_input.setStyleSheet(input_style)
        self.nome_input = QLineEdit(); self.nome_input.setStyleSheet(input_style)
        self.sexo_input = QComboBox(); self.sexo_input.addItems(["", "FEMININO", "MASCULINO"]); self.sexo_input.setStyleSheet(input_style)
        self.cpf_input = QLineEdit(); self.cpf_input.setStyleSheet(input_style)
        self.rg_input = QLineEdit(); self.rg_input.setStyleSheet(input_style)
        self.cep_input = QLineEdit(); self.cep_input.setStyleSheet(input_style)
        self.bairro_input = QLineEdit(); self.bairro_input.setStyleSheet(input_style)
        self.nasc_input = QDateEdit(); self.nasc_input.setCalendarPopup(True); self.nasc_input.setDate(QDate.currentDate()); self.nasc_input.setStyleSheet(input_style)
        self.cel_input = QLineEdit(); self.cel_input.setStyleSheet(input_style)
        self.email_input = QLineEdit(); self.email_input.setStyleSheet(input_style)
        self.estado_civil_input = QComboBox(); self.estado_civil_input.addItems(["", "SOLTEIRO", "CASADO", "DIVORCIADO"]); self.estado_civil_input.setStyleSheet(input_style)
        self.endereco_input = QLineEdit(); self.endereco_input.setStyleSheet(input_style)
        self.cidade_input = QLineEdit(); self.cidade_input.setStyleSheet(input_style)
        self.uf_input = QComboBox(); self.uf_input.addItems(["", "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]); self.uf_input.setStyleSheet(input_style)
        self.telefone_input = QLineEdit(); self.telefone_input.setStyleSheet(input_style)
        self.cadastro_input = QDateEdit(); self.cadastro_input.setCalendarPopup(True); self.cadastro_input.setDate(QDate.currentDate()); self.cadastro_input.setStyleSheet(input_style)
        self.tipo_cliente_input = QComboBox(); self.tipo_cliente_input.addItems(["", "ATACADO", "VAREJO", "DESATIVADO"]); self.tipo_cliente_input.setStyleSheet(input_style)
        self.limite_input = QDoubleSpinBox(); self.limite_input.setMaximum(999999.99); self.limite_input.setStyleSheet(input_style)
        self.disponivel_input = QDoubleSpinBox(); self.disponivel_input.setMaximum(999999.99); self.disponivel_input.setStyleSheet(input_style)
        self.controlar_input = QComboBox(); self.controlar_input.addItems(["NÃO", "SIM"]); self.controlar_input.setStyleSheet(input_style)
        self.obs_input = QTextEdit(); self.obs_input.setStyleSheet("max-width: 250px;")

        campos = [
            ("Código", self.codigo_input), ("descricao", self.nome_input),
            ("Sexo", self.sexo_input), ("CPF/CNPJ", self.cpf_input),
            ("RG/IE", self.rg_input), ("CEP", self.cep_input),
            ("Bairro", self.bairro_input), ("Data de Nasc", self.nasc_input),
            ("Celular", self.cel_input), ("E-mail", self.email_input),
            ("Estado Civil", self.estado_civil_input), ("Endereço", self.endereco_input),
            ("Cidade", self.cidade_input), ("UF", self.uf_input),
            ("Telefone", self.telefone_input), ("Data Cadastro", self.cadastro_input),
            ("Tipo de Preço do Cliente", self.tipo_cliente_input), ("Limite Crédito", self.limite_input),
            ("Limite Disponível", self.disponivel_input), ("Controlar limite", self.controlar_input),
            ("Observação", self.obs_input)
        ]

        for i, (label, widget) in enumerate(campos):
            row, col = divmod(i, 2)
            form_layout.addWidget(QLabel(label), row, col * 2)
            form_layout.addWidget(widget, row, col * 2 + 1)

        form_widget.setLayout(form_layout)

        # ====== IMAGEM À DIREITA ======
        self.foto_label = QLabel()
        self.foto_label.setFixedSize(260, 260)
        self.foto_label.setStyleSheet("background-color: white; border: 1px solid gray; border-radius: 10px;")
        self.foto_label.setAlignment(Qt.AlignCenter)

        self.adicionar_foto_btn = QPushButton("Adicionar Foto - F7")
        self.adicionar_foto_btn.setStyleSheet("background-color: #0099FF; color: white;")
        self.adicionar_foto_btn.clicked.connect(self.selecionar_foto)

        self.remover_foto_btn = QPushButton("Remover foto")
        self.remover_foto_btn.setStyleSheet("background-color: #CC3333; color: white;")
        self.remover_foto_btn.clicked.connect(self.remover_foto)

        foto_layout = QVBoxLayout()
        foto_layout.addWidget(self.foto_label)
        foto_layout.addWidget(self.adicionar_foto_btn)
        foto_layout.addWidget(self.remover_foto_btn)

        # ====== BOTÕES INFERIORES ======
        self.salvar_btn = QPushButton("Salvar - F3")
        self.salvar_btn.setStyleSheet("background-color: #0055CC; color: white; padding: 10px; border-radius: 8px;")
        self.salvar_btn.clicked.connect(self.salvar_cliente)

        # ====== LAYOUT PRINCIPAL ======
        layout_principal = QHBoxLayout()
        layout_principal.addWidget(form_widget, 3)
        layout_principal.addLayout(foto_layout, 1)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout_principal)
        main_layout.addWidget(self.salvar_btn)

        self.setLayout(main_layout)

    def criar_tabela(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT, descricao TEXT, sexo TEXT, cpf TEXT, rg TEXT, cep TEXT, bairro TEXT,
            nasc TEXT, celular TEXT, email TEXT, estado_civil TEXT, endereco TEXT,
            cidade TEXT, uf TEXT, telefone TEXT, cadastro TEXT, tipo_cliente TEXT,
            limite REAL, disponivel REAL, controlar_limite TEXT, observacao TEXT,
            foto TEXT
        )''')
        self.conexao.commit()

    def selecionar_foto(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Selecionar Foto", "", "Imagens (*.png *.jpg *.bmp)")
        if file_name:
            pixmap = QPixmap(file_name).scaled(260, 260, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.foto_label.setPixmap(pixmap)
            self.foto_path = file_name

    def remover_foto(self):
        self.foto_label.clear()
        self.foto_path = ""

    def salvar_cliente(self):
        descricao = self.nome_input.text()
        cpf = self.cpf_input.text()
        email = self.email_input.text()

        if not descricao:
            self.nome_input.setStyleSheet("border: 2px solid red;")
            return

        dados = (
            self.codigo_input.text(),
            descricao,
            self.sexo_input.currentText(),
            cpf,
            self.rg_input.text(),
            self.cep_input.text(),
            self.bairro_input.text(),
            self.nasc_input.date().toString("yyyy-MM-dd"),
            self.cel_input.text(),
            email,
            self.estado_civil_input.currentText(),
            self.endereco_input.text(),
            self.cidade_input.text(),
            self.uf_input.currentText(),
            self.telefone_input.text(),
            self.cadastro_input.date().toString("yyyy-MM-dd"),
            self.tipo_cliente_input.currentText(),
            self.limite_input.value(),
            self.disponivel_input.value(),
            self.controlar_input.currentText(),
            self.obs_input.toPlainText(),
            getattr(self, 'foto_path', '')
        )

        self.cursor.execute("""
            INSERT INTO clientes (
                codigo, descricao, sexo, cpf, rg, cep, bairro, nasc, celular, email,
                estado_civil, endereco, cidade, uf, telefone, cadastro, tipo_cliente,
                limite, disponivel, controlar_limite, observacao, foto
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, dados)

        self.conexao.commit()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    janela = CadastroClientes()
    janela.show()
    sys.exit(app.exec_())
