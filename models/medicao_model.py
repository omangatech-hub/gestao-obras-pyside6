class MedicaoModel:
    def __init__(self, db):
        self.db = db

    def create(self, atividade_id, data, quantidade_executada, observacao=None):
        q = """
        INSERT INTO medicoes (atividade_id, data, quantidade_executada, observacao)
        VALUES (?, ?, ?, ?)
        """
        cur = self.db.execute(q, (atividade_id, data, quantidade_executada, observacao))
        return cur.lastrowid

    def get_by_atividade(self, atividade_id):
        return self.db.fetchall("SELECT * FROM medicoes WHERE atividade_id = ? ORDER BY data DESC", (atividade_id,))

    def get(self, medicao_id):
        return self.db.fetchone("SELECT * FROM medicoes WHERE id = ?", (medicao_id,))

    def delete(self, medicao_id):
        self.db.execute("DELETE FROM medicoes WHERE id = ?", (medicao_id,))
