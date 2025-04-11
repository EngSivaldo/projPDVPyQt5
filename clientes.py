import sys
import os
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QDialog, QLabel, QLineEdit, QPushButton, QFileDialog,
    QVBoxLayout, QHBoxLayout, QFormLayout, QComboBox, QDateEdit, QTextEdit,
    QDoubleSpinBox, QWidget, QGridLayout
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QDate


class CadastroClientes(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cadastro de Clientes")
        self.setMinimumWidth(1100)
        self.setStyleSheet("background-color: #007ACC; color: white;")

        self.conexao = sqlite3.connect("banco_dados.db")
        self.cursor = self.conexao.cursor()
        self.criar_tabela()

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

        # === Campos de entrada ===
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
        self.uf_input = QComboBox(); self.uf_input.addItems(
            ["", "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO",
             "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ",
             "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]); self.uf_input.setStyleSheet(input_style)
        self.telefone_input = QLineEdit(); self.telefone_input.setStyleSheet(input_style)
        self.cadastro_input = QDateEdit(); self.cadastro_input.setCalendarPopup(True); self.cadastro_input.setDate(QDate.currentDate()); self.cadastro_input.setStyleSheet(input_style)
        self.tipo_cliente_input = QComboBox(); self.tipo_cliente_input.addItems(["", "ATACADO", "VAREJO", "DESATIVADO"]); self.tipo_cliente_input.setStyleSheet(input_style)
        self.limite_input = QDoubleSpinBox(); self.limite_input.setMaximum(999999.99); self.limite_input.setStyleSheet(input_style)
        self.disponivel_input = QDoubleSpinBox(); self.disponivel_input.setMaximum(999999.99); self.disponivel_input.setStyleSheet(input_style)
        self.controlar_input = QComboBox(); self.controlar_input.addItems(["NÃO", "SIM"]); self.controlar_input.setStyleSheet(input_style)
        self.obs_input = QTextEdit(); self.obs_input.setStyleSheet("max-width: 250px;")

        campos = [
            ("Código", self.codigo_input), ("Descrição", self.nome_input),
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

        self.adicionar_foto_btn = QPushButton("Adicionar Foto")
        self.adicionar_foto_btn.clicked.connect(self.adicionar_foto)
        self.remover_foto_btn = QPushButton("Remover Foto")
        self.remover_foto_btn.clicked.connect(self.remover_foto)

        botoes_foto_layout = QVBoxLayout()
        botoes_foto_layout.addWidget(self.foto_label)
        botoes_foto_layout.addWidget(self.adicionar_foto_btn)
        botoes_foto_layout.addWidget(self.remover_foto_btn)
        botoes_foto_layout.addStretch()

        # ====== BOTÕES GERAIS ======
        salvar_btn = QPushButton("Salvar")
        salvar_btn.clicked.connect(self.salvar_cliente)

        layout_principal = QHBoxLayout()
        layout_principal.addWidget(form_widget)
        layout_principal.addLayout(botoes_foto_layout)

        layout_geral = QVBoxLayout()
        layout_geral.addLayout(layout_principal)
        layout_geral.addWidget(salvar_btn)

        self.setLayout(layout_geral)

    def criar_tabela(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT, nome TEXT, sexo TEXT, cpf TEXT, rg TEXT, cep TEXT,
                bairro TEXT, nasc TEXT, celular TEXT, email TEXT, estado_civil TEXT,
                endereco TEXT, cidade TEXT, uf TEXT, telefone TEXT, data_cadastro TEXT,
                tipo_cliente TEXT, limite REAL, disponivel REAL, controlar TEXT,
                observacao TEXT, foto TEXT
            )
        """)
        self.conexao.commit()

    def adicionar_foto(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Selecionar Foto", "", "Imagens (*.png *.jpg *.jpeg)")
        if file_name:
            pixmap = QPixmap(file_name).scaled(260, 260, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.foto_label.setPixmap(pixmap)
            self.foto_path = file_name

    def remover_foto(self):
        self.foto_label.clear()
        self.foto_path = None

    # ... (todo o código acima permanece igual até o final do método criar_tabela)

    def criar_tabela(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT,
                nome TEXT,
                sexo TEXT,
                cpf TEXT,
                rg TEXT,
                cep TEXT,
                bairro TEXT,
                nasc TEXT,
                celular TEXT,
                email TEXT,
                estado_civil TEXT,
                endereco TEXT,
                cidade TEXT,
                uf TEXT,
                telefone TEXT,
                data_cadastro TEXT,
                tipo_cliente TEXT,
                limite REAL,
                disponivel REAL,
                controlar_limite TEXT,
                obs TEXT,
                foto_path TEXT
            )
        """)
        self.conexao.commit()

    def salvar_cliente(self):
        # Gerar código automaticamente
        self.cursor.execute("SELECT MAX(codigo) FROM clientes")
        ultimo_codigo = self.cursor.fetchone()[0]

        if ultimo_codigo:
            try:
                proximo_codigo = str(int(ultimo_codigo) + 1).zfill(5)  # Ex: '00004'
            except ValueError:
                proximo_codigo = "00001"
        else:
            proximo_codigo = "00001"

        # Inserir no banco
        self.cursor.execute("""
            INSERT INTO clientes (
                codigo, nome, sexo, cpf, rg, cep, bairro, nasc, celular,
                email, estado_civil, endereco, cidade, uf, telefone,
                data_cadastro, tipo_cliente, limite, disponivel,
                controlar_limite, obs, foto_path
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            proximo_codigo, self.nome_input.text(), self.sexo_input.currentText(),
            self.cpf_input.text(), self.rg_input.text(), self.cep_input.text(),
            self.bairro_input.text(), self.nasc_input.date().toString("yyyy-MM-dd"),
            self.cel_input.text(), self.email_input.text(), self.estado_civil_input.currentText(),
            self.endereco_input.text(), self.cidade_input.text(), self.uf_input.currentText(),
            self.telefone_input.text(), self.cadastro_input.date().toString("yyyy-MM-dd"),
            self.tipo_cliente_input.currentText(), self.limite_input.value(),
            self.disponivel_input.value(), self.controlar_input.currentText(),
            self.obs_input.toPlainText(), getattr(self, "foto_path", "")
        ))

        self.conexao.commit()


    def adicionar_foto(self):
        foto, _ = QFileDialog.getOpenFileName(self, "Selecionar Foto", "", "Imagens (*.png *.jpg *.jpeg)")
        if foto:
            self.foto_path = foto
            pixmap = QPixmap(foto).scaled(self.foto_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.foto_label.setPixmap(pixmap)

    def remover_foto(self):
        self.foto_label.clear()
        self.foto_path = ""

    def exibir_lista_clientes(self):
        lista = ListaClientes()
        lista.exec_()


class ListaClientes(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lista de Clientes")
        self.setMinimumSize(600, 400)
        self.setStyleSheet("background-color: white; color: black;")

        layout = QVBoxLayout()
        self.tabela = QWidget()
        self.layout_tabela = QVBoxLayout()
        self.tabela.setLayout(self.layout_tabela)
        layout.addWidget(self.tabela)

        self.setLayout(layout)
        self.carregar_dados()

    def carregar_dados(self):
        conn = sqlite3.connect("banco_dados.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, cpf, celular FROM clientes ORDER BY nome")

        clientes = cursor.fetchall()
        conn.close()

        from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
        tabela = QTableWidget()
        tabela.setColumnCount(4)
        tabela.setHorizontalHeaderLabels(["ID", "Nome", "CPF", "Celular"])
        tabela.setRowCount(len(clientes))

        for row, cliente in enumerate(clientes):
            for col, valor in enumerate(cliente):
                item = QTableWidgetItem(str(valor))
                tabela.setItem(row, col, item)

        self.layout_tabela.addWidget(tabela)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = CadastroClientes()

    # Cria o botão Lista (F4)
    btn_lista = QPushButton("Lista (F4)")
    btn_lista.clicked.connect(janela.exibir_lista_clientes)
    janela.layout().addWidget(btn_lista)

    janela.show()
    sys.exit(app.exec_())
