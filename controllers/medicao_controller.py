from models.medicao_model import MedicaoModel

class MedicaoController:
    def __init__(self, db):
        self.model = MedicaoModel(db)

    def criar_medicao(self, atividade_id, data, quantidade_executada, observacao=None):
        return self.model.create(atividade_id, data, quantidade_executada, observacao)

    def listar_por_atividade(self, atividade_id):
        return self.model.get_by_atividade(atividade_id)

    def excluir(self, medicao_id):
        return self.model.delete(medicao_id)
