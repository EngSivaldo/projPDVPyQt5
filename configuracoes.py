from PyQt5.QtWidgets import (
    QDialog, QLabel, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout,
    QTabWidget, QWidget, QMessageBox, QGroupBox, QFormLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class TelaConfiguracoes(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuração")
        self.setFixedSize(850, 600)
        self.setStyleSheet("background-color: #0070C0; color: white; font-size: 13px;")

        layout = QVBoxLayout()

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: 0; }
            QTabBar::tab {
                background: #0F6CBF;
                padding: 10px 20px;
                font-weight: bold;
                color: white;
                border: 1px solid #0F6CBF;
            }
            QTabBar::tab:selected {
                background: orange;
                color: white;
            }
        """)
        self.tabs.addTab(self.criar_aba_geral(), "Geral")
        self.tabs.addTab(QWidget(), "Cupom Venda")
        self.tabs.addTab(QWidget(), "Teclas Atalho")
        self.tabs.addTab(QWidget(), "Balanças")
        self.tabs.addTab(QWidget(), "Configurar Backup")
        layout.addWidget(self.tabs)

        # Botões inferiores
        botoes = QHBoxLayout()

        video_btn = QPushButton("ver vídeo de ajuda\nsobre esta tela?")
        video_btn.setStyleSheet("background-color: red; color: white; padding: 10px; font-weight: bold;")
        video_btn.clicked.connect(self.mostrar_video)
        botoes.addWidget(video_btn)

        salvar_btn = QPushButton("SALVAR")
        salvar_btn.setStyleSheet("background-color: white; color: #0070C0; font-weight: bold; padding: 15px 30px;")
        salvar_btn.clicked.connect(self.salvar_configuracoes)
        botoes.addStretch()
        botoes.addWidget(salvar_btn)

        layout.addLayout(botoes)
        self.setLayout(layout)

    def criar_aba_geral(self):
        aba = QWidget()
        h_layout = QHBoxLayout()

        def combo(*itens):
            cb = QComboBox()
            cb.addItems(itens)
            cb.setStyleSheet("background-color: white; color: black;")
            return cb

        colunas = [QVBoxLayout() for _ in range(4)]

        campos = [
            # Coluna 1
            [("Modelo Tela PDV", combo("MODELO 1", "MODELO 2", "MODELO 3")),
             ("Número do Caixa:", combo("1", "2", "3", "4")),
             ("Buscar Atualização ao abrir", combo("Sempre Buscar", "Nunca Buscar")),
             ("Comissão Produtos", combo("Sobre o Preço", "Outro")),
             ("Mostrar Monitor Estoque", combo("SIM - MOSTRAR NA TELA", "NÃO")),
             ("Cor da Tela Login", combo("Custom...", "Azul", "Preto")),
             ("Aviso de Estoque Mínimo", combo("DESATIVADO", "ATIVADO")),
             ("Juros Venda Aprazo", combo("em real R$", "em porcentagem"))],

            # Coluna 2
            [("1°COR Tela Vendas", combo("Custom...", "Azul", "Verde")),
             ("Descontos Vendas", combo("em porcentagem", "em reais")),
             ("Leitor tela de vendas", combo("sempre ativo", "manual")),
             ("Calc. Pr Custo Add Estoque", combo("SIM - AUTOMATICO", "NÃO")),
             ("Perg. Finalizar Venda", combo("Sempre Perguntar", "Nunca")),
             ("Letra Listas Produtos", combo("dBlack", "Normal", "Grande")),
             ("Aviso Caixa Anterior aberto", combo("SIM - AVISAR", "NÃO"))],

            # Coluna 3
            [("2°COR Tela Vendas", combo("Preto", "Branco", "Cinza")),
             ("Vendas PDV Mesas", combo("Finalizar Modelo1", "Modelo2")),
             ("Gaveta de Dinheiro", combo("ABRIR APÓS CUPOM", "MANUAL")),
             ("Alterar Data Na Venda", combo("NÃO", "SIM")),
             ("Venda Cartão c/ Aprazo", combo("NÃO", "SIM")),
             ("Fundo Listas Produtos", combo("dWhite", "dGray", "dBlack")),
             ("Permitir Reabrir o Caixa", combo("SIM - PERGUNTAR", "NÃO"))],

            # Coluna 4
            [("Cores da Tela PDV", combo("Cores Padrão", "Preto e Branco")),
             ("Tela Cad Produtos", combo("MODELO 1", "MODELO 2")),
             ("Termo de Venda", combo("NÃO", "SIM")),
             ("Prefixo/sufixo Leitor", combo("NÃO", "SIM")),
             ("Troco em venda PIX", combo("DESATIVADO", "ATIVADO")),
             ("Calc. Lucro do Produto", combo("Sobre Preço Custo", "Sobre Preço Venda")),
             ("Venda Atacado c/ Aprazo", combo("NÃO", "SIM"))]
        ]

        # Preenche colunas com pares label/input
        for i in range(4):
            for texto, widget in campos[i]:
                label = QLabel(texto)
                label.setStyleSheet("font-weight: bold;")
                colunas[i].addWidget(label)
                colunas[i].addWidget(widget)

        # Junta colunas no layout horizontal
        for coluna in colunas:
            h_layout.addLayout(coluna)

        aba.setLayout(h_layout)
        return aba

    def mostrar_video(self):
        QMessageBox.information(self, "Ajuda", "Abrir link de vídeo explicativo (em desenvolvimento).")

    def salvar_configuracoes(self):
        QMessageBox.information(self, "Salvar", "Configurações salvas com sucesso!")
