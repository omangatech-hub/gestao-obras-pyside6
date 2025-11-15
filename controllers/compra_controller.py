from models.compra_model import CompraModel

class CompraController:
    def __init__(self, db, material_controller=None, obra_controller=None):
        self.model = CompraModel(db)
        self.material_controller = material_controller
        self.obra_controller = obra_controller

    def criar_compra(self, material_id, obra_id, quantidade, fornecedor, data_compra, valor_total, status='Em aberto'):
        return self.model.create(material_id, obra_id, quantidade, fornecedor, data_compra, valor_total, status)

    def listar(self):
        return self.model.get_all()

    def listar_materiais(self):
        """Retorna lista de materiais para seleção em compras"""
        if self.material_controller:
            return self.material_controller.listar()
        return []

    def listar_obras(self):
        """Retorna lista de obras para seleção em compras"""
        if self.obra_controller:
            return self.obra_controller.listar_obras()
        return []

    def deletar(self, compra_id):
        return self.model.delete(compra_id)
