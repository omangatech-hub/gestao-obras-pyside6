from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QStackedWidget
from PySide6.QtGui import QScreen
from PySide6.QtCore import Qt
from ui.obras_list import ObrasList
from ui.materiais_view import MateriaisView
from ui.compras_view import ComprasView
from ui.financeiro_view import FinanceiroView
from ui.evm_view import EVMView

class MainWindow(QMainWindow):
    def __init__(self, controllers):
        super().__init__()
        self.controllers = controllers
        self.setWindowTitle("Gestão de Obras - MVP (PySide6)")
        
        # Configurar janela responsiva - tamanho baseado na tela do monitor
        screen: QScreen = self.screen()
        screen_geometry = screen.geometry()
        
        # Define tamanho como 90% da tela disponível (menor que antes)
        window_width = int(screen_geometry.width() * 0.90)
        window_height = int(screen_geometry.height() * 0.90)
        self.resize(window_width, window_height)
        
        # Centraliza a janela na tela
        self.move(
            int((screen_geometry.width() - window_width) / 2),
            int((screen_geometry.height() - window_height) / 2)
        )

        central = QWidget()
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(5, 5, 5, 5)  # Reduzir margens
        main_layout.setSpacing(5)  # Reduzir espaçamento
        central.setLayout(main_layout)
        self.setCentralWidget(central)

        # menu lateral simples - mais compacto
        self.menu = QWidget()
        menu_layout = QVBoxLayout()
        menu_layout.setContentsMargins(2, 2, 2, 2)  # Margens reduzidas
        menu_layout.setSpacing(3)  # Espaçamento reduzido
        self.menu.setLayout(menu_layout)
        
        lbl = QLabel("<b>Menu</b>")
        lbl.setAlignment(Qt.AlignCenter)
        menu_layout.addWidget(lbl)
        
        self.btnObras = QPushButton("Obras")
        self.btnObras.setMinimumHeight(35)
        self.btnMateriais = QPushButton("Materiais")
        self.btnMateriais.setMinimumHeight(35)
        self.btnCompras = QPushButton("Compras")
        self.btnCompras.setMinimumHeight(35)
        self.btnFinanceiro = QPushButton("Despesas / Financeiro")
        self.btnFinanceiro.setMinimumHeight(35)
        self.btnEVM = QPushButton("Painel EVM")
        self.btnEVM.setMinimumHeight(35)
        
        menu_layout.addWidget(self.btnObras)
        menu_layout.addWidget(self.btnMateriais)
        menu_layout.addWidget(self.btnCompras)
        menu_layout.addWidget(self.btnFinanceiro)
        menu_layout.addWidget(self.btnEVM)
        menu_layout.addStretch()

        # área principal com páginas
        self.pages = QStackedWidget()
        # página obras
        obras_page = ObrasList(controllers['obra'], controllers['atividade'], controllers['medicao'])
        self.pages.addWidget(obras_page)
        # página materiais
        materiais_page = MateriaisView(controllers['material'])
        self.pages.addWidget(materiais_page)
        # compras
        compras_page = ComprasView(controllers['compra'], controllers['material'], controllers['obra'])
        self.pages.addWidget(compras_page)
        # financeiro/despesas
        financeiro_page = FinanceiroView(controllers['despesa'], controllers['obra'])
        self.pages.addWidget(financeiro_page)
        # EVM
        evm_page = EVMView(controllers['obra'], controllers['evm'])
        self.pages.addWidget(evm_page)

        main_layout.addWidget(self.menu, 0)  # Menu com tamanho fixo reduzido
        main_layout.addWidget(self.pages, 1)  # Conteúdo expandido

        # ligações
        self.btnObras.clicked.connect(lambda: self.pages.setCurrentIndex(0))
        self.btnMateriais.clicked.connect(lambda: self.pages.setCurrentIndex(1))
        self.btnCompras.clicked.connect(lambda: self.pages.setCurrentIndex(2))
        self.btnFinanceiro.clicked.connect(lambda: self.pages.setCurrentIndex(3))
        self.btnEVM.clicked.connect(lambda: self.pages.setCurrentIndex(4))
