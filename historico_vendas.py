from PyQt5.QtWidgets import (
    QDialog, QLabel, QTableWidget, QTableWidgetItem, QPushButton,
    QVBoxLayout, QHBoxLayout, QGridLayout, QLineEdit, QDateEdit
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
import sqlite3
import os

class HistoricoVendas(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Histórico de Vendas")
        self.setFixedSize(1080, 550)
        self.setStyleSheet("background-color: #0073a6; color: white;")

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

        filtro_layout = QHBoxLayout()
        filtro_layout.addWidget(QLabel("De:"))
        filtro_layout.addWidget(self.date_de)
        filtro_layout.addWidget(QLabel("Até:"))
        filtro_layout.addWidget(self.date_ate)
        filtro_layout.addWidget(self.filtro_cliente)
        filtro_layout.addWidget(self.botao_filtrar)

        # Tabela de vendas
        self.tabela = QTableWidget(0, 6)
        self.tabela.setHorizontalHeaderLabels([
            "ID", "DATA", "CLIENTE", "TOTAL", "DESCONTO", "FORMA DE PAGAMENTO"
        ])
        self.tabela.setStyleSheet("background-color: white; color: black; font-weight: bold;")
        self.tabela.horizontalHeader().setStretchLastSection(True)

        self.total_label = QLabel("Total: R$ 0,00")
        self.total_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.total_label.setStyleSheet("padding: 5px; background-color: #005b85;")

        self.layout.addLayout(filtro_layout, 0, 0)
        self.layout.addWidget(self.tabela, 1, 0)
        self.layout.addWidget(self.total_label, 2, 0)

        self.carregar_dados()

    def carregar_dados(self):
        data_de = self.date_de.date().toString("yyyy-MM-dd")
        data_ate = self.date_ate.date().toString("yyyy-MM-dd")
        cliente_filtro = self.filtro_cliente.text().strip()

        # Caminho do banco
        caminho_db = os.path.join(os.path.dirname(__file__), "banco_dados.db")
        con = sqlite3.connect(caminho_db)
        cur = con.cursor()

        # Consulta com join para buscar descricao do cliente
        query = """
            SELECT v.id, v.data, c.descricao, v.total, v.desconto, v.forma_pagamento
            FROM vendas v
            LEFT JOIN clientes c ON v.cliente_id = c.id
            WHERE v.data BETWEEN ? AND ?
        """
        params = [data_de, data_ate]

        if cliente_filtro:
            query += " AND c.descricao LIKE ?"
            params.append(f"%{cliente_filtro}%")

        cur.execute(query, params)
        resultados = cur.fetchall()
        con.close()

        self.tabela.setRowCount(0)
        total_vendas = 0

        for linha, row in enumerate(resultados):
            self.tabela.insertRow(linha)
            for col, item in enumerate(row):
                if isinstance(item, float):
                    valor = f"R$ {item:.2f}".replace(".", ",")
                else:
                    valor = str(item) if item is not None else ""
                self.tabela.setItem(linha, col, QTableWidgetItem(valor))
            total_vendas += row[3] or 0  # total

        self.total_label.setText(f"Total: R$ {total_vendas:.2f}".replace(".", ","))

