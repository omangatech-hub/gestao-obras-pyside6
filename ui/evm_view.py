from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox
from PySide6.QtCore import Qt

class EVMView(QWidget):
    def __init__(self, obra_controller, evm_controller):
        super().__init__()
        self.obra_controller = obra_controller
        self.evm_controller = evm_controller
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.combo = QComboBox()
        for o in self.obra_controller.listar_obras():
            self.combo.addItem(o.get("nome"), o.get("id"))
        self.combo.currentIndexChanged.connect(self.atualizar)
        layout.addWidget(self.combo)

        self.lbl_pv = QLabel()
        self.lbl_ev = QLabel()
        self.lbl_ac = QLabel()
        self.lbl_spi = QLabel()
        self.lbl_cpi = QLabel()

        layout.addWidget(self.lbl_pv)
        layout.addWidget(self.lbl_ev)
        layout.addWidget(self.lbl_ac)
        layout.addWidget(self.lbl_spi)
        layout.addWidget(self.lbl_cpi)

        self.setLayout(layout)
        self.atualizar()

    def atualizar(self):
        obra_id = self.combo.currentData()
        dados = self.evm_controller.calcular_evm(obra_id)
        self.lbl_pv.setText(f"PV (Planejado): R$ {dados.get('PV',0):.2f}")
        self.lbl_ev.setText(f"EV (Agregado): R$ {dados.get('EV',0):.2f}")
        self.lbl_ac.setText(f"AC (Custo Real): R$ {dados.get('AC',0):.2f}")
        self.lbl_spi.setText(f"SPI (Índice de Prazo): {dados.get('SPI',0):.2f}")
        self.lbl_cpi.setText(f"CPI (Índice de Custo): {dados.get('CPI',0):.2f}")
