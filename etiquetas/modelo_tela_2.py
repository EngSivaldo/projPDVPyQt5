# gerar_etiquetas/modelo2_etiquetas.py
from PyQt5.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout,
    QGridLayout, QGroupBox, QComboBox, QSpinBox, QTableWidget, QTableWidgetItem, QWidget
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt


class TelaGerarEtiquetasModelo2(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editar Etiquetas - Modelo 2")
        self.setFixedSize(1000, 600)
        self.setStyleSheet("background-color: #0077b6; color: white; font-family: Arial;")

        layout = QGridLayout()

        # Coluna da Esquerda - Campos
        form_layout = QVBoxLayout()

        campos = [
            ("Etiqueta Linha 1", QLineEdit()),
            ("Etiqueta Linha 2", QLineEdit()),
            ("Etiqueta Linha 3", QLineEdit()),
            ("Etiqueta Linha 4", QLineEdit()),
            ("Etiqueta Linha 5", QLineEdit()),
            ("Código Produto", QLineEdit()),
        ]

        self.campos_inputs = {}

        for label_text, widget in campos:
            label = QLabel(label_text)
            label.setFont(QFont("Arial", 10, QFont.Bold))
            form_layout.addWidget(label)
            form_layout.addWidget(widget)
            self.campos_inputs[label_text] = widget

        # Botões abaixo dos campos
        botoes_layout = QHBoxLayout()
        btn_salvar = QPushButton("Salvar")
        btn_limpar = QPushButton("Limpar")
        btn_fechar = QPushButton("Fechar")

        for btn in [btn_salvar, btn_limpar, btn_fechar]:
            btn.setFixedWidth(100)
            botoes_layout.addWidget(btn)

        form_layout.addLayout(botoes_layout)

        # Adiciona form_layout à coluna 0
        layout.addLayout(form_layout, 0, 0)

        # Coluna da Direita - Visualização
        visual_layout = QVBoxLayout()

        titulo_preview = QLabel("Visualização da Etiqueta")
        titulo_preview.setFont(QFont("Arial", 12, QFont.Bold))
        titulo_preview.setAlignment(Qt.AlignCenter)
        visual_layout.addWidget(titulo_preview)

        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setStyleSheet("background-color: white; color: black; font-size: 12pt;")
        self.preview_text.setFixedSize(400, 300)
        visual_layout.addWidget(self.preview_text)

        atualizar_btn = QPushButton("Atualizar Visualização")
        atualizar_btn.clicked.connect(self.atualizar_visualizacao)
        visual_layout.addWidget(atualizar_btn)

        layout.addLayout(visual_layout, 0, 1)

        self.setLayout(layout)

    def atualizar_visualizacao(self):
        linhas = []
        for i in range(1, 6):
            texto = self.campos_inputs[f"Etiqueta Linha {i}"].text()
            linhas.append(texto)
        codigo = self.campos_inputs["Código Produto"].text()
        visual = "\n".join(linhas) + f"\n\nCódigo: {codigo}"
        self.preview_text.setPlainText(visual)
