from PyQt5.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QDateEdit, QComboBox, QRadioButton,
    QButtonGroup, QGridLayout
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
import sqlite3

class ContasReceber(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Contas a Receber")
        self.setFixedSize(1160, 620)
        self.setStyleSheet("background-color: #0073a6; color: white;")
        self.layout = QVBoxLayout(self)

        # Filtros principais
        filtros_layout = QGridLayout()
        self.radio_cliente = QRadioButton("descricao Cliente")
        self.radio_venda = QRadioButton("Nº Venda")
        self.radio_cliente.setChecked(True)

        grupo_busca = QButtonGroup()
        grupo_busca.addButton(self.radio_cliente)
        grupo_busca.addButton(self.radio_venda)

        self.input_busca = QLineEdit()
        self.input_busca.setPlaceholderText("pressione F5 para abrir lista de clientes")
        self.combo_status = QComboBox()
        self.combo_status.addItems(["", "Aberto", "Pago", "Parcial"])
        self.combo_ordenar = QComboBox()
        self.combo_ordenar.addItems(["", "Data Venda", "Vencimento", "descricao Cliente"])

        self.data_inicio = QDateEdit(calendarPopup=True)
        self.data_inicio.setDate(QDate.currentDate())
        self.data_fim = QDateEdit(calendarPopup=True)
        self.data_fim.setDate(QDate.currentDate())

        self.combo_tipo_data = QComboBox()
        self.combo_tipo_data.addItems(["DATA VENDA", "VENCIMENTO", "PRÓXIMO PGTO"])

        self.botao_pesquisar = QPushButton("Pesquisar")
        self.botao_pesquisar.clicked.connect(self.buscar_contas)

        filtros_layout.addWidget(self.radio_cliente, 0, 0)
        filtros_layout.addWidget(self.radio_venda, 0, 1)
        filtros_layout.addWidget(self.input_busca, 1, 0, 1, 2)
        filtros_layout.addWidget(QLabel("Status"), 0, 2)
        filtros_layout.addWidget(self.combo_status, 1, 2)
        filtros_layout.addWidget(QLabel("Ordenar Por"), 0, 3)
        filtros_layout.addWidget(self.combo_ordenar, 1, 3)
        filtros_layout.addWidget(QLabel("Filtrar por Data"), 0, 4)
        filtros_layout.addWidget(self.data_inicio, 1, 4)
        filtros_layout.addWidget(QLabel("até"), 0, 5)
        filtros_layout.addWidget(self.data_fim, 1, 5)
        filtros_layout.addWidget(self.combo_tipo_data, 1, 6)
        filtros_layout.addWidget(self.botao_pesquisar, 1, 7)

        self.layout.addLayout(filtros_layout)

        # Tabela
        self.tabela = QTableWidget(0, 13)
        self.tabela.setHorizontalHeaderLabels([
            "Nº Venda", "descricao do Cliente", "Nº Parcelas", "Valor Parcela", "Dia Venc.",
            "Acréscimo", "Desconto", "Vlr Pago", "Restante", "Total", "Data Venda",
            "Próximo Pgto", "Status"
        ])
        self.tabela.setStyleSheet("background-color: white; color: black; font-weight: bold;")
        self.layout.addWidget(self.tabela)

        # Rodapé com totais
        self.label_total = QLabel("Total: R$ 0,00")
        self.label_pago = QLabel("Pago: R$ 0,00")
        self.label_apagar = QLabel("A Pagar: R$ 0,00")
        for lbl in (self.label_total, self.label_pago, self.label_apagar):
            lbl.setFont(QFont("Arial", 12, QFont.Bold))
            lbl.setStyleSheet("background-color: #005b85; padding: 10px;")

        rodape_layout = QHBoxLayout()
        rodape_layout.addWidget(self.label_total)
        rodape_layout.addWidget(self.label_pago)
        rodape_layout.addWidget(self.label_apagar)
        self.layout.addLayout(rodape_layout)

    def buscar_contas(self):
        modo_busca = "cliente" if self.radio_cliente.isChecked() else "venda"
        texto = self.input_busca.text().strip()
        status = self.combo_status.currentText()
        ordenar = self.combo_ordenar.currentText()
        tipo_data = self.combo_tipo_data.currentText()

        data_ini = self.data_inicio.date().toString("yyyy-MM-dd")
        data_fim = self.data_fim.date().toString("yyyy-MM-dd")

        query = """
            SELECT v.venda_id, c.descricao, v.parcelas, v.valor_parcela, v.vencimento,
                   v.acrescimo, v.desconto, v.valor_pago, v.restante, v.total,
                   v.data_venda, v.proximo_pagamento, v.status
            FROM contas_receber v
            LEFT JOIN clientes c ON v.cliente_id = c.id
            WHERE 1=1
        """
        params = []

        if texto:
            if modo_busca == "cliente":
                query += " AND c.descricao LIKE ?"
                params.append(f"%{texto}%")
            else:
                query += " AND v.venda_id = ?"
                params.append(texto)

        if status:
            query += " AND v.status = ?"
            params.append(status)

        campo_data = "v.data_venda" if tipo_data == "DATA VENDA" else "v.vencimento" if tipo_data == "VENCIMENTO" else "v.proximo_pagamento"
        query += f" AND {campo_data} BETWEEN ? AND ?"
        params.extend([data_ini, data_fim])

        if ordenar == "Data Venda":
            query += " ORDER BY v.data_venda DESC"
        elif ordenar == "Vencimento":
            query += " ORDER BY v.vencimento ASC"
        elif ordenar == "descricao Cliente":
            query += " ORDER BY c.descricao ASC"

        conn = sqlite3.connect("banco_dados.db")
        cur = conn.cursor()
        cur.execute(query, params)
        resultados = cur.fetchall()
        conn.close()

        # Preencher tabela
        self.tabela.setRowCount(0)
        total = pago = apagar = 0

        for i, linha in enumerate(resultados):
            self.tabela.insertRow(i)
            for j, valor in enumerate(linha):
                valor_str = f"{valor:.2f}".replace(".", ",") if isinstance(valor, float) else str(valor)
                self.tabela.setItem(i, j, QTableWidgetItem(valor_str))

            total += linha[9] or 0
            pago += linha[7] or 0
            apagar += linha[8] or 0

        self.label_total.setText(f"Total: R$ {total:.2f}".replace(".", ","))
        self.label_pago.setText(f"Pago: R$ {pago:.2f}".replace(".", ","))
        self.label_apagar.setText(f"A Pagar: R$ {apagar:.2f}".replace(".", ","))

