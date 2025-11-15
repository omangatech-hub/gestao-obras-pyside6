class AtividadeModel:
    def __init__(self, db):
        self.db = db

    def create(self, obra_id, nome, quantidade_prevista=0, unidade="", custo_unitario=0.0, data_inicio=None, data_fim=None):
        q = """
        INSERT INTO atividades (obra_id, nome, quantidade_prevista, unidade, custo_unitario, data_inicio, data_fim)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        cur = self.db.execute(q, (obra_id, nome, quantidade_prevista, unidade, custo_unitario, data_inicio, data_fim))
        return cur.lastrowid

    def get_by_obra(self, obra_id):
        return self.db.fetchall("SELECT * FROM atividades WHERE obra_id = ? ORDER BY id", (obra_id,))

    def get(self, atividade_id):
        return self.db.fetchone("SELECT * FROM atividades WHERE id = ?", (atividade_id,))

    def update(self, atividade_id, **fields):
        cols = []
        vals = []
        for k, v in fields.items():
            cols.append(f"{k} = ?")
            vals.append(v)
        vals.append(atividade_id)
        q = f"UPDATE atividades SET {', '.join(cols)} WHERE id = ?"
        self.db.execute(q, tuple(vals))

    def delete(self, atividade_id):
        self.db.execute("DELETE FROM atividades WHERE id = ?", (atividade_id,))
