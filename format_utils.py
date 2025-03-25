import re
from datetime import datetime

def normalizar_data(data_str):
    data_str = re.sub(r"[^\d]", "", data_str)
    if len(data_str) == 8:
        return datetime.strptime(data_str, "%d%m%Y")
    raise ValueError("Data inválida")

def formatar_data(data_obj):
    return data_obj.strftime("%d/%m/%Y")

def formatar_valor(valor_str):
    valor_str = valor_str.replace(",", ".").replace("R$", "").strip()
    return round(float(valor_str), 2)

def formatar_valor_str(valor):
    return f"R$ {valor:,.2f}".replace(".", "#").replace(",", ".").replace("#", ",")
