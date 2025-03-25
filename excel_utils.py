import os
import pandas as pd
from format_utils import (
    formatar_data,
    formatar_valor,
    formatar_valor_str,
    normalizar_data
)
from tkinter import messagebox
from datetime import datetime

def obter_semestre(data):
    mes = data.month
    ano = data.year
    return f"{'1sem' if mes <= 6 else '2sem'}_{ano}"

def obter_nome_mes(data):
    return data.strftime("%B").capitalize()

def obter_proximo_id(arquivo, aba):
    if os.path.exists(arquivo):
        try:
            df = pd.read_excel(arquivo, sheet_name=aba)
            if df.empty:
                return 1
            maiores_ids = df["ID"].astype(str).str.extract(r"^(\d+)")
            maiores_ids = maiores_ids.dropna().astype(int)
            return maiores_ids.max().values[0] + 1
        except:
            return 1
    return 1

def salvar_boletos(nome, emissao_str, vencimento_str, valor_str, parcelas_str):
    try:
        data_emissao = normalizar_data(emissao_str)
        data_vencimento = normalizar_data(vencimento_str)
        valor_total = formatar_valor(valor_str)
        valor_formatado = formatar_valor_str(valor_total)
        semestre = obter_semestre(data_emissao)
        nome_mes = obter_nome_mes(data_emissao)
        arquivo = f"boletos_{semestre}.xlsx"

        id_base = obter_proximo_id(arquivo, nome_mes)
        registros = []

        if parcelas_str and parcelas_str.isdigit() and int(parcelas_str) > 1:
            num_parcelas = int(parcelas_str)
            valor_parcela = round(valor_total / num_parcelas, 2)
            valor_parcela_formatado = formatar_valor_str(valor_parcela)

            for i in range(1, num_parcelas + 1):
                registros.append({
                    "ID": f"{id_base}-{i}",
                    "Nome": nome,
                    "Emissão": formatar_data(data_emissao),
                    "Vencimento": formatar_data(data_vencimento),
                    "Valor": valor_parcela_formatado,
                    "Status": "Em Aberto",
                    "Data de Baixa": "",
                    "Parcela": f"{i}/{num_parcelas}"
                })
        else:
            registros.append({
                "ID": str(id_base),
                "Nome": nome,
                "Emissão": formatar_data(data_emissao),
                "Vencimento": formatar_data(data_vencimento),
                "Valor": valor_formatado,
                "Status": "Em Aberto",
                "Data de Baixa": "",
                "Parcela": ""
            })

        df_novo = pd.DataFrame(registros)

        if os.path.exists(arquivo):
            try:
                df_existente = pd.read_excel(arquivo, sheet_name=nome_mes)
                df_final = pd.concat([df_existente, df_novo], ignore_index=True)
            except:
                df_final = df_novo
        else:
            df_final = df_novo

        modo = "a" if os.path.exists(arquivo) else "w"
        if modo == "a":
            with pd.ExcelWriter(arquivo, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
                df_final.to_excel(writer, sheet_name=nome_mes, index=False)
        else:
            with pd.ExcelWriter(arquivo, engine="openpyxl") as writer:
                df_final.to_excel(writer, sheet_name=nome_mes, index=False)

        messagebox.showinfo("Sucesso", "Boleto(s) salvo(s) com sucesso!")

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar boleto:\n{str(e)}")

def buscar_boletos(termo=""):
    resultados = []

    for arquivo in os.listdir():
        if arquivo.startswith("boletos_") and arquivo.endswith(".xlsx"):
            planilha = pd.ExcelFile(arquivo)
            for aba in planilha.sheet_names:
                try:
                    df = pd.read_excel(planilha, sheet_name=aba)
                    if "ID" not in df.columns:
                        continue
                    df = df.fillna("")
                    if termo == "":
                        resultados.append((arquivo, aba, df))
                    else:
                        filtrado = df[
                            df["ID"].astype(str).str.lower().str.contains(termo) |
                            df["Nome"].astype(str).str.lower().str.contains(termo) |
                            df["Vencimento"].astype(str).str.contains(termo)
                        ]
                        if not filtrado.empty:
                            resultados.append((arquivo, aba, filtrado))
                except Exception as e:
                    print(f"Erro ao ler {arquivo} / {aba}: {e}")
    return resultados

def dar_baixa(id_boleto, arquivo, aba):
    hoje = datetime.now().strftime("%d/%m/%Y")

    try:
        df = pd.read_excel(arquivo, sheet_name=aba)
        if "ID" not in df.columns:
            return False
        if id_boleto not in df["ID"].astype(str).values:
            return False

        df.loc[df["ID"].astype(str) == id_boleto, "Status"] = "Pago"
        df.loc[df["ID"].astype(str) == id_boleto, "Data de Baixa"] = hoje

        with pd.ExcelWriter(arquivo, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            df.to_excel(writer, sheet_name=aba, index=False)

        return True

    except Exception as e:
        print(f"Erro ao dar baixa: {e}")
        return False
