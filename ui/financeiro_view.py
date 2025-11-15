from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QComboBox, QTableWidget, QTableWidgetItem, QMessageBox, QFileDialog
)
from PySide6.QtCore import Qt
from utils.helpers import exportar_csv, exportar_excel

class FinanceiroView(QWidget):
    def __init__(self, despesa_controller, obra_controller):
        super().__init__()
        self.controller = despesa_controller
        self.obra_controller = obra_controller
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Formulário
        form = QHBoxLayout()

        self.combo_obra = QComboBox()
        for o in self.obra_controller.listar_obras():
            self.combo_obra.addItem(o.get("nome"), o.get("id"))

        self.input_categoria = QLineEdit()
        self.input_data = QLineEdit()
        self.input_valor = QLineEdit()
        self.input_desc = QLineEdit()

        form.addWidget(QLabel("Obra"))
        form.addWidget(self.combo_obra)

        form.addWidget(QLabel("Categoria"))
        form.addWidget(self.input_categoria)

        form.addWidget(QLabel("Data"))
        form.addWidget(self.input_data)

        form.addWidget(QLabel("Valor"))
        form.addWidget(self.input_valor)

        form.addWidget(QLabel("Descrição"))
        form.addWidget(self.input_desc)

        layout.addLayout(form)

        btn_add = QPushButton("Registrar Despesa")
        btn_add.clicked.connect(self.registrar)
        layout.addWidget(btn_add)

        # Export buttons
        he = QHBoxLayout()
        self.btn_csv = QPushButton("Exportar CSV")
        self.btn_xlsx = QPushButton("Exportar Excel")
        he.addWidget(self.btn_csv)
        he.addWidget(self.btn_xlsx)
        layout.addLayout(he)
        self.btn_csv.clicked.connect(self.export_csv)
        self.btn_xlsx.clicked.connect(self.export_xlsx)

        # Tabela de despesas
        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.carregar_tabela()

    def registrar(self):
        try:
            obra_id = self.combo_obra.currentData()
            categoria = self.input_categoria.text()
            data = self.input_data.text()
            valor = float(self.input_valor.text() or 0)
            desc = self.input_desc.text()
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Entrada inválida: {e}")
            return

        self.controller.criar_despesa(obra_id, categoria, data, valor, desc)
        QMessageBox.information(self, "OK", "Despesa registrada.")
        self.carregar_tabela()

    def carregar_tabela(self):
        despesas = self.controller.listar_todas()
        self.table.setRowCount(len(despesas))
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Obra", "Categoria", "Data", "Valor", "Descrição"])

        for i, d in enumerate(despesas):
            self.table.setItem(i, 0, QTableWidgetItem(str(d.get("id"))))
            self.table.setItem(i, 1, QTableWidgetItem(str(d.get("obra"))))
            self.table.setItem(i, 2, QTableWidgetItem(str(d.get("categoria"))))
            self.table.setItem(i, 3, QTableWidgetItem(str(d.get("data"))))
            self.table.setItem(i, 4, QTableWidgetItem(str(d.get("valor"))))
            self.table.setItem(i, 5, QTableWidgetItem(str(d.get("descricao"))))

    def export_csv(self):
        despesas = self.controller.listar_todas()
        if not despesas:
            QMessageBox.information(self, "Info", "Nenhuma despesa para exportar.")
            return
        path, _ = QFileDialog.getSaveFileName(self, "Salvar CSV", "despesas.csv", "CSV Files (*.csv)")
        if path:
            cols = ["id","obra","categoria","data","valor","descricao"]
            exportar_csv(path, despesas, cols)
            QMessageBox.information(self, "OK", f"Exportado: {path}")

    def export_xlsx(self):
        despesas = self.controller.listar_todas()
        if not despesas:
            QMessageBox.information(self, "Info", "Nenhuma despesa para exportar.")
            return
        path, _ = QFileDialog.getSaveFileName(self, "Salvar XLSX", "despesas.xlsx", "Excel Files (*.xlsx)")
        if path:
            cols = ["id","obra","categoria","data","valor","descricao"]
            exportar_excel(path, despesas, cols)
            QMessageBox.information(self, "OK", f"Exportado: {path}")
