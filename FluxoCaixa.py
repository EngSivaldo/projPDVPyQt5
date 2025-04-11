from PyQt5.QtWidgets import (
    QDialog, QLabel, QTableWidget, QTableWidgetItem, QPushButton,
    QVBoxLayout, QHBoxLayout, QComboBox, QDateEdit, QGridLayout
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
import sqlite3

class FluxoCaixa(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fluxo de Caixa")
        self.setFixedSize(1080, 550)
        self.setStyleSheet("background-color: #0073a6; color: white;")

        self.layout = QGridLayout(self)

        # TABELA MENSAL
        self.tabela_mes = QTableWidget(12, 4)
        self.tabela_mes.setHorizontalHeaderLabels(["TOTAL", "DESCONTO", "SUBTOTAL", "LUCRO"])
        self.tabela_mes.setVerticalHeaderLabels([
            "JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO",
            "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"
        ])
        self.tabela_mes.setStyleSheet("background-color: white; color: black; font-weight: bold;")

        self.total_mes_label = QLabel("Total =    00,00       00,00       00,00       00,00")
        self.total_mes_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.total_mes_label.setStyleSheet("padding: 5px; background-color: #005b85;")

        ano_layout = QHBoxLayout()
        self.combo_ano = QComboBox()
        self.combo_ano.setStyleSheet("color: black;")
        self.combo_ano.addItems([str(ano) for ano in range(2020, 2031)])
        self.botao_atualizar_ano = QPushButton("Atualizar")
        self.botao_atualizar_ano.clicked.connect(self.carregar_dados_mes)
        ano_layout.addWidget(QLabel("Atualize o Ano"))
        ano_layout.addWidget(self.combo_ano)
        ano_layout.addWidget(self.botao_atualizar_ano)

        # TABELA DIÁRIA
        self.tabela_dia = QTableWidget(0, 3)
        self.tabela_dia.setHorizontalHeaderLabels(["VALOR VENDAS", "FORMA DE PGTO", "LUCRO"])
        self.tabela_dia.setStyleSheet("background-color: white; color: black; font-weight: bold;")

        self.total_dia_label = QLabel("00,00                     00,00")
        self.total_dia_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.total_dia_label.setStyleSheet("padding: 5px; background-color: #005b85;")

        data_layout = QHBoxLayout()
        self.date_edit = QDateEdit(calendarPopup=True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setStyleSheet("color: black;")
        self.botao_atualizar_data = QPushButton("Atualizar")
        self.botao_atualizar_data.clicked.connect(self.carregar_dados_dia)
        data_layout.addWidget(QLabel("Atualize a Data"))
        data_layout.addWidget(self.date_edit)
        data_layout.addWidget(self.botao_atualizar_data)

        # ADICIONAR AO LAYOUT
        self.layout.addWidget(QLabel("VENDAS - MÊS"), 0, 0)
        self.layout.addWidget(self.tabela_mes, 1, 0)
        self.layout.addWidget(self.total_mes_label, 2, 0)
        self.layout.addLayout(ano_layout, 3, 0)

        self.layout.addWidget(QLabel("VENDAS - DIAS"), 0, 1)
        self.layout.addWidget(self.tabela_dia, 1, 1)
        self.layout.addWidget(self.total_dia_label, 2, 1)
        self.layout.addLayout(data_layout, 3, 1)

        self.carregar_dados_mes()
        self.carregar_dados_dia()

    def carregar_dados_mes(self):
        ano = self.combo_ano.currentText()
        dados_mes = [[0, 0, 0, 0] for _ in range(12)]

        con = sqlite3.connect("banco_dados.db")
        cursor = con.cursor()
        try:
            cursor.execute("SELECT data_venda, total, desconto, subtotal, lucro FROM vendas")
            for data, total, desconto, subtotal, lucro in cursor.fetchall():
                if data.startswith(ano):
                    mes = int(data[5:7]) - 1
                    dados_mes[mes][0] += total
                    dados_mes[mes][1] += desconto
                    dados_mes[mes][2] += subtotal
                    dados_mes[mes][3] += lucro
        except sqlite3.OperationalError as e:
            print("Erro ao carregar dados mensais:", e)
        finally:
            con.close()

        total_geral = [0, 0, 0, 0]
        for i in range(12):
            for j in range(4):
                valor = f"{dados_mes[i][j]:.2f}".replace(".", ",")
                self.tabela_mes.setItem(i, j, QTableWidgetItem(valor))
                total_geral[j] += dados_mes[i][j]

        total_str = "Total =    " + "       ".join(f"{t:.2f}".replace(".", ",") for t in total_geral)
        self.total_mes_label.setText(total_str)

    def carregar_dados_dia(self):
        data = self.date_edit.date().toString("yyyy-MM-dd")

        con = sqlite3.connect("banco_dados.db")
        cursor = con.cursor()
        try:
            cursor.execute("SELECT total, forma_pagamento, lucro FROM vendas WHERE data_venda = ?", (data,))
            resultados = cursor.fetchall()
        except sqlite3.OperationalError as e:
            print("Erro ao carregar dados diários:", e)
            resultados = []
        finally:
            con.close()

        self.tabela_dia.setRowCount(0)
        total_vendas = 0
        total_lucro = 0

        for linha, (total, forma_pagamento, lucro) in enumerate(resultados):
            self.tabela_dia.insertRow(linha)
            self.tabela_dia.setItem(linha, 0, QTableWidgetItem(f"{total:.2f}".replace(".", ",")))
            self.tabela_dia.setItem(linha, 1, QTableWidgetItem(forma_pagamento))
            self.tabela_dia.setItem(linha, 2, QTableWidgetItem(f"{lucro:.2f}".replace(".", ",")))
            total_vendas += total
            total_lucro += lucro

        total_dia_str = f"{total_vendas:.2f}".replace(".", ",") + "                     " + f"{total_lucro:.2f}".replace(".", ",")
        self.total_dia_label.setText(total_dia_str)
