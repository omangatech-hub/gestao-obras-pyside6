class CompraModel:
    def __init__(self, db):
        self.db = db

    def create(self, material_id, obra_id, quantidade, fornecedor, data_compra, valor_total, status='Em aberto'):
        q = """
        INSERT INTO compras (material_id, obra_id, quantidade, fornecedor, data_compra, valor_total, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        cur = self.db.execute(q, (material_id, obra_id, quantidade, fornecedor, data_compra, valor_total, status))
        return cur.lastrowid

    def get_all(self):
        q = """
        SELECT c.id, m.descricao AS material, c.quantidade, c.fornecedor,
               c.data_compra, c.valor_total, c.status, o.nome AS obra
        FROM compras c
        LEFT JOIN materiais m ON m.id = c.material_id
        LEFT JOIN obras o ON o.id = c.obra_id
        ORDER BY c.data_compra DESC
        """
        return self.db.fetchall(q)

    def delete(self, compra_id):
        self.db.execute("DELETE FROM compras WHERE id = ?", (compra_id,))
