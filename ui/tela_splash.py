from PySide6.QtWidgets import QSplashScreen
from PySide6.QtGui import QPixmap, QFont, QColor, QScreen
from PySide6.QtCore import Qt, QTimer
import os

class TelaSplash:
    """Tela de abertura/splash do aplicativo"""
    
    @staticmethod
    def criar_splash(app):
        """Cria e exibe a tela de splash em tela cheia"""
        
        # Obtém o tamanho da tela (monitor)
        screen: QScreen = app.primaryScreen()
        screen_geometry = screen.geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        
        # Cria pixmap com tamanho da tela
        pixmap = QPixmap(screen_width, screen_height)
        pixmap.fill(QColor(255, 255, 255))  # Fundo branco
        
        splash = QSplashScreen(pixmap)
        splash.setWindowFlags(splash.windowFlags() | Qt.FramelessWindowHint)
        splash.showFullScreen()
        app.processEvents()
        
        # Adiciona texto no centro da tela
        font = QFont()
        font.setPointSize(24)
        font.setBold(True)
        splash.setFont(font)
        splash.showMessage(
            "Gestão de Obras PySide6",
            Qt.AlignCenter,
            QColor(0, 0, 0)  # Texto preto para contraste com fundo branco
        )
        
        app.processEvents()
        
        return splash
    
    @staticmethod
    def fechar_splash(splash, tempo_ms=3000):
        """Fecha a splash após o tempo especificado (em milissegundos)"""
        timer = QTimer()
        timer.singleShot(tempo_ms, splash.close)
        return timer
