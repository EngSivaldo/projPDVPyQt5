import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QDialog, QLabel, QLineEdit, QPushButton,
                             QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox,
                             QWidget, QCompleter, QComboBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtGui import QColor
class PagamentoDialog(QDialog):
    def __init__(self, total, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Forma de Pagamento")
        self.total = total  # Total sem desconto
        self.total_com_desconto = total  # Total com desconto
        self.metodo = None

        self.setFixedSize(300, 260)
        layout = QVBoxLayout()

        # Total
        self.label_total = QLabel(f"Total a pagar: R$ {self.total:.2f}")
        layout.addWidget(self.label_total)

        # Campo de desconto
        self.label_desconto = QLabel("Desconto (% ou R$):")
        self.input_desconto = QLineEdit()
        self.input_desconto.setPlaceholderText("Digite valor ou %")
        layout.addWidget(self.label_desconto)
        layout.addWidget(self.input_desconto)

        # Combo de pagamento
        layout.addWidget(QLabel("Forma de Pagamento:"))
        self.combo_pagamento = QComboBox()
        self.combo_pagamento.addItems(["Dinheiro", "Cartão de Crédito", "Cartão de Débito", "PIX"])
        layout.addWidget(self.combo_pagamento)

        # Campo valor recebido (apenas para dinheiro)
        self.label_recebido = QLabel("Valor Recebido:")
        self.input_dinheiro = QLineEdit()
        self.input_dinheiro.setValidator(QDoubleValidator(0.0, 100000.0, 2))
        layout.addWidget(self.label_recebido)
        layout.addWidget(self.input_dinheiro)

        # Label troco
        self.label_troco = QLabel("Troco: R$ 0.00")
        layout.addWidget(self.label_troco)

        # Botão confirmar
        self.btn_confirmar = QPushButton("Confirmar Pagamento")
        layout.addWidget(self.btn_confirmar)

        self.setLayout(layout)

        # Conexões
        self.combo_pagamento.currentTextChanged.connect(self.on_metodo_pagamento_changed)
        self.btn_confirmar.clicked.connect(self.confirmar_pagamento)
        self.input_dinheiro.textChanged.connect(self.atualizar_troco)
        self.input_desconto.textChanged.connect(self.atualizar_total_com_desconto)

        # Inicializa
        self.on_metodo_pagamento_changed(self.combo_pagamento.currentText())

    def on_metodo_pagamento_changed(self, metodo):
        if metodo == "Dinheiro":
            self.label_recebido.setVisible(True)
            self.input_dinheiro.setVisible(True)
            self.input_dinheiro.setEnabled(True)
            self.input_dinheiro.clear()
            self.label_troco.setText("Troco: R$ 0.00")
        else:
            self.label_recebido.setVisible(False)
            self.input_dinheiro.setVisible(False)
            self.label_troco.setText("Troco: R$ 0.00")

    def atualizar_troco(self):
        if self.combo_pagamento.currentText() != "Dinheiro":
            return

        texto_valor = self.input_dinheiro.text().replace(",", ".").replace("R$", "").strip()
        try:
            valor_recebido = float(texto_valor)
            troco = valor_recebido - self.total_com_desconto
            if troco < 0:
                troco = 0.0
            self.label_troco.setText(f"Troco: R$ {troco:.2f}")
        except ValueError:
            self.label_troco.setText("Troco: R$ 0.00")

    def atualizar_total_com_desconto(self):
        texto_desconto = self.input_desconto.text().replace(",", ".").strip()

        if not texto_desconto:
            self.total_com_desconto = self.total
            self.label_total.setText(f"Total a pagar: R$ {self.total:.2f}")
            return

        try:
            if "%" in texto_desconto:
                percentual = float(texto_desconto.replace("%", "").strip())
                desconto = self.total * (percentual / 100)
            else:
                desconto = float(texto_desconto)
            self.total_com_desconto = self.total - desconto
            if self.total_com_desconto < 0:
                self.total_com_desconto = 0
            self.label_total.setText(f"Total a pagar: R$ {self.total_com_desconto:.2f}")
        except ValueError:
            self.label_total.setText(f"Total a pagar: R$ {self.total:.2f}")

    def confirmar_pagamento(self):
        metodo = self.combo_pagamento.currentText()

        if metodo == "Dinheiro":
            texto_valor = self.input_dinheiro.text().replace(",", ".").replace("R$", "").strip()
            if not texto_valor:
                QMessageBox.warning(self, "Erro", "Digite o valor recebido.")
                return
            try:
                valor_recebido = float(texto_valor)
                if valor_recebido < self.total_com_desconto:
                    QMessageBox.warning(self, "Valor insuficiente", "O valor recebido é menor que o total da venda.")
                    return
            except ValueError:
                QMessageBox.warning(self, "Erro", "Digite um valor válido.")
                return

        self.metodo = metodo
        self.accept()


class TelaVendas(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tela de Vendas - Show das Galáxias")
        self.setFixedSize(1000, 500)

        self.conn = sqlite3.connect("banco_dados.db")
        self.cursor = self.conn.cursor()

        self.total = 0.0

        self.layout_principal = QHBoxLayout()
        self.layout_esquerdo = QVBoxLayout()

        self.titulo = QLabel("VENDA DE PRODUTOS")
        self.titulo.setFont(QFont("Arial", 18, QFont.Bold))
        self.titulo.setStyleSheet("color: red; background-color: navy; padding: 10px; border-radius: 10px;")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.layout_esquerdo.addWidget(self.titulo)

        layout_input = QHBoxLayout()
        self.input_nome = QLineEdit()
        self.input_nome.setPlaceholderText("Digite o descricao ou descrição do produto")
        self.input_nome.setStyleSheet("padding: 5px; font-size: 14px; border: 2px solid navy; border-radius: 8px;")
        self.input_quantidade = QLineEdit()
        self.input_quantidade.setPlaceholderText("Quantidade")
        self.input_quantidade.setStyleSheet("padding: 5px; font-size: 14px; border: 2px solid navy; border-radius: 8px;")
        layout_input.addWidget(self.input_nome)
        layout_input.addWidget(self.input_quantidade)
        self.layout_esquerdo.addLayout(layout_input)

        self.btn_adicionar = QPushButton("Adicionar Item")
        self.btn_adicionar.setStyleSheet("background-color: red; color: white; padding: 10px; font-weight: bold; border-radius: 10px;")
        self.btn_adicionar.clicked.connect(self.adicionar_item)
        self.layout_esquerdo.addWidget(self.btn_adicionar)

        self.tabela_venda = QTableWidget()
        self.tabela_venda.setColumnCount(4)
        self.tabela_venda.setHorizontalHeaderLabels(["Produto", "Qtd", "Preço Unit.", "Total"])
        self.layout_esquerdo.addWidget(self.tabela_venda)

        self.label_total = QLabel("Total: R$ 0.00")
        self.label_total.setFont(QFont("Arial", 14, QFont.Bold))
        self.label_total.setStyleSheet("color: navy;")
        self.layout_esquerdo.addWidget(self.label_total)

        self.btn_finalizar = QPushButton("Finalizar Venda")
        self.btn_finalizar.setStyleSheet("background-color: navy; color: white; padding: 10px; font-weight: bold; border-radius: 10px;")
        self.btn_finalizar.clicked.connect(self.finalizar_venda)
        self.layout_esquerdo.addWidget(self.btn_finalizar)

        self.layout_direito = QVBoxLayout()
        self.label_lista = QLabel("PRODUTOS DISPONÍVEIS")
        self.label_lista.setFont(QFont("Arial", 14, QFont.Bold))
        self.label_lista.setAlignment(Qt.AlignCenter)
        self.layout_direito.addWidget(self.label_lista)

        self.tabela_produtos = QTableWidget()
        self.tabela_produtos.setColumnCount(2)
        self.tabela_produtos.setHorizontalHeaderLabels(["Produto", "Preço"])
        self.tabela_produtos.setEditTriggers(QTableWidget.NoEditTriggers)
        self.layout_direito.addWidget(self.tabela_produtos)

        self.carregar_produtos()
        self.preparar_autocompletar()

        self.layout_principal.addLayout(self.layout_esquerdo, 2)
        self.layout_principal.addLayout(self.layout_direito, 1)
        self.setLayout(self.layout_principal)

    def carregar_produtos(self):
        self.cursor.execute("SELECT descricao, preco_venda, estoque FROM produtos")
        produtos = self.cursor.fetchall()
        self.tabela_produtos.setRowCount(0)
        self.tabela_produtos.setColumnCount(3)
        self.tabela_produtos.setHorizontalHeaderLabels(["Descrição", "Preço", "Estoque"])

        for linha, (descricao, preco, estoque) in enumerate(produtos):
            self.tabela_produtos.insertRow(linha)
            self.tabela_produtos.setItem(linha, 0, QTableWidgetItem(descricao))
            self.tabela_produtos.setItem(linha, 1, QTableWidgetItem(f"R$ {preco:.2f}"))
            self.tabela_produtos.setItem(linha, 2, QTableWidgetItem(str(estoque)))
            
            item_estoque = QTableWidgetItem(str(estoque))
            # Se o estoque for menor que 5, pintar de vermelho
            if estoque < 5:
                item_estoque.setBackground(QColor("#d32f2f"))   # vermelho
                item_estoque.setForeground(QColor("white"))     # texto branco

            self.tabela_produtos.setItem(linha, 2, item_estoque)

    def preparar_autocompletar(self):
        self.cursor.execute("SELECT descricao, descricao FROM produtos")
        resultados = self.cursor.fetchall()
        sugestoes = []
        for descricao, descricao in resultados:
            sugestoes.append(descricao)
            if descricao:
                sugestoes.append(descricao)
        completer = QCompleter(sugestoes)
        completer.setCaseSensitivity(False)
        self.input_nome.setCompleter(completer)

    def adicionar_item(self):
        nome_ou_descricao = self.input_nome.text().strip()
        try:
            quantidade = int(self.input_quantidade.text())
        except ValueError:
            QMessageBox.warning(self, "Erro", "Digite uma quantidade válida.")
            return

        if not nome_ou_descricao:
            QMessageBox.warning(self, "Erro", "Digite a descrição do produto.")
            return

        self.cursor.execute("""
            SELECT descricao, preco_venda, estoque FROM produtos 
            WHERE descricao LIKE ? OR descricao LIKE ?
        """, (f"%{nome_ou_descricao}%", f"%{nome_ou_descricao}%"))
        resultado = self.cursor.fetchone()

        if resultado:
            descricao, preco_unit, estoque_disponivel = resultado

            if estoque_disponivel <= 0:
                QMessageBox.warning(self, "Estoque Zerado",
                                    f"O produto '{descricao}' está com estoque zerado.")
                return

            if quantidade > estoque_disponivel:
                QMessageBox.warning(self, "Estoque Insuficiente",
                                    f"Estoque disponível para '{descricao}': {estoque_disponivel}\n"
                                    f"Quantidade solicitada: {quantidade}")
                return

            # Tudo certo, agora pode calcular e adicionar
            total_item = preco_unit * quantidade

            linha = self.tabela_venda.rowCount()
            self.tabela_venda.insertRow(linha)
            self.tabela_venda.setItem(linha, 0, QTableWidgetItem(descricao))
            self.tabela_venda.setItem(linha, 1, QTableWidgetItem(str(quantidade)))
            self.tabela_venda.setItem(linha, 2, QTableWidgetItem(f"R$ {preco_unit:.2f}"))
            self.tabela_venda.setItem(linha, 3, QTableWidgetItem(f"R$ {total_item:.2f}"))

            self.total += total_item
            self.label_total.setText(f"Total: R$ {self.total:.2f}")
            self.input_nome.clear()
            self.input_quantidade.clear()
        else:
            QMessageBox.warning(self, "Erro", "Produto não encontrado.")


    def finalizar_venda(self):
        if self.total == 0:
            QMessageBox.information(self, "Aviso", "Nenhum item adicionado à venda.")
            return

        dialog = PagamentoDialog(self.total)
        if dialog.exec_() == QDialog.Accepted:
            metodo = dialog.metodo
            data = QDateTime.currentDateTime().toString("yyyy-MM-dd")
            hora = QDateTime.currentDateTime().toString("HH:mm:ss")

            self.cursor.execute("""
                INSERT INTO vendas (data, hora, total, forma_pagamento)
                VALUES (?, ?, ?, ?)
            """, (data, hora, self.total, metodo))
            id_venda = self.cursor.lastrowid

            for row in range(self.tabela_venda.rowCount()):
                descricao = self.tabela_venda.item(row, 0).text()
                qtd = int(self.tabela_venda.item(row, 1).text())
                preco_unit = float(self.tabela_venda.item(row, 2).text().replace("R$", "").strip())
                
                self.cursor.execute("SELECT id, estoque FROM produtos WHERE descricao = ?", (descricao,))
                resultado = self.cursor.fetchone()

                if resultado:
                    produto_id, estoque_atual = resultado

                    if qtd > estoque_atual:
                        QMessageBox.warning(self, "Estoque insuficiente",
                            f"O produto '{descricao}' possui apenas {estoque_atual} unidade(s) em estoque.\n"
                            f"Tente reduzir a quantidade ou reponha o estoque.")
                        self.conn.rollback()
                        return

                    # Atualiza o estoque
                    novo_estoque = estoque_atual - qtd
                    self.cursor.execute("""
                        UPDATE produtos SET estoque = ? WHERE id = ?
                    """, (novo_estoque, produto_id))


                    # Salva item da venda
                    self.cursor.execute("""
                        INSERT INTO itens_venda (venda_id, produto_id, quantidade, preco_unit)
                        VALUES (?, ?, ?, ?)
                    """, (id_venda, produto_id, qtd, preco_unit))

            self.conn.commit()
            QMessageBox.information(self, "Venda Concluída",
                                    f"Venda finalizada com sucesso!\nTotal: R$ {self.total:.2f}\nPagamento: {metodo}")
            self.tabela_venda.setRowCount(0)
            self.total = 0.0
            self.label_total.setText("Total: R$ 0.00")
            self.carregar_produtos()  # ← ATUALIZA A LISTA DE PRODUTOS COM ESTOQUE NOVO


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TelaVendas()
    window.show()
    sys.exit(app.exec_())
