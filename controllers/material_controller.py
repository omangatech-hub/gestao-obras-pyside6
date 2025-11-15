from models.material_model import MaterialModel

class MaterialController:
    def __init__(self, db):
        self.model = MaterialModel(db)

    def criar_material(self, codigo, descricao, unidade, estoque=0):
        return self.model.create(codigo, descricao, unidade, estoque)

    def listar(self):
        return self.model.get_all()

    def ajustar_estoque(self, material_id, delta):
        return self.model.adjust_stock(material_id, delta)

    def atualizar(self, material_id, **fields):
        return self.model.update(material_id, **fields)

    def obter(self, material_id):
        return self.model.get(material_id)
