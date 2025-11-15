from models.despesa_model import DespesaModel

class DespesaController:
    def __init__(self, db):
        self.model = DespesaModel(db)

    def criar_despesa(self, obra_id, categoria, data, valor, descricao):
        return self.model.create(obra_id, categoria, data, valor, descricao)

    def listar_todas(self):
        return self.model.get_all()
