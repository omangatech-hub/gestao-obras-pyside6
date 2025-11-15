class MaterialModel:
    def __init__(self, db):
        self.db = db

    def create(self, codigo, descricao, unidade, estoque=0):
        q = "INSERT INTO materiais (codigo, descricao, unidade, estoque) VALUES (?, ?, ?, ?)"
        cur = self.db.execute(q, (codigo, descricao, unidade, estoque))
        return cur.lastrowid

    def get_all(self):
        return self.db.fetchall("SELECT * FROM materiais ORDER BY descricao")

    def get(self, material_id):
        return self.db.fetchone("SELECT * FROM materiais WHERE id = ?", (material_id,))

    def update(self, material_id, **fields):
        cols = []
        vals = []
        for k, v in fields.items():
            cols.append(f"{k} = ?")
            vals.append(v)
        vals.append(material_id)
        q = f"UPDATE materiais SET {', '.join(cols)} WHERE id = ?"
        self.db.execute(q, tuple(vals))

    def adjust_stock(self, material_id, delta):
        self.db.execute("UPDATE materiais SET estoque = estoque + ? WHERE id = ?", (delta, material_id))

    def delete(self, material_id):
        self.db.execute("DELETE FROM materiais WHERE id = ?", (material_id,))
