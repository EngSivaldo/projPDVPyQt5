import sqlite3
from PyQt5.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QComboBox,
    QHBoxLayout, QVBoxLayout, QGridLayout, QFileDialog, QMessageBox,
    QTableWidget, QTableWidgetItem, QInputDialog,  QSizePolicy, QHeaderView
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class CadastroProdutoWindow(QDialog):
    def __init__(self):
        super().__init__()
       

        self.setWindowTitle("Cadastro de Produtos")
        self.setFixedSize(950, 700)
        self.initUI()
        self.carregar_tabela()
       
        
    def editar_estoque(self, row, column):
        if column != 2:
            return  # Só permite editar o estoque (coluna 2)

        descricao = self.tabela_produtos.item(row, 1).text()  # Coluna 1 = Descrição

        novo_estoque, ok = QInputDialog.getInt(self, "Editar Estoque",
                                            f"Novo estoque para '{descricao}':", min=0)
        if ok:
            try:
                conexao = sqlite3.connect("banco_dados.db")
                cursor = conexao.cursor()
                cursor.execute("UPDATE produtos SET estoque = ? WHERE descricao = ?", (novo_estoque, descricao))
                conexao.commit()
                conexao.close()

                QMessageBox.information(self, "Estoque Atualizado", f"Estoque de '{descricao}' atualizado com sucesso!")
                self.carregar_tabela()
                
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao atualizar o estoque: {str(e)}")


    def initUI(self):
        layout = QVBoxLayout()

        titulo = QLabel("CADASTRO DE PRODUTOS")
        titulo.setStyleSheet("font-size: 28px; font-weight: bold;")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        grid = QGridLayout()
        grid.setSpacing(10)

        self.codigo = QLineEdit(); grid.addWidget(QLabel("Código:"), 0, 0); grid.addWidget(self.codigo, 0, 1)
        self.descricao = QLineEdit(); grid.addWidget(QLabel("Descrição:"), 0, 2); grid.addWidget(self.descricao, 0, 3)
        self.fornecedor = QLineEdit(); grid.addWidget(QLabel("Fornecedor:"), 1, 0); grid.addWidget(self.fornecedor, 1, 1)
        self.unidade = QComboBox(); self.unidade.addItems(["UN", "LT", "KG", "CX"]); grid.addWidget(QLabel("Unidade:"), 1, 2); grid.addWidget(self.unidade, 1, 3)
        self.preco_compra = QLineEdit(); grid.addWidget(QLabel("Preço de Compra:"), 2, 0); grid.addWidget(self.preco_compra, 2, 1)
        self.preco_venda = QLineEdit(); grid.addWidget(QLabel("Preço de Venda:"), 2, 2); grid.addWidget(self.preco_venda, 2, 3)
        self.preco_prazo = QLineEdit(); grid.addWidget(QLabel("Preço a Prazo:"), 3, 0); grid.addWidget(self.preco_prazo, 3, 1)
        self.preco_atacado = QLineEdit(); grid.addWidget(QLabel("Preço Atacado:"), 3, 2); grid.addWidget(self.preco_atacado, 3, 3)
        self.estoque = QLineEdit(); grid.addWidget(QLabel("Estoque Atual:"), 4, 0); grid.addWidget(self.estoque, 4, 1)
        self.estoque_minimo = QLineEdit(); grid.addWidget(QLabel("Est. Mínimo:"), 4, 2); grid.addWidget(self.estoque_minimo, 4, 3)
        self.grupo = QComboBox(); self.grupo.addItems(["BEBIDAS", "ALIMENTOS", "LIMPEZA"]); grid.addWidget(QLabel("Grupo:"), 5, 0); grid.addWidget(self.grupo, 5, 1)
        self.categoria = QComboBox(); self.categoria.addItems(["REFRIGERANTES", "DOCES", "LATICÍNIOS"]); grid.addWidget(QLabel("Categoria:"), 5, 2); grid.addWidget(self.categoria, 5, 3)
        self.marca = QLineEdit(); grid.addWidget(QLabel("Marca:"), 6, 0); grid.addWidget(self.marca, 6, 1)
        self.subgrupo = QLineEdit(); grid.addWidget(QLabel("Subgrupo:"), 6, 2); grid.addWidget(self.subgrupo, 6, 3)
        self.ingredientes = QLineEdit(); grid.addWidget(QLabel("Ingredientes:"), 7, 0); grid.addWidget(self.ingredientes, 7, 1, 1, 3)
        self.tamanho = QLineEdit(); grid.addWidget(QLabel("Tamanho:"), 8, 0); grid.addWidget(self.tamanho, 8, 1)
        self.balanca = QComboBox(); self.balanca.addItems(["SIM", "NÃO"]); grid.addWidget(QLabel("Balança:"), 8, 2); grid.addWidget(self.balanca, 8, 3)
        self.lucro = QLineEdit(); grid.addWidget(QLabel("Lucro:"), 9, 0); grid.addWidget(self.lucro, 9, 1)
        self.lucro_porcento = QLineEdit(); grid.addWidget(QLabel("Lucro (%):"), 9, 2); grid.addWidget(self.lucro_porcento, 9, 3)
        self.obs = QLineEdit(); grid.addWidget(QLabel("Observação:"), 10, 0); grid.addWidget(self.obs, 10, 1, 1, 3)

        self.img = QLabel(); self.img.setFixedSize(200, 280)
        self.img.setStyleSheet("background-color: white; border: 1px solid #ccc;")
        self.img.setPixmap(QPixmap("coca.png").scaled(200, 280, Qt.KeepAspectRatio))
        self.caminho_imagem = "coca.png"
        grid.addWidget(self.img, 0, 4, 8, 1)

        self.btn_img = QPushButton("Buscar Foto")
        self.btn_img.clicked.connect(self.carregarImagem)
        grid.addWidget(self.btn_img, 8, 4)

        layout.addLayout(grid)

        botoes = QHBoxLayout()
        self.btn_novo = QPushButton("Novo - F2")
        self.btn_salvar = QPushButton("Salvar - F3")
        self.btn_salvar.clicked.connect(self.salvar_produto)
        botoes.addWidget(self.btn_novo)
        botoes.addWidget(self.btn_salvar)
        layout.addLayout(botoes)

        # TABELA DE PRODUTOS
        self.tabela_produtos = QTableWidget()
        self.tabela_produtos.setColumnCount(4)
        self.tabela_produtos.setHorizontalHeaderLabels(["Código", "Descrição", "Fornecedor", "Preço"])
        self.tabela_produtos.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tabela_produtos.horizontalHeader().setStretchLastSection(True)
        self.tabela_produtos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


        layout.addWidget(self.tabela_produtos)

        # Conectar o clique duplo da tabela à função de edição
        self.tabela_produtos.cellDoubleClicked.connect(self.editar_estoque)

        self.setLayout(layout)
        self.setStyleSheet("""
            QDialog { background-color: #0077B6; color: white; font-family: Arial; }
            QLineEdit, QComboBox { background-color: white; color: black; border: 1px solid #ccc; padding: 2px; }
            QLabel { font-weight: bold; }
            QPushButton { background-color: #023E8A; color: white; padding: 6px 12px; border-radius: 6px; }
        """)


    def carregarImagem(self):
        file, _ = QFileDialog.getOpenFileName(self, "Selecionar Imagem", "", "Imagens (*.png *.jpg *.jpeg)")
        if file:
            self.img.setPixmap(QPixmap(file).scaled(200, 280, Qt.KeepAspectRatio))
            self.caminho_imagem = file


    def salvar_produto(self):
        try:
            conexao = sqlite3.connect("banco_dados.db")
            cursor = conexao.cursor()

            cursor.execute("""
                INSERT INTO produtos (
                    codigo, descricao, fornecedor, unidade, preco_compra, preco_venda,
                    preco_prazo, preco_atacado, estoque, estoque_minimo, grupo,
                    categoria, marca, subgrupo, ingredientes, tamanho, balanca,
                    lucro, lucro_porcento, obs
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.codigo.text(), self.descricao.text(), self.fornecedor.text(),
                self.unidade.currentText(), float(self.preco_compra.text() or 0),
                float(self.preco_venda.text() or 0), float(self.preco_prazo.text() or 0),
                float(self.preco_atacado.text() or 0), float(self.estoque.text() or 0),
                float(self.estoque_minimo.text() or 0), self.grupo.currentText(),
                self.categoria.currentText(), self.marca.text(), self.subgrupo.text(),
                self.ingredientes.text(), self.tamanho.text(), self.balanca.currentText(),
                float(self.lucro.text() or 0), float(self.lucro_porcento.text() or 0),
                self.obs.text()
            ))

            conexao.commit()
            conexao.close()

            QMessageBox.information(self, "Sucesso", "Produto salvo com sucesso!")
            self.carregar_tabela()

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao salvar: {str(e)}")


    def carregar_tabela(self):
        try:
            conexao = sqlite3.connect("banco_dados.db")
            cursor = conexao.cursor()
            cursor.execute("SELECT codigo, descricao, fornecedor, preco_venda, estoque FROM produtos")
            dados = cursor.fetchall()
            conexao.close()

            self.tabela_produtos.setRowCount(0)
            self.tabela_produtos.setColumnCount(5)
            self.tabela_produtos.setHorizontalHeaderLabels(["Código", "Descrição", "Fornecedor", "Preço Venda", "Estoque"])

            for row_num, row_data in enumerate(dados):
                self.tabela_produtos.insertRow(row_num)
                for col_num, data in enumerate(row_data):
                    self.tabela_produtos.setItem(row_num, col_num, QTableWidgetItem(str(data)))

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao carregar os produtos: {str(e)}")





