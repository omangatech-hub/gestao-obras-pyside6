import sqlite3
import os

class Database:
    def __init__(self, db_name="gestao_obras.db"):
        base_dir = os.path.dirname(__file__)
        self.db_path = os.path.join(base_dir, db_name)
        # ensure folder exists
        os.makedirs(base_dir, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

    def execute(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        return cursor

    def fetchall(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def fetchone(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else None

    def create_tables(self):
        tables = [
            """
            CREATE TABLE IF NOT EXISTS obras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cliente TEXT,
                endereco TEXT,
                data_inicio TEXT,
                data_fim_prevista TEXT,
                valor_contrato REAL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS atividades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                obra_id INTEGER NOT NULL,
                nome TEXT,
                quantidade_prevista REAL,
                unidade TEXT,
                custo_unitario REAL,
                data_inicio TEXT,
                data_fim TEXT,
                FOREIGN KEY (obra_id) REFERENCES obras(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS medicoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                atividade_id INTEGER NOT NULL,
                data TEXT,
                quantidade_executada REAL,
                observacao TEXT,
                FOREIGN KEY (atividade_id) REFERENCES atividades(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS materiais (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT,
                descricao TEXT,
                unidade TEXT
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS compras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                material_id INTEGER,
                obra_id INTEGER,
                quantidade REAL,
                fornecedor TEXT,
                data_compra TEXT,
                valor_total REAL,
                status TEXT,
                FOREIGN KEY (material_id) REFERENCES materiais(id) ON DELETE SET NULL,
                FOREIGN KEY (obra_id) REFERENCES obras(id) ON DELETE SET NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS despesas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                obra_id INTEGER NOT NULL,
                categoria TEXT,
                data TEXT,
                valor REAL,
                descricao TEXT,
                FOREIGN KEY (obra_id) REFERENCES obras(id) ON DELETE CASCADE
            );
            """
        ]

        for table in tables:
            self.execute(table)
