from models.compra_model import CompraModel

class CompraController:
    def __init__(self, db):
        self.model = CompraModel(db)

    def criar_compra(self, material_id, obra_id, quantidade, fornecedor, data_compra, valor_total, status='Em aberto'):
        return self.model.create(material_id, obra_id, quantidade, fornecedor, data_compra, valor_total, status)

    def listar(self):
        return self.model.get_all()

    def deletar(self, compra_id):
        return self.model.delete(compra_id)
