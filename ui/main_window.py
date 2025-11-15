from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QStackedWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
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
        self.resize(1100, 700)

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
        
        # Criar font para os botões
        font_botoes = QFont()
        font_botoes.setPointSize(9)
        
        self.btnObras = QPushButton("Obras")
        self.btnObras.setFont(font_botoes)
        self.btnObras.setMinimumHeight(32)
        self.btnObras.setMaximumHeight(32)
        self.btnMateriais = QPushButton("Materiais")
        self.btnMateriais.setFont(font_botoes)
        self.btnMateriais.setMinimumHeight(32)
        self.btnMateriais.setMaximumHeight(32)
        self.btnCompras = QPushButton("Compras")
        self.btnCompras.setFont(font_botoes)
        self.btnCompras.setMinimumHeight(32)
        self.btnCompras.setMaximumHeight(32)
        self.btnFinanceiro = QPushButton("Despesas / Financeiro")
        self.btnFinanceiro.setFont(font_botoes)
        self.btnFinanceiro.setMinimumHeight(32)
        self.btnFinanceiro.setMaximumHeight(32)
        self.btnEVM = QPushButton("Painel EVM")
        self.btnEVM.setFont(font_botoes)
        self.btnEVM.setMinimumHeight(32)
        self.btnEVM.setMaximumHeight(32)
        
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
        
        # Definir largura máxima do menu - aumentado para caber o texto
        self.menu.setMaximumWidth(200)
        self.menu.setMinimumWidth(200)
