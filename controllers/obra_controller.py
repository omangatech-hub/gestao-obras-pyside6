from models.obra_model import ObraModel

class ObraController:
    def __init__(self, db):
        self.model = ObraModel(db)

    def criar_obra(self, nome, cliente=None, endereco=None, data_inicio=None, data_fim_prevista=None, valor_contrato=0.0):
        return self.model.create(nome, cliente, endereco, data_inicio, data_fim_prevista, valor_contrato)

    def listar_obras(self):
        return self.model.get_all()

    def obter_obra(self, obra_id):
        return self.model.get(obra_id)

    def atualizar_obra(self, obra_id, **fields):
        return self.model.update(obra_id, **fields)

    def remover_obra(self, obra_id):
        return self.model.delete(obra_id)
