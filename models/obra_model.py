class ObraModel:
    def __init__(self, db):
        self.db = db

    def create(self, nome, cliente=None, endereco=None, data_inicio=None, data_fim_prevista=None, valor_contrato=0.0):
        q = """
        INSERT INTO obras (nome, cliente, endereco, data_inicio, data_fim_prevista, valor_contrato)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        cur = self.db.execute(q, (nome, cliente, endereco, data_inicio, data_fim_prevista, valor_contrato))
        return cur.lastrowid

    def get_all(self):
        return self.db.fetchall("SELECT * FROM obras ORDER BY id DESC")

    def get(self, obra_id):
        return self.db.fetchone("SELECT * FROM obras WHERE id = ?", (obra_id,))

    def update(self, obra_id, **fields):
        cols = []
        vals = []
        for k, v in fields.items():
            cols.append(f"{k} = ?")
            vals.append(v)
        vals.append(obra_id)
        q = f"UPDATE obras SET {', '.join(cols)} WHERE id = ?"
        self.db.execute(q, tuple(vals))

    def delete(self, obra_id):
        self.db.execute("DELETE FROM obras WHERE id = ?", (obra_id,))
