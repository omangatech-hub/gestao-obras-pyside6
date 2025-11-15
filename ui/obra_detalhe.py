from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QTabWidget, QWidget, QFormLayout
from ui.atividades_view import AtividadesView
from ui.medicoes_view import MedicoesView

class ObraDetalhe(QDialog):
    def __init__(self, obra, atividade_controller, medicao_controller, parent=None):
        super().__init__(parent)
        self.obra = obra
        self.atividade_controller = atividade_controller
        self.medicao_controller = medicao_controller
        self.setWindowTitle(f"Obra - {obra.get('nome')}")
        self.resize(900, 600)
        layout = QVBoxLayout()
        header = QLabel(f"<b>{obra.get('nome')}</b><br>Cliente: {obra.get('cliente') or ''}<br>Endereço: {obra.get('endereco') or ''}")
        layout.addWidget(header)

        tabs = QTabWidget()
        self.tabResumo = QWidget()
        self.tabAtividades = AtividadesView(obra.get("id"), atividade_controller, medicao_controller)
        self.tabMedicoes = MedicoesView(obra.get("id"), atividade_controller, medicao_controller)

        tabs.addTab(self.tabResumo, "Resumo")
        tabs.addTab(self.tabAtividades, "Atividades")
        tabs.addTab(self.tabMedicoes, "Medições")

        # resumo simples
        rlayout = QFormLayout()
        from PySide6.QtWidgets import QLabel as QL
        rlayout.addRow("Valor Contrato:", QL(f"R$ {obra.get('valor_contrato') or 0:.2f}"))
        rlayout.addRow("Data Início:", QL(obra.get('data_inicio') or ""))
        rlayout.addRow("Data Fim Prev.:", QL(obra.get('data_fim_prevista') or ""))
        self.tabResumo.setLayout(rlayout)

        layout.addWidget(tabs)
        self.setLayout(layout)
