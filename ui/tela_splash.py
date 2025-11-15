from PySide6.QtWidgets import QSplashScreen
from PySide6.QtGui import QPixmap, QFont, QColor
from PySide6.QtCore import Qt, QTimer
import os

class TelaSplash:
    """Tela de abertura/splash do aplicativo"""
    
    @staticmethod
    def criar_splash(app):
        """Cria e exibe a tela de splash"""
        
        # Tenta carregar a imagem
        caminho_imagem = os.path.join(os.path.dirname(__file__), '..', 'assets', 'splash.png')
        
        if os.path.exists(caminho_imagem):
            pixmap = QPixmap(caminho_imagem)
        else:
            # Se não existir imagem, cria um fundo padrão
            pixmap = QPixmap(800, 600)
            pixmap.fill(QColor(255, 255, 255))  # Branco
        
        splash = QSplashScreen(pixmap)
        splash.show()
        app.processEvents()
        
        # Adiciona texto
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        splash.setFont(font)
        splash.showMessage(
            "Gestão de Obras PySide6",
            Qt.AlignBottom | Qt.AlignCenter,
            QColor(255, 255, 255)
        )
        
        app.processEvents()
        
        return splash
    
    @staticmethod
    def fechar_splash(splash, tempo_ms=3000):
        """Fecha a splash após o tempo especificado (em milissegundos)"""
        timer = QTimer()
        timer.singleShot(tempo_ms, splash.close)
        return timer
