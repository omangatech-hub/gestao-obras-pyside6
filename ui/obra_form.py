from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit, QDateEdit, QDoubleSpinBox, QPushButton, QHBoxLayout, QLabel
from PySide6.QtCore import QDate

class ObraForm(QDialog):
    def __init__(self, controller, obra=None, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.obra = obra
        self.setWindowTitle("Obra")
        self.layout = QFormLayout()
        self.txtNome = QLineEdit()
        self.txtCliente = QLineEdit()
        self.txtEndereco = QLineEdit()
        self.dtInicio = QDateEdit()
        self.dtInicio.setCalendarPopup(True)
        self.dtFimPrev = QDateEdit()
        self.dtFimPrev.setCalendarPopup(True)
        self.spinValor = QDoubleSpinBox()
        self.spinValor.setMaximum(1e12)
        self.spinValor.setPrefix("R$ ")
        self.spinValor.setDecimals(2)

        self.layout.addRow("Nome:", self.txtNome)
        self.layout.addRow("Cliente:", self.txtCliente)
        self.layout.addRow("Endereço:", self.txtEndereco)
        self.layout.addRow("Data Início:", self.dtInicio)
        self.layout.addRow("Data Fim Prev.:", self.dtFimPrev)
        self.layout.addRow("Valor Contrato:", self.spinValor)

        self.btnSalvar = QPushButton("Salvar")
        self.btnCancelar = QPushButton("Cancelar")
        h = QHBoxLayout()
        h.addWidget(self.btnSalvar)
        h.addWidget(self.btnCancelar)
        self.layout.addRow(h)
        self.setLayout(self.layout)

        self.btnSalvar.clicked.connect(self.save)
        self.btnCancelar.clicked.connect(self.reject)

        if obra:
            self.load_data(obra)
        else:
            d = QDate.currentDate()
            self.dtInicio.setDate(d)
            self.dtFimPrev.setDate(d)

    def load_data(self, obra):
        self.txtNome.setText(obra.get("nome", ""))
        self.txtCliente.setText(obra.get("cliente", "") or "")
        self.txtEndereco.setText(obra.get("endereco", "") or "")
        try:
            if obra.get("data_inicio"):
                self.dtInicio.setDate(QDate.fromString(obra.get("data_inicio"), "yyyy-MM-dd"))
            if obra.get("data_fim_prevista"):
                self.dtFimPrev.setDate(QDate.fromString(obra.get("data_fim_prevista"), "yyyy-MM-dd"))
        except:
            pass
        self.spinValor.setValue(obra.get("valor_contrato") or 0.0)

    def save(self):
        nome = self.txtNome.text().strip()
        if not nome:
            self.layout.addRow(QLabel("Nome obrigatório"), QLabel(""))
            return
        cliente = self.txtCliente.text().strip()
        endereco = self.txtEndereco.text().strip()
        data_inicio = self.dtInicio.date().toString("yyyy-MM-dd")
        data_fim = self.dtFimPrev.date().toString("yyyy-MM-dd")
        valor = self.spinValor.value()
        if self.obra:
            self.controller.atualizar_obra(self.obra["id"], nome=nome, cliente=cliente, endereco=endereco, data_inicio=data_inicio, data_fim_prevista=data_fim, valor_contrato=valor)
        else:
            self.controller.criar_obra(nome, cliente, endereco, data_inicio, data_fim, valor)
        self.accept()
