from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QDialog, QFormLayout, QLineEdit, QMessageBox, QFileDialog, QRadioButton, QButtonGroup
from utils.importar_excel import ImportadorExcel
from utils.gerenciador_excel import GerenciadorExcel

class MateriaisView(QWidget):
    def __init__(self, material_controller, parent=None):
        super().__init__(parent)
        self.material_controller = material_controller
        self.gerenciador_excel = None
        self.usando_excel = False
        self.layout = QVBoxLayout()
        
        # Botões de modo
        h_modo = QHBoxLayout()
        self.btnBancoDados = QPushButton("Usar Banco de Dados")
        self.btnCarregarExcel = QPushButton("Carregar do Excel")
        h_modo.addWidget(self.btnBancoDados)
        h_modo.addWidget(self.btnCarregarExcel)
        self.layout.addLayout(h_modo)
        
        # Botões de ação
        h = QHBoxLayout()
        self.btnNovo = QPushButton("Novo Material")
        self.btnRefresh = QPushButton("Atualizar")
        self.btnImportar = QPushButton("Importar Excel")
        self.btnExportarModelo = QPushButton("Baixar Modelo")
        h.addWidget(self.btnNovo)
        h.addWidget(self.btnImportar)
        h.addWidget(self.btnExportarModelo)
        h.addWidget(self.btnRefresh)
        self.layout.addLayout(h)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID","Código","Descrição","Unidade"])
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

        self.btnNovo.clicked.connect(self.novo_material)
        self.btnRefresh.clicked.connect(self.load)
        self.btnImportar.clicked.connect(self.importar_excel)
        self.btnExportarModelo.clicked.connect(self.exportar_modelo)
        self.btnBancoDados.clicked.connect(self.usar_banco_dados)
        self.btnCarregarExcel.clicked.connect(self.usar_excel)
        self.table.cellDoubleClicked.connect(self.editar_material)

        self.load()

    def load(self):
        if self.usando_excel and self.gerenciador_excel:
            materiais = self.gerenciador_excel.obter_materiais()
        else:
            materiais = self.material_controller.listar()
        
        self.table.setRowCount(len(materiais))
        for r, m in enumerate(materiais):
            self.table.setItem(r,0, QTableWidgetItem(str(m.get("id"))))
            self.table.setItem(r,1, QTableWidgetItem(m.get("codigo") or ""))
            self.table.setItem(r,2, QTableWidgetItem(m.get("descricao") or ""))
            self.table.setItem(r,3, QTableWidgetItem(m.get("unidade") or ""))

    def novo_material(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Novo Material")
        form = QFormLayout(dlg)
        txtCodigo = QLineEdit()
        txtDesc = QLineEdit()
        txtUnid = QLineEdit()
        form.addRow("Código:", txtCodigo)
        form.addRow("Descrição:", txtDesc)
        form.addRow("Unidade:", txtUnid)
        btnSalvar = QPushButton("Salvar")
        btnCancelar = QPushButton("Cancelar")
        h = QHBoxLayout()
        h.addWidget(btnSalvar)
        h.addWidget(btnCancelar)
        form.addRow(h)

        def save():
            codigo = txtCodigo.text().strip()
            desc = txtDesc.text().strip()
            unid = txtUnid.text().strip()
            if not desc:
                QMessageBox.warning(self, "Erro", "Descrição obrigatória")
                return
            self.material_controller.criar_material(codigo, desc, unid)
            dlg.accept()
            self.load()

        btnSalvar.clicked.connect(save)
        btnCancelar.clicked.connect(dlg.reject)
        dlg.exec()

    def editar_material(self, row, col):
        """Método chamado ao dar duplo clique em uma célula da tabela"""
        material_id = int(self.table.item(row, 0).text())
        material = self.material_controller.obter(material_id)
        
        dlg = QDialog(self)
        dlg.setWindowTitle("Editar Material")
        form = QFormLayout(dlg)
        txtCodigo = QLineEdit()
        txtDesc = QLineEdit()
        txtUnid = QLineEdit()
        
        txtCodigo.setText(material.get("codigo") or "")
        txtDesc.setText(material.get("descricao") or "")
        txtUnid.setText(material.get("unidade") or "")
        
        form.addRow("Código:", txtCodigo)
        form.addRow("Descrição:", txtDesc)
        form.addRow("Unidade:", txtUnid)
        btnSalvar = QPushButton("Salvar")
        btnCancelar = QPushButton("Cancelar")
        h = QHBoxLayout()
        h.addWidget(btnSalvar)
        h.addWidget(btnCancelar)
        form.addRow(h)

        def update():
            codigo = txtCodigo.text().strip()
            desc = txtDesc.text().strip()
            unid = txtUnid.text().strip()
            if not desc:
                QMessageBox.warning(self, "Erro", "Descrição obrigatória")
                return
            self.material_controller.atualizar(material_id, codigo=codigo, descricao=desc, unidade=unid)
            dlg.accept()
            self.load()

        btnSalvar.clicked.connect(update)
        btnCancelar.clicked.connect(dlg.reject)
        dlg.exec()

    def importar_excel(self):
        """Abre diálogo para selecionar arquivo Excel"""
        arquivo, _ = QFileDialog.getOpenFileName(
            self,
            "Selecione o arquivo Excel",
            "",
            "Arquivos Excel (*.xlsx *.xls);;Todos os arquivos (*.*)"
        )
        
        if not arquivo:
            return
        
        sucesso, mensagem = ImportadorExcel.importar_materiais(arquivo, self.material_controller)
        
        if sucesso:
            QMessageBox.information(self, "Sucesso", mensagem)
            self.load()
        else:
            QMessageBox.critical(self, "Erro na Importação", mensagem)

    def exportar_modelo(self):
        """Exporta um modelo de Excel para download"""
        caminho, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar modelo Excel",
            "modelo_materiais.xlsx",
            "Arquivos Excel (*.xlsx)"
        )
        
        if not caminho:
            return
        
        sucesso, mensagem = ImportadorExcel.exportar_modelo_excel(caminho)
        
        if sucesso:
            QMessageBox.information(self, "Sucesso", mensagem)
        else:
            QMessageBox.critical(self, "Erro", mensagem)

    def usar_banco_dados(self):
        """Muda para usar banco de dados"""
        self.usando_excel = False
        self.btnNovo.setEnabled(True)
        self.btnImportar.setEnabled(True)
        self.btnExportarModelo.setEnabled(True)
        QMessageBox.information(self, "Modo", "Agora usando Banco de Dados")
        self.load()

    def usar_excel(self):
        """Carrega um arquivo Excel para usar como fonte de dados"""
        arquivo, _ = QFileDialog.getOpenFileName(
            self,
            "Selecione o arquivo Excel com materiais",
            "",
            "Arquivos Excel (*.xlsx *.xls);;Todos os arquivos (*.*)"
        )
        
        if not arquivo:
            return
        
        self.gerenciador_excel = GerenciadorExcel()
        sucesso, mensagem = self.gerenciador_excel.carregar_arquivo(arquivo)
        
        if sucesso:
            self.usando_excel = True
            self.btnNovo.setEnabled(False)
            self.btnImportar.setEnabled(False)
            self.btnExportarModelo.setEnabled(False)
            QMessageBox.information(self, "Sucesso", mensagem + "\n\nAgora usando Excel como fonte de dados")
            self.load()
        else:
            QMessageBox.critical(self, "Erro", mensagem)

