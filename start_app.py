import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Splash screen
    splash_pix = QPixmap("imagens/splash.png")
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()

    # Função para iniciar o main_v2.py depois do splash
    def start_main():
        splash.close()
        subprocess.Popen([sys.executable, "main_v2.py"])  # inicia o main_v2.py

    # Fecha o splash depois de 3 segundos e chama o main_v2.py
    QTimer.singleShot(3000, start_main)

    sys.exit(app.exec_())
