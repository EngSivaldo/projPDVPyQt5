from PyQt5.QtWidgets import (
    QDialog, QLabel, QTableWidget, QTableWidgetItem, QPushButton,
    QVBoxLayout, QHBoxLayout, QComboBox, QDateEdit, QLineEdit,
    QRadioButton, QButtonGroup, QMessageBox
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QIcon
import sqlite3
import os

class ContasPagar(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Contas A Pagar")
        self.setFixedSize(1100, 580)
        self.setStyleSheet("background-color: #0d75a8; color: white;")

        self.layout = QVBoxLayout(self)

        # Filtros superiores
        filtros_layout = QHBoxLayout()

        self.radio_num = QRadioButton("Nº Documento")
        self.radio_forn = QRadioButton("Fornecedor")
        self.radio_desc = QRadioButton("Descrição")
        self.radio_num.setChecked(True)
        self.grupo_radio = QButtonGroup()
        for btn in [self.radio_num, self.radio_forn, self.radio_desc]:
            self.grupo_radio.addButton(btn)
            filtros_layout.addWidget(btn)

        self.campo_busca = QLineEdit()
        self.campo_busca.returnPressed.connect(self.buscar_registros)
        filtros_layout.addWidget(self.campo_busca)

        self.combo_data = QComboBox()
        self.combo_data.addItems(["Data Vencimento", "Data Cadastro"])
        filtros_layout.addWidget(self.combo_data)

        self.data_inicio = QDateEdit(calendarPopup=True)
        self.data_inicio.setDate(QDate.currentDate())
        filtros_layout.addWidget(self.data_inicio)
        filtros_layout.addWidget(QLabel("Até"))

        self.data_fim = QDateEdit(calendarPopup=True)
        self.data_fim.setDate(QDate.currentDate())
        filtros_layout.addWidget(self.data_fim)

        self.combo_status = QComboBox()
        self.combo_status.addItems(["", "PENDENTE", "PAGO"])
        filtros_layout.addWidget(self.combo_status)

        self.layout.addLayout(filtros_layout)

        # Tabela principal
        self.tabela = QTableWidget(0, 9)
        self.tabela.setHorizontalHeaderLabels([
            "Código", "Descrição", "Valor", "Data Cad", "Fornecedor",
            "Tipo", "Vencimento", "Valor Pago", "Status"
        ])
        self.tabela.setStyleSheet("background-color: white; color: black; font-weight: bold;")
        self.layout.addWidget(self.tabela)

        # Totais
        totais_layout = QHBoxLayout()
        self.label_total = QLabel("R$ 0,00")
        self.label_pago = QLabel("R$ 0,00")
        self.label_apagar = QLabel("R$ 0,00")
        for lbl in [self.label_total, self.label_pago, self.label_apagar]:
            lbl.setFont(QFont("Arial", 16, QFont.Bold))
            lbl.setFixedSize(180, 80)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet("background-color: #0073a6; color: white; border: 2px solid white;")
        totais_layout.addWidget(self.label_total)
        totais_layout.addWidget(self.label_pago)
        totais_layout.addWidget(self.label_apagar)
        self.layout.addLayout(totais_layout)

        # Botões inferiores
        botoes_layout = QHBoxLayout()

        self.btn_adicionar = QPushButton("ADICIONAR / EDITAR")
        self.btn_pagar = QPushButton("PAGAR CONTA")
        self.btn_cancelar = QPushButton("CANCELAR")
        self.btn_relatorio = QPushButton("RELATÓRIO")

        for btn in [self.btn_adicionar, self.btn_pagar, self.btn_cancelar, self.btn_relatorio]:
            btn.setFixedHeight(60)
            btn.setStyleSheet("background-color: #005b85; font-weight: bold;")
            botoes_layout.addWidget(btn)

        self.layout.addLayout(botoes_layout)

        self.campo_busca.textChanged.connect(self.buscar_registros)
        self.combo_status.currentTextChanged.connect(self.buscar_registros)
        self.data_inicio.dateChanged.connect(self.buscar_registros)
        self.data_fim.dateChanged.connect(self.buscar_registros)
        self.combo_data.currentTextChanged.connect(self.buscar_registros)

        self.btn_pagar.clicked.connect(self.marcar_como_pago)

        self.buscar_registros()

    def buscar_registros(self):
        campo = self.campo_busca.text().strip().lower()
        tipo_filtro = self.grupo_radio.checkedButton().text()
        data_ini = self.data_inicio.date().toString("yyyy-MM-dd")
        data_fim = self.data_fim.date().toString("yyyy-MM-dd")
        campo_data = "vencimento" if self.combo_data.currentText() == "Data Vencimento" else "data_cadastro"
        status = self.combo_status.currentText()

        con = sqlite3.connect("banco_dados.db")
        cursor = con.cursor()

        query = f"SELECT * FROM contas_pagar WHERE date({campo_data}) BETWEEN ? AND ?"
        params = [data_ini, data_fim]

        if campo:
            if tipo_filtro == "Nº Documento":
                query += " AND CAST(id AS TEXT) LIKE ?"
            elif tipo_filtro == "Fornecedor":
                query += " AND LOWER(fornecedor) LIKE ?"
            else:
                query += " AND LOWER(descricao) LIKE ?"
            params.append(f"%{campo}%")

        if status:
            query += " AND status = ?"
            params.append(status)

        cursor.execute(query, params)
        resultados = cursor.fetchall()
        con.close()

        self.tabela.setRowCount(0)
        total = pago = apagar = 0

        for linha, dado in enumerate(resultados):
            self.tabela.insertRow(linha)
            for col, valor in enumerate(dado):
                item = QTableWidgetItem(str(valor))
                self.tabela.setItem(linha, col, item)
            total += dado[2]  # valor
            pago += dado[7]   # valor_pago
        apagar = total - pago

        self.label_total.setText(f"R$ {total:.2f}".replace(".", ","))
        self.label_pago.setText(f"R$ {pago:.2f}".replace(".", ","))
        self.label_apagar.setText(f"R$ {apagar:.2f}".replace(".", ","))

    def marcar_como_pago(self):
        linha = self.tabela.currentRow()
        if linha == -1:
            QMessageBox.warning(self, "Aviso", "Selecione uma conta para pagar.")
            return

        id_conta = self.tabela.item(linha, 0).text()
        valor = float(self.tabela.item(linha, 2).text().replace(",", "."))

        CAMINHO_DB = os.path.join(os.path.dirname(__file__), "banco_dados.db")
        con = sqlite3.connect(CAMINHO_DB)
        cursor = con.cursor()
        cursor.execute("UPDATE contas_pagar SET status = 'PAGO', valor_pago = ? WHERE id = ?", (valor, id_conta))
        con.commit()
        con.close()

        self.buscar_registros()
        QMessageBox.information(self, "Sucesso", "Conta marcada como PAGA com sucesso.")
