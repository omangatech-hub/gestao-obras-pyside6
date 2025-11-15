from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QDialog, QFormLayout, QDateEdit, QDoubleSpinBox, QTextEdit
from PySide6.QtCore import QDate

class MedicoesView(QWidget):
    def __init__(self, obra_id, atividade_controller, medicao_controller, parent=None):
        super().__init__(parent)
        self.obra_id = obra_id
        self.atividade_controller = atividade_controller
        self.medicao_controller = medicao_controller

        self.layout = QVBoxLayout()
        top = QHBoxLayout()
        self.cmbAtividades = QComboBox()
        self.btnNovo = QPushButton("Nova Medição")
        self.btnRefresh = QPushButton("Atualizar")
        top.addWidget(self.cmbAtividades)
        top.addWidget(self.btnNovo)
        top.addWidget(self.btnRefresh)
        self.layout.addLayout(top)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID","Data","Qtd Exec.","Observação"])
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

        self.btnNovo.clicked.connect(self.nova_medicao)
        self.btnRefresh.clicked.connect(self.load_atividades)
        self.cmbAtividades.currentIndexChanged.connect(self.load_medicoes)

        self.load_atividades()

    def load_atividades(self):
        rows = self.atividade_controller.listar_por_obra(self.obra_id)
        self.cmbAtividades.clear()
        self.atividades = rows
        for a in rows:
            self.cmbAtividades.addItem(f"{a.get('id')} - {a.get('nome')}", a.get('id'))
        self.load_medicoes()

    def load_medicoes(self):
        idx = self.cmbAtividades.currentIndex()
        if idx < 0:
            self.table.setRowCount(0)
            return
        atividade_id = self.cmbAtividades.currentData()
        rows = self.medicao_controller.listar_por_atividade(atividade_id)
        self.table.setRowCount(len(rows))
        for r, m in enumerate(rows):
            self.table.setItem(r,0, QTableWidgetItem(str(m.get("id"))))
            self.table.setItem(r,1, QTableWidgetItem(m.get("data") or ""))
            self.table.setItem(r,2, QTableWidgetItem(str(m.get("quantidade_executada") or 0)))
            self.table.setItem(r,3, QTableWidgetItem(m.get("observacao") or ""))

    def nova_medicao(self):
        idx = self.cmbAtividades.currentIndex()
        if idx < 0:
            return
        atividade_id = self.cmbAtividades.currentData()
        dlg = QDialog(self)
        dlg.setWindowTitle("Nova Medição")
        form = QFormLayout(dlg)
        dt = QDateEdit()
        dt.setCalendarPopup(True)
        dt.setDate(QDate.currentDate())
        qtd = QDoubleSpinBox()
        qtd.setMaximum(1e9)
        obs = QTextEdit()
        form.addRow("Data:", dt)
        form.addRow("Quantidade Executada:", qtd)
        form.addRow("Observação:", obs)
        btnSalvar = QPushButton("Salvar")
        btnCancelar = QPushButton("Cancelar")
        h = QHBoxLayout()
        h.addWidget(btnSalvar)
        h.addWidget(btnCancelar)
        form.addRow(h)

        def save_and_close():
            data = dt.date().toString("yyyy-MM-dd")
            quantidade = qtd.value()
            observacao = obs.toPlainText()
            self.medicao_controller.criar_medicao(atividade_id, data, quantidade, observacao)
            dlg.accept()
            self.load_medicoes()

        btnSalvar.clicked.connect(save_and_close)
        btnCancelar.clicked.connect(dlg.reject)
        dlg.exec()
