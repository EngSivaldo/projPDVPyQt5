import sys
import sqlite3

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget,
    QHBoxLayout, QToolButton, QDialog, QMessageBox, QSpacerItem, QSizePolicy, QSplashScreen
)
from PyQt5.QtGui import QIcon, QPixmap, QFont, QPainter, QBrush, QColor
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QPoint, QEasingCurve, QTimer

# Importações das janelas reais do sistema
from clientes import CadastroClientes
from cadastro_produtos import CadastroProdutoWindow
from tela_vendas import TelaVendas
from fornecedor import TelaCadastroFornecedores
from historico_vendas import HistoricoVendas
from FluxoCaixa import FluxoCaixa
from contas_pagar import ContasPagar
from contas_receber import ContasReceber
from fechar_caixa import TelaFecharCaixa
from tela_impressoras import TelaImpressoras
from etiquetas.selecao_modelo import SelecaoModeloEtiqueta
from configuracoes import TelaConfiguracoes
from backup_dados import BackupWindow
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl

import shutil
import datetime
import os

def backup_banco():
    pasta_backup = os.path.join(os.path.dirname(__file__), "backups")
    os.makedirs(pasta_backup, exist_ok=True)

    caminho_original = os.path.join(os.path.dirname(__file__), "banco_dados.db")
    data = datetime.datetime.now().strftime("%Y%m%d")
    caminho_backup = os.path.join(pasta_backup, f"backup_banco_dados_{data}.db")

    if os.path.exists(caminho_original) and not os.path.exists(caminho_backup):
        shutil.copy2(caminho_original, caminho_backup)
        print(f"🛡️ Backup criado: {caminho_backup}")
    else:
        print("📁 Backup já existe para hoje.")

#   # Limpa backups com mais de 7 dias de idade
def limpar_backups_antigos(dias=7):
    pasta_backup = os.path.join(os.path.dirname(__file__), "backups")
    if not os.path.exists(pasta_backup):
        return

    agora = datetime.datetime.now()
    for nome in os.listdir(pasta_backup):
        caminho = os.path.join(pasta_backup, nome)
        if os.path.isfile(caminho):
            modificado = datetime.datetime.fromtimestamp(os.path.getmtime(caminho))
            if (agora - modificado).days > dias:
                os.remove(caminho)
                print(f"🗑️ Backup antigo removido: {nome}")


class GradientBackground(QWidget):
    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)
           # Cria backup do banco logo na inicialização do sistema
        backup_banco()

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QBrush(QColor(15, 108, 191), Qt.SolidPattern)
        painter.fillRect(self.rect(), gradient)

class MainPDVWindow(QMainWindow):
    def __init__(self, versao_teste=False, usuario_logado="Usuário", codigo_usuario="000"):
        super().__init__()
        self.versao_teste = versao_teste
        self.usuario_logado = usuario_logado
        self.codigo_usuario = codigo_usuario

        self.setWindowTitle("SYSON PDV PRÓ")
        self.setGeometry(100, 100, 1366, 768)
        self.setStyleSheet("color: white;")

        self.init_ui()
        self.init_database()
        
         # Reproduzir som ao abrir a janela
        self.tocar_musica_intro()

    def tocar_musica_intro(self):
        from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
        from PyQt5.QtCore import QUrl
        import os

        self.player = QMediaPlayer()
        caminho_absoluto = os.path.abspath("sons/musica_intro.mp3")
        url = QUrl.fromLocalFile(caminho_absoluto)
        media = QMediaContent(url)
        self.player.setMedia(media)
        self.player.setVolume(50)
        self.player.play()

    def animar_logo(self):
        self.animacao = QPropertyAnimation(self.logo, b"pos")
        self.animacao.setDuration(3000)
        self.animacao.setStartValue(QPoint(self.logo.x(), self.logo.y()))
        self.animacao.setEndValue(QPoint(self.logo.x(), self.logo.y() + 15))
        self.animacao.setLoopCount(-1)
        self.animacao.setEasingCurve(QEasingCurve.InOutQuad)
        self.animacao.start()

    def init_ui(self):
        bg = GradientBackground()
        self.setCentralWidget(bg)

        main_layout = QVBoxLayout(bg)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # BARRA DE MENU
        menu_layout = QHBoxLayout()
        botoes = [
            ("PRODUTOS", "imagens/produtos.png", self.abrir_tela_produtos),
            ("CLIENTES", "imagens/clientes.png", self.abrir_tela_clientes),
            ("FORNECEDOR", "imagens/fornecedor.png", self.abrir_tela_fornecedor),
            ("HIST VENDAS", "imagens/historico_vendas.png", self.abrir_tela_historico_vendas),
            ("FLUXO DE CAIXA", "imagens/fluxo_caixa.png", self.abrir_tela_fluxo_caixa),
            ("C. A PAGAR", "imagens/contas_pagar.png", self.abrir_tela_contas_pagar),
            ("C. A RECEBER", "imagens/contas_receber.png", self.abrir_tela_contas_receber),
            ("VENDAS", "imagens/vendas.png", self.abrir_tela_vendas),
            ("FECHAR CAIXA", "imagens/fechar_caixa.png", self.abrir_tela_fechar_caixa),
            ("IMPRESSORAS", "imagens/impressora.png", self.abrir_tela_impressoras),
            ("BACKUP", "imagens/backup.png", self.abrir_tela_backup),
            ("ETIQUETAS", "imagens/etiquetas.png", self.abrir_tela_etiquetas),
            ("LOGOUT", "imagens/logout.png", self.logout)
        ]

        for descricao, icone_path, acao in botoes:
            btn = QToolButton()
            btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            btn.setIcon(QIcon(icone_path))
            btn.setText(descricao)
            btn.setIconSize(QSize(48, 48))
            btn.setFixedSize(100, 85)
            btn.setStyleSheet("""
                QToolButton {
                    background-color: rgba(255, 255, 255, 0.1);
                    color: white;
                    font-size: 10px;
                    font-weight: bold;
                    padding: 8px;
                    border-radius: 10px;
                }
                QToolButton:hover {
                    background-color: rgba(255, 255, 255, 0.3);
                    color: #ffcc00;
                }
            """)
            btn.clicked.connect(acao)
            menu_layout.addWidget(btn)

        main_layout.addLayout(menu_layout)
        main_layout.addSpacing(30)

        # LOGO CENTRALIZADA COM EFEITO
        logo_container = QWidget()
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        self.logo = QLabel()
        pixmap = QPixmap("imagens/imgChatGPT.png")
        self.logo.setPixmap(pixmap.scaled(1000, 620, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.logo.setAlignment(Qt.AlignCenter)
        self.logo.setStyleSheet("border: none; margin: 0 auto;")
        logo_layout.addWidget(self.logo, alignment=Qt.AlignCenter)
        main_layout.addWidget(logo_container, alignment=Qt.AlignCenter)
        self.animar_logo()

        # EXPANSOR
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # RODAPÉ ESTILIZADO
        rodape = QLabel(
            f"<b>SYSON PDV PRÓ</b> | descricao da Empresa | Usuário: <i>{self.usuario_logado}</i> | Código: {self.codigo_usuario}"
        )
        rodape.setAlignment(Qt.AlignCenter)
        rodape.setStyleSheet("""
            background-color: rgba(0, 0, 0, 0.4);
            color: white;
            padding: 12px;
            font-size: 12px;
            font-family: 'Segoe UI', sans-serif;
        """)
        main_layout.addWidget(rodape)

    def abrir_tela_vendas(self): TelaVendas().exec_()
    def abrir_tela_produtos(self): CadastroProdutoWindow().exec_()
    def abrir_tela_clientes(self): CadastroClientes().exec_()
    def abrir_tela_fornecedor(self): TelaCadastroFornecedores().exec_()
    def abrir_tela_historico_vendas(self): HistoricoVendas().exec_()
    def abrir_tela_fluxo_caixa(self): FluxoCaixa().exec_()
    def abrir_tela_contas_pagar(self): ContasPagar().exec_()
    def abrir_tela_contas_receber(self): ContasReceber().exec_()
    def abrir_tela_fechar_caixa(self): TelaFecharCaixa().exec_()
    def abrir_tela_impressoras(self): TelaImpressoras().exec_()
    def abrir_tela_backup(self): BackupWindow().exec_()
    def abrir_tela_etiquetas(self): SelecaoModeloEtiqueta().exec_()

    def animar_logo(self):
        self.animacao = QPropertyAnimation(self.logo, b"pos")
        self.animacao.setDuration(2000)
        self.animacao.setStartValue(QPoint(self.logo.x(), self.logo.y()))
        self.animacao.setEndValue(QPoint(self.logo.x(), self.logo.y() + 30))
        self.animacao.setLoopCount(-1)
        self.animacao.setEasingCurve(QEasingCurve.InOutSine)  # movimento suave
        self.animacao.setDirection(QPropertyAnimation.Forward)
        self.animacao.start()
        
    def tocar_musica_fundo(self):
        self.player = QMediaPlayer()
        url = QUrl.fromLocalFile("sons/musica_intro.mp3")  # Substitua com o caminho correto
        self.player.setMedia(QMediaContent(url))
        self.player.setVolume(50)  # Volume de 0 a 100
        self.player.play()




    def logout(self):
        resposta = QMessageBox.question(
            self, "Confirmação de Logout", "Tem certeza que deseja sair do sistema?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if resposta == QMessageBox.Yes:
            self.close()

    def init_database(self):
        self.conn = sqlite3.connect("banco_dados.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT,
                descricao TEXT,
                fornecedor TEXT,
                unidade TEXT,
                preco_compra REAL,
                preco_venda REAL
            )
        """)
        self.conn.commit()
        self.tocar_musica_fundo()

        
    
    

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Splash screen
    splash_pix = QPixmap("imagens/splash.png")
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()

    # Espera de 3 segundos antes de iniciar a janela principal
    QTimer.singleShot(3000, splash.close)

    def start_main_window():
        global main_window  # <- isso mantém a referência viva
        main_window = MainPDVWindow(versao_teste=True, usuario_logado="Admin", codigo_usuario="001")
        main_window.show()


    QTimer.singleShot(3000, start_main_window)

    sys.exit(app.exec_())
