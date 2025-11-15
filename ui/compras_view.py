from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QComboBox, QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox
)
from PySide6.QtCore import Qt

class ComprasView(QWidget):
    def __init__(self, compra_controller, material_controller, obra_controller):
        super().__init__()
        self.controller = compra_controller
        self.material_controller = material_controller
        self.obra_controller = obra_controller
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Campos de cadastro
        form = QHBoxLayout()

        self.combo_material = QComboBox()
        self.carregar_materiais()

        self.combo_obra = QComboBox()
        self.carregar_obras()

        self.input_qtd = QLineEdit()
        self.input_fornecedor = QLineEdit()
        self.input_data = QLineEdit()
        self.input_valor = QLineEdit()
        self.input_status = QLineEdit()
        self.input_status.setText("Recebido")

        form.addWidget(QLabel("Material"))
        form.addWidget(self.combo_material)

        form.addWidget(QLabel("Obra"))
        form.addWidget(self.combo_obra)

        form.addWidget(QLabel("Qtd"))
        form.addWidget(self.input_qtd)

        form.addWidget(QLabel("Fornecedor"))
        form.addWidget(self.input_fornecedor)

        form.addWidget(QLabel("Data"))
        form.addWidget(self.input_data)

        form.addWidget(QLabel("Valor Total"))
        form.addWidget(self.input_valor)

        form.addWidget(QLabel("Status"))
        form.addWidget(self.input_status)

        layout.addLayout(form)

        btn_add = QPushButton("Registrar Compra")
        btn_add.clicked.connect(self.registrar_compra)
        layout.addWidget(btn_add)

        # Tabela
        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.carregar_tabela()

    def carregar_materiais(self):
        """Carrega lista de materiais no combo"""
        self.combo_material.clear()
        materiais = self.material_controller.listar()
        for m in materiais:
            descricao = m.get("descricao", "")
            codigo = m.get("codigo", "")
            if codigo:
                descricao = f"[{codigo}] {descricao}"
            self.combo_material.addItem(descricao, m.get("id"))

    def carregar_obras(self):
        """Carrega lista de obras no combo"""
        self.combo_obra.clear()
        obras = self.obra_controller.listar_obras()
        for o in obras:
            self.combo_obra.addItem(o.get("nome"), o.get("id"))

    def registrar_compra(self):
        try:
            material = self.combo_material.currentData()
            obra = self.combo_obra.currentData()
            qtd = float(self.input_qtd.text() or 0)
            fornecedor = self.input_fornecedor.text()
            data = self.input_data.text()
            valor = float(self.input_valor.text() or 0)
            status = self.input_status.text() or "Recebido"
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Entrada inválida: {e}")
            return

        self.controller.criar_compra(material, obra, qtd, fornecedor, data, valor, status)
        QMessageBox.information(self, "OK", "Compra registrada e estoque atualizado.")
        self.carregar_tabela()

    def carregar_tabela(self):
        compras = self.controller.listar()
        self.table.setRowCount(len(compras))
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["ID", "Material", "Qtd", "Fornecedor", "Data", "Valor", "Status", "Obra"])

        for i, c in enumerate(compras):
            self.table.setItem(i, 0, QTableWidgetItem(str(c.get("id"))))
            self.table.setItem(i, 1, QTableWidgetItem(str(c.get("material"))))
            self.table.setItem(i, 2, QTableWidgetItem(str(c.get("quantidade"))))
            self.table.setItem(i, 3, QTableWidgetItem(str(c.get("fornecedor"))))
            self.table.setItem(i, 4, QTableWidgetItem(str(c.get("data_compra"))))
            self.table.setItem(i, 5, QTableWidgetItem(str(c.get("valor_total"))))
            self.table.setItem(i, 6, QTableWidgetItem(str(c.get("status"))))
            self.table.setItem(i, 7, QTableWidgetItem(str(c.get("obra"))))
        
        # Recarregar materiais e obras quando atualiza tabela
        self.carregar_materiais()
        self.carregar_obras()
