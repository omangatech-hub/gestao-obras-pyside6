from models.atividade_model import AtividadeModel

class AtividadeController:
    def __init__(self, db):
        self.model = AtividadeModel(db)

    def criar_atividade(self, obra_id, nome, quantidade_prevista=0, unidade="", custo_unitario=0.0, data_inicio=None, data_fim=None):
        return self.model.create(obra_id, nome, quantidade_prevista, unidade, custo_unitario, data_inicio, data_fim)

    def listar_por_obra(self, obra_id):
        return self.model.get_by_obra(obra_id)

    def atualizar(self, atividade_id, **fields):
        return self.model.update(atividade_id, **fields)

    def excluir(self, atividade_id):
        return self.model.delete(atividade_id)
