import sqlite3
import os
import csv  # Adicionando a importação do módulo csv
from PyQt5.QtWidgets import (
    QDialog, QLabel, QTableWidget, QTableWidgetItem, QPushButton,
    QVBoxLayout, QHBoxLayout, QGridLayout, QLineEdit, QDateEdit, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from fpdf import FPDF  # Importando fpdf para gerar PDFs

class HistoricoVendas(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Histórico de Vendas")
        self.setFixedSize(1080, 550)
        self.setStyleSheet("background-color: #0073a6; color: white;")
        self.conn = sqlite3.connect("banco_dados.db")
        self.cursor = self.conn.cursor()

        self.layout = QGridLayout(self)

        # Filtros de data e cliente
        self.date_de = QDateEdit(calendarPopup=True)
        self.date_de.setDate(QDate.currentDate())
        self.date_de.setStyleSheet("color: black;")

        self.date_ate = QDateEdit(calendarPopup=True)
        self.date_ate.setDate(QDate.currentDate())
        self.date_ate.setStyleSheet("color: black;")

        self.filtro_cliente = QLineEdit()
        self.filtro_cliente.setPlaceholderText("Filtrar por cliente")
        self.filtro_cliente.setStyleSheet("color: black;")

        self.botao_filtrar = QPushButton("Filtrar")
        self.botao_filtrar.clicked.connect(self.carregar_dados)

        self.botao_exportar_pdf = QPushButton("Exportar PDF")
        self.botao_exportar_pdf.clicked.connect(self.exportar_pdf)

        self.botao_exportar_csv = QPushButton("Exportar CSV")
        self.botao_exportar_csv.clicked.connect(self.exportar_csv)

        botoes_exportar_layout = QHBoxLayout()
        botoes_exportar_layout.addWidget(self.botao_exportar_pdf)
        botoes_exportar_layout.addWidget(self.botao_exportar_csv)

        self.layout.addLayout(botoes_exportar_layout, 3, 0)

        # Inicializando a tabela de vendas antes de conectar o sinal
        self.tabela = QTableWidget(0, 7)
        self.tabela.setHorizontalHeaderLabels([
            "ID", "DATA", "CLIENTE", "TOTAL", "DESCONTO", "TOTAL COM DESCONTO", "FORMA DE PAGAMENTO"
        ])
        self.tabela.setStyleSheet("background-color: white; color: black; font-weight: bold;")
        self.tabela.horizontalHeader().setStretchLastSection(True)
        self.tabela.cellDoubleClicked.connect(self.abrir_detalhes_venda)

        filtro_layout = QHBoxLayout()
        filtro_layout.addWidget(QLabel("De:"))
        filtro_layout.addWidget(self.date_de)
        filtro_layout.addWidget(QLabel("Até:"))
        filtro_layout.addWidget(self.date_ate)
        filtro_layout.addWidget(self.filtro_cliente)
        filtro_layout.addWidget(self.botao_filtrar)

        # Tabela de vendas
        self.layout.addLayout(filtro_layout, 0, 0)
        self.layout.addWidget(self.tabela, 1, 0)

        self.total_label = QLabel("Total: R$ 0,00")
        self.total_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.total_label.setStyleSheet("padding: 5px; background-color: #005b85;")
        self.layout.addWidget(self.total_label, 2, 0)

        # Botão de exportar CSV
        self.botao_exportar = QPushButton("Exportar para CSV")
        self.botao_exportar.clicked.connect(self.exportar_csv)
        self.layout.addWidget(self.botao_exportar, 3, 0)

        self.botao_cancelar = QPushButton("Cancelar Venda Selecionada")
        self.botao_cancelar.clicked.connect(self.cancelar_venda)
        self.layout.addWidget(self.botao_cancelar, 5, 0)

        self.carregar_dados()  # Carregar os dados ao iniciar

    def carregar_dados(self):
        data_de = self.date_de.date().toString("yyyy-MM-dd")
        data_ate = self.date_ate.date().toString("yyyy-MM-dd")
        cliente_filtro = self.filtro_cliente.text().strip()

        query = """
            SELECT v.id, v.data, c.descricao, v.total, v.desconto, v.total_com_desconto, v.forma_pagamento
            FROM vendas v
            LEFT JOIN clientes c ON v.cliente_id = c.id
            WHERE v.data BETWEEN ? AND ?
        """

        params = [data_de, data_ate]

        if cliente_filtro:
            query += " AND c.descricao LIKE ?"
            params.append(f"%{cliente_filtro}%")

        self.cursor.execute(query, params)
        resultados = self.cursor.fetchall()

        self.tabela.setRowCount(0)
        total_vendas = 0
        total_com_desconto = 0

        for linha, row in enumerate(resultados):
            self.tabela.insertRow(linha)
            for col, item in enumerate(row):
                if isinstance(item, float):
                    valor = f"R$ {item:.2f}".replace(".", ",")
                else:
                    valor = str(item) if item is not None else ""
                self.tabela.setItem(linha, col, QTableWidgetItem(valor))
            total_vendas += row[3] or 0  # total
            total_com_desconto += row[5] or 0  # total com desconto

        self.total_label.setText(f"Total: R$ {total_vendas:.2f} | Total com Desconto: R$ {total_com_desconto:.2f}".replace(".", ","))

    def exportar_csv(self):
        caminho, _ = QFileDialog.getSaveFileName(self, "Salvar CSV", "", "CSV Files (*.csv)")
        if not caminho:
            return

        with open(caminho, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            headers = [self.tabela.horizontalHeaderItem(i).text() for i in range(self.tabela.columnCount())]
            writer.writerow(headers)
            for row in range(self.tabela.rowCount()):
                linha = [self.tabela.item(row, col).text() for col in range(self.tabela.columnCount())]
                writer.writerow(linha)

    def exportar_pdf(self):
        caminho, _ = QFileDialog.getSaveFileName(self, "Salvar PDF", "", "PDF Files (*.pdf)")
        if not caminho:
            return

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=10)

        colunas = [self.tabela.horizontalHeaderItem(i).text() for i in range(self.tabela.columnCount())]
        pdf.cell(200, 10, "Histórico de Vendas", ln=True, align='C')
        for col in colunas:
            pdf.cell(30, 8, col, border=1)
        pdf.ln()

        for row in range(self.tabela.rowCount()):
            for col in range(self.tabela.columnCount()):
                texto = self.tabela.item(row, col).text()
                pdf.cell(30, 8, texto, border=1)
            pdf.ln()

        pdf.output(caminho)

    def abrir_detalhes_venda(self, row, column):
        id_venda = self.tabela.item(row, 0).text()

        query = """
            SELECT v.id, v.data, v.hora, 
                COALESCE(c.nome, c.descricao, 'Não informado') AS cliente, 
                v.total, 
                COALESCE(v.desconto, 0), 
                COALESCE(v.total_com_desconto, v.total), 
                v.forma_pagamento, 
                COALESCE(v.observacoes, '')
            FROM vendas v
            LEFT JOIN clientes c ON c.id = v.cliente_id
            WHERE v.id = ?
        """
        self.cursor.execute(query, (id_venda,))
        venda = self.cursor.fetchone()

        if venda:
            id_venda, data, hora, cliente, total, desconto, total_com_desc, pagamento, obs = venda

            detalhes = (
                f"ID: {id_venda}\n"
                f"Data: {data} {hora}\n"
                f"Cliente: {cliente}\n"
                f"Total: R$ {total:.2f}\n"
                f"Desconto: R$ {desconto:.2f}\n"
                f"Total com Desconto: R$ {total_com_desc:.2f}\n"
                f"Pagamento: {pagamento}\n"
                f"Observações: {obs}"
            )
            QMessageBox.information(self, "Detalhes da Venda", detalhes)

    def cancelar_venda(self):
        # Verifica se a conexão com o banco de dados está ativa
        if not self.conn:
            QMessageBox.critical(self, "Erro", "Falha na conexão com o banco de dados.")
            return

        linha = self.tabela.currentRow()
        if linha == -1:
            QMessageBox.warning(self, "Aviso", "Selecione uma venda para cancelar.")
            return

        id_venda = int(self.tabela.item(linha, 0).text())

        resposta = QMessageBox.question(self, "Cancelar Venda",
            f"Tem certeza que deseja cancelar a venda ID {id_venda}?\nIsso irá estornar o estoque dos produtos.",
            QMessageBox.Yes | QMessageBox.No)

        if resposta == QMessageBox.Yes:
            try:
                # Verificar se já foi cancelada
                self.cursor.execute("SELECT cancelada FROM vendas WHERE id = ?", (id_venda,))
                status = self.cursor.fetchone()
                if status and status[0] == 1:
                    QMessageBox.information(self, "Aviso", "Essa venda já foi cancelada.")
                    return

                # Marcar venda como cancelada
                self.cursor.execute("UPDATE vendas SET cancelada = 1 WHERE id = ?", (id_venda,))

                # Recuperar os itens da venda
                self.cursor.execute("SELECT produto_id, quantidade FROM itens_venda WHERE venda_id = ?", (id_venda,))
                itens = self.cursor.fetchall()

                # Estornar o estoque
                for produto_id, quantidade in itens:
                    self.cursor.execute("UPDATE produtos SET estoque = estoque + ? WHERE id = ?", (quantidade, produto_id))

                self.conn.commit()

                # Mensagem de sucesso após a exclusão
                QMessageBox.information(self, "Sucesso", f"Venda ID {id_venda} cancelada e estoque estornado.")

                # Marcar a linha da venda como vermelha na tabela
                for col in range(self.tabela.columnCount()):
                    item = self.tabela.item(linha, col)
                    if item:
                        item.setBackground(Qt.red)  # Marca toda a linha de vermelho

                # Atualiza a tabela de vendas para refletir as mudanças
                self.carregar_dados()  # Recarrega os dados da tabela
                self.tabela.setRowColor(linha, Qt.red)  # Atualiza a cor da linha explicitamente

            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao cancelar venda: {str(e)}")
                self.conn.rollback()



