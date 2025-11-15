import csv
import openpyxl
from datetime import datetime

def exportar_csv(nome_arquivo, dados, colunas):
    with open(nome_arquivo, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(colunas)
        for d in dados:
            writer.writerow([d.get(c, "") for c in colunas])

def exportar_excel(nome_arquivo, dados, colunas):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(colunas)
    for d in dados:
        ws.append([d.get(c, "") for c in colunas])
    wb.save(nome_arquivo)

def today_str():
    return datetime.now().strftime("%Y-%m-%d")
