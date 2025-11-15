from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox
from ui.obra_form import ObraForm
from ui.obra_detalhe import ObraDetalhe

class ObrasList(QWidget):
    def __init__(self, obra_controller, atividade_controller, medicao_controller, parent=None):
        super().__init__(parent)
        self.obra_controller = obra_controller
        self.atividade_controller = atividade_controller
        self.medicao_controller = medicao_controller

        self.layout = QVBoxLayout()
        btns = QHBoxLayout()
        self.btnNovo = QPushButton("Nova Obra")
        self.btnAtualizar = QPushButton("Atualizar lista")
        btns.addWidget(self.btnNovo)
        btns.addWidget(self.btnAtualizar)
        self.layout.addLayout(btns)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID","Nome","Cliente","Início","Fim Prev.","Valor"])
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

        self.btnNovo.clicked.connect(self.nova_obra)
        self.btnAtualizar.clicked.connect(self.load)
        self.table.cellDoubleClicked.connect(self.open_obra)

        self.load()

    def load(self):
        obras = self.obra_controller.listar_obras()
        self.table.setRowCount(len(obras))
        for r, o in enumerate(obras):
            self.table.setItem(r, 0, QTableWidgetItem(str(o.get("id"))))
            self.table.setItem(r, 1, QTableWidgetItem(o.get("nome") or ""))
            self.table.setItem(r, 2, QTableWidgetItem(o.get("cliente") or ""))
            self.table.setItem(r, 3, QTableWidgetItem(o.get("data_inicio") or ""))
            self.table.setItem(r, 4, QTableWidgetItem(o.get("data_fim_prevista") or ""))
            self.table.setItem(r, 5, QTableWidgetItem(f'R$ {o.get("valor_contrato") or 0:.2f}'))

    def nova_obra(self):
        dlg = ObraForm(self.obra_controller, parent=self)
        if dlg.exec():
            self.load()

    def open_obra(self, row, col):
        item = self.table.item(row, 0)
        if not item:
            return
        obra_id = int(item.text())
        obra = self.obra_controller.obter_obra(obra_id)
        if not obra:
            QMessageBox.warning(self, "Erro", "Obra não encontrada")
            return
        detalhe = ObraDetalhe(obra, self.atividade_controller, self.medicao_controller, parent=self)
        detalhe.exec()
        self.load()
