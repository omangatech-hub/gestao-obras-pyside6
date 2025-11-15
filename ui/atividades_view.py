from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QDialog, QFormLayout, QLineEdit, QDateEdit, QDoubleSpinBox
from PySide6.QtCore import QDate

class AtividadesView(QWidget):
    def __init__(self, obra_id, atividade_controller, medicao_controller, parent=None):
        super().__init__(parent)
        self.obra_id = obra_id
        self.atividade_controller = atividade_controller
        self.medicao_controller = medicao_controller

        self.layout = QVBoxLayout()
        h = QHBoxLayout()
        self.btnNovo = QPushButton("Nova Atividade")
        self.btnRefresh = QPushButton("Atualizar")
        h.addWidget(self.btnNovo)
        h.addWidget(self.btnRefresh)
        self.layout.addLayout(h)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID","Nome","Qtd Prev.","Unid","Custo Unit.","Período"])
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

        self.btnNovo.clicked.connect(self.nova_atividade)
        self.btnRefresh.clicked.connect(self.load)
        self.table.cellDoubleClicked.connect(self.open_medicoes)

        self.load()

    def load(self):
        rows = self.atividade_controller.listar_por_obra(self.obra_id)
        self.table.setRowCount(len(rows))
        for r, a in enumerate(rows):
            self.table.setItem(r,0, QTableWidgetItem(str(a.get("id"))))
            self.table.setItem(r,1, QTableWidgetItem(a.get("nome") or ""))
            self.table.setItem(r,2, QTableWidgetItem(str(a.get("quantidade_prevista") or 0)))
            self.table.setItem(r,3, QTableWidgetItem(a.get("unidade") or ""))
            self.table.setItem(r,4, QTableWidgetItem(f"R$ {a.get('custo_unitario') or 0:.2f}"))

            periodo = f"{a.get('data_inicio') or ''} -> {a.get('data_fim') or ''}"
            self.table.setItem(r,5, QTableWidgetItem(periodo))

    def nova_atividade(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Nova Atividade")
        form = QFormLayout(dlg)
        txtNome = QLineEdit()
        txtQtd = QDoubleSpinBox()
        txtQtd.setMaximum(1e9)
        txtUnid = QLineEdit()
        dtInicio = QDateEdit()
        dtInicio.setCalendarPopup(True)
        dtInicio.setDate(QDate.currentDate())
        dtFim = QDateEdit()
        dtFim.setCalendarPopup(True)
        dtFim.setDate(QDate.currentDate())
        spinCusto = QDoubleSpinBox()
        spinCusto.setMaximum(1e12)
        spinCusto.setDecimals(2)

        form.addRow("Nome:", txtNome)
        form.addRow("Quantidade Prev.:", txtQtd)
        form.addRow("Unidade:", txtUnid)
        form.addRow("Data Início:", dtInicio)
        form.addRow("Data Fim:", dtFim)
        form.addRow("Custo Unit.:", spinCusto)

        btnSalvar = QPushButton("Salvar")
        btnCancelar = QPushButton("Cancelar")
        h = QHBoxLayout()
        h.addWidget(btnSalvar)
        h.addWidget(btnCancelar)
        form.addRow(h)

        def save_and_close():
            nome = txtNome.text().strip()
            if not nome:
                return
            qtd = txtQtd.value()
            unid = txtUnid.text().strip()
            di = dtInicio.date().toString("yyyy-MM-dd")
            df = dtFim.date().toString("yyyy-MM-dd")
            custo = spinCusto.value()
            self.atividade_controller.criar_atividade(self.obra_id, nome, qtd, unid, custo, di, df)
            dlg.accept()
            self.load()

        btnSalvar.clicked.connect(save_and_close)
        btnCancelar.clicked.connect(dlg.reject)
        dlg.exec()
