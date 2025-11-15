class DespesaModel:
    def __init__(self, db):
        self.db = db

    def create(self, obra_id, categoria, data, valor, descricao):
        q = "INSERT INTO despesas (obra_id, categoria, data, valor, descricao) VALUES (?, ?, ?, ?, ?)"
        cur = self.db.execute(q, (obra_id, categoria, data, valor, descricao))
        return cur.lastrowid

    def get_by_obra(self, obra_id):
        return self.db.fetchall("SELECT * FROM despesas WHERE obra_id = ? ORDER BY data DESC", (obra_id,))

    def get_all(self):
        q = "SELECT d.id, o.nome as obra, d.categoria, d.data, d.valor, d.descricao FROM despesas d LEFT JOIN obras o ON o.id = d.obra_id ORDER BY d.data DESC"
        return self.db.fetchall(q)

    def delete(self, despesa_id):
        self.db.execute("DELETE FROM despesas WHERE id = ?", (despesa_id,))
