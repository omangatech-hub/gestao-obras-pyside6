class EVMModel:
    def __init__(self, db):
        self.db = db

    def calcular_evm(self, obra_id):
        pv = self.db.fetchone("""
            SELECT SUM(quantidade_prevista * custo_unitario) AS pv
            FROM atividades
            WHERE obra_id = ?
        """, (obra_id,))

        ev = self.db.fetchone("""
            SELECT SUM(medicoes.quantidade_executada * atividades.custo_unitario) AS ev
            FROM medicoes
            JOIN atividades ON atividades.id = medicoes.atividade_id
            WHERE atividades.obra_id = ?
        """, (obra_id,))

        ac = self.db.fetchone("""
            SELECT SUM(valor) AS ac
            FROM despesas
            WHERE obra_id = ?
        """, (obra_id,))

        pv = pv.get('pv') if pv else None
        ev = ev.get('ev') if ev else None
        ac = ac.get('ac') if ac else None
        
        pv = float(pv) if pv is not None else 0
        ev = float(ev) if ev is not None else 0
        ac = float(ac) if ac is not None else 0

        cpi = (ev / ac) if ac > 0 else 0
        spi = (ev / pv) if pv > 0 else 0

        return {"PV": pv or 0, "EV": ev or 0, "AC": ac or 0, "CPI": cpi, "SPI": spi}
