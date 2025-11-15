from models.material_model import MaterialModel

class MaterialController:
    def __init__(self, db):
        self.model = MaterialModel(db)

    def criar_material(self, codigo, descricao, unidade):
        return self.model.criar_material(codigo, descricao, unidade)

    def listar(self):
        return self.model.get_all()

    def atualizar(self, material_id, **fields):
        return self.model.update(material_id, **fields)

    def obter(self, material_id):
        return self.model.get(material_id)
