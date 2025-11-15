from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QDialog, QFormLayout, QLineEdit, QDoubleSpinBox, QMessageBox

class MateriaisView(QWidget):
    def __init__(self, material_controller, parent=None):
        super().__init__(parent)
        self.material_controller = material_controller
        self.layout = QVBoxLayout()
        h = QHBoxLayout()
        self.btnNovo = QPushButton("Novo Material")
        self.btnRefresh = QPushButton("Atualizar")
        h.addWidget(self.btnNovo)
        h.addWidget(self.btnRefresh)
        self.layout.addLayout(h)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID","Código","Descrição","Unidade","Estoque"])
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

        self.btnNovo.clicked.connect(self.novo_material)
        self.btnRefresh.clicked.connect(self.load)
        self.table.cellDoubleClicked.connect(self.editar_material)

        self.load()

    def load(self):
        rows = self.material_controller.listar()
        self.table.setRowCount(len(rows))
        for r, m in enumerate(rows):
            self.table.setItem(r,0, QTableWidgetItem(str(m.get("id"))))
            self.table.setItem(r,1, QTableWidgetItem(m.get("codigo") or ""))
            self.table.setItem(r,2, QTableWidgetItem(m.get("descricao") or ""))
            self.table.setItem(r,3, QTableWidgetItem(m.get("unidade") or ""))
            self.table.setItem(r,4, QTableWidgetItem(str(m.get("estoque") or 0)))

    def novo_material(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Novo Material")
        form = QFormLayout(dlg)
        txtCodigo = QLineEdit()
        txtDesc = QLineEdit()
        txtUnid = QLineEdit()
        spinEst = QDoubleSpinBox()
        spinEst.setMaximum(1e9)
        form.addRow("Código:", txtCodigo)
        form.addRow("Descrição:", txtDesc)
        form.addRow("Unidade:", txtUnid)
        form.addRow("Estoque:", spinEst)
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
            est = spinEst.value()
            if not desc:
                QMessageBox.warning(self, "Erro", "Descrição obrigatória")
                return
            self.material_controller.criar_material(codigo, desc, unid, est)
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
        spinEst = QDoubleSpinBox()
        spinEst.setMaximum(1e9)
        
        txtCodigo.setText(material.get("codigo") or "")
        txtDesc.setText(material.get("descricao") or "")
        txtUnid.setText(material.get("unidade") or "")
        spinEst.setValue(material.get("estoque") or 0)
        
        form.addRow("Código:", txtCodigo)
        form.addRow("Descrição:", txtDesc)
        form.addRow("Unidade:", txtUnid)
        form.addRow("Estoque:", spinEst)
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
            est = spinEst.value()
            if not desc:
                QMessageBox.warning(self, "Erro", "Descrição obrigatória")
                return
            self.material_controller.atualizar(material_id, codigo=codigo, descricao=desc, unidade=unid, estoque=est)
            dlg.accept()
            self.load()

        btnSalvar.clicked.connect(update)
        btnCancelar.clicked.connect(dlg.reject)
        dlg.exec()

