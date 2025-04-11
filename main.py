import sys
from PyQt5.QtWidgets import QApplication
from splash import SplashVisual         # Splash do sistema
from janela import MainPDVWindow       # Janela principal corrigida

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Mostra a splash
    splash = SplashVisual()
    if splash.exec_() == 1:  # Quando clicar em "Entrar no Sistema"
        janela = MainPDVWindow()
        janela.show()
        sys.exit(app.exec_())
