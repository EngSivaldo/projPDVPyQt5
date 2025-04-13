from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QFrame
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtGui import QTextDocument
from PyQt5.QtCore import Qt

class TelaRecibo(QDialog):
    def __init__(self, dados_venda, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Recibo da Venda")
        self.resize(400, 600)
        self.dados_venda = dados_venda

        layout = QVBoxLayout()

        # Moldura para o recibo
        moldura = QFrame()
        moldura.setFrameShape(QFrame.Box)
        moldura.setLineWidth(2)
        moldura.setStyleSheet("QFrame { border: 2px solid #555; border-radius: 10px; padding: 10px; background-color: #fdfdfd; }")
        
        recibo_layout = QVBoxLayout(moldura)
        self.recibo_texto = QLabel(self.gerar_texto_recibo())
        self.recibo_texto.setAlignment(Qt.AlignTop)
        self.recibo_texto.setStyleSheet("font-family: Courier; font-size: 14px;")
        self.recibo_texto.setWordWrap(True)
        recibo_layout.addWidget(self.recibo_texto)

        layout.addWidget(moldura)

        # Botão de imprimir
        btn_imprimir = QPushButton("Imprimir Recibo")
        btn_imprimir.clicked.connect(self.imprimir_recibo)
        btn_imprimir.setStyleSheet("QPushButton { background-color: #d32f2f; color: white; font-weight: bold; padding: 10px; border-radius: 5px; } QPushButton:hover { background-color: #b71c1c; }")
        layout.addWidget(btn_imprimir)

        self.setLayout(layout)

    def gerar_texto_recibo(self):
        total_bruto = self.dados_venda.get('total_bruto', self.dados_venda['total'])
        desconto = self.dados_venda.get('desconto', 0.0)
        total_final = self.dados_venda['total']

        porcentagem_desconto = (desconto / total_bruto * 100) if total_bruto > 0 else 0.0

        texto = f"***** RECIBO DE VENDA *****\n\n"
        texto += f"Data: {self.dados_venda['data']} {self.dados_venda['hora']}\n"
        texto += f"Forma de Pagamento: {self.dados_venda['metodo']}\n"
        texto += "\nItens:\n"

        for item in self.dados_venda['itens']:
            texto += f"{item['descricao']} - {item['quantidade']} x R${item['preco_unit']:.2f}\n"

        texto += f"\nTotal Bruto: R$ {total_bruto:.2f}"
        texto += f"\nDesconto: R$ {desconto:.2f} ({porcentagem_desconto:.1f}%)"
        texto += f"\nTOTAL FINAL: R$ {total_final:.2f}\n"

        texto += "\nObrigado pela preferência!"
        return texto


    def imprimir_recibo(self):
        doc = QTextDocument()
        doc.setPlainText(self.recibo_texto.text())

        printer = QPrinter()
        dialog = QPrintDialog(printer, self)

        if dialog.exec_() == QPrintDialog.Accepted:
            doc.print_(printer)
