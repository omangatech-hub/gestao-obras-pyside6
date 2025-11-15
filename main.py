import sys
from PySide6.QtWidgets import QApplication
from database.db import Database
from controllers.obra_controller import ObraController
from controllers.atividade_controller import AtividadeController
from controllers.medicao_controller import MedicaoController
from controllers.material_controller import MaterialController
from controllers.compra_controller import CompraController
from controllers.despesa_controller import DespesaController
from controllers.despesa_controller import DespesaController as DespCtrl
from models.evm_model import EVMModel
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)

    # DB
    db = Database()

    # controllers
    obra_ctrl = ObraController(db)
    atividade_ctrl = AtividadeController(db)
    medicao_ctrl = MedicaoController(db)
    material_ctrl = MaterialController(db)
    compra_ctrl = CompraController(db)
    despesa_ctrl = DespesaController(db)
    evm_model = EVMModel(db)

    controllers = {
        'obra': obra_ctrl,
        'atividade': atividade_ctrl,
        'medicao': medicao_ctrl,
        'material': material_ctrl,
        'compra': compra_ctrl,
        'despesa': despesa_ctrl,
        'evm': evm_model
    }

    # main window
    win = MainWindow(controllers)
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
