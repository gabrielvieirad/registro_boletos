import tkinter as tk
from tkinter import ttk, messagebox
from config import TIPOS_BOLETOS
from excel_utils import salvar_boletos, buscar_boletos, dar_baixa

def iniciar_interface():
    root = tk.Tk()
    root.title("Cadastro de Boletos")
    root.geometry("600x700")

    # Mapeia ID da Treeview → (arquivo, aba)
    linha_para_origem = {}

    def limpar_campos():
        combo_nome.set("")
        entry_nome_boleto.delete(0, tk.END)
        entry_emissao.delete(0, tk.END)
        entry_vencimento.delete(0, tk.END)
        entry_valor.delete(0, tk.END)
        entry_parcelas.delete(0, tk.END)
        entry_nome_boleto.grid_remove()
        entry_parcelas.grid_remove()
        tree.delete(*tree.get_children())
        linha_para_origem.clear()

    def verificar_boletos_faturados(event):
        tipo = combo_nome.get()
        if tipo == "Boletos Faturados":
            entry_nome_boleto.grid()
            entry_parcelas.grid()
        else:
            entry_nome_boleto.grid_remove()
            entry_parcelas.grid_remove()

    def acao_salvar():
        nome_tipo = combo_nome.get().strip()
        if not nome_tipo:
            messagebox.showerror("Erro", "Selecione o tipo de boleto.")
            return

        if nome_tipo == "Boletos Faturados":
            nome_personalizado = entry_nome_boleto.get().strip()
            if not nome_personalizado:
                messagebox.showerror("Erro", "Informe o nome do boleto faturado.")
                return
            parcelas = entry_parcelas.get().strip()
            if not parcelas.isdigit() or int(parcelas) < 1:
                messagebox.showerror("Erro", "Informe o número de parcelas válido.")
                return
        else:
            nome_personalizado = nome_tipo
            parcelas = ""

        if not entry_emissao.get().strip() or not entry_vencimento.get().strip() or not entry_valor.get().strip():
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios.")
            return

        salvar_boletos(
            nome_personalizado,
            entry_emissao.get(),
            entry_vencimento.get(),
            entry_valor.get(),
            parcelas
        )
        limpar_campos()

    def acao_buscar():
        termo = entry_busca.get().strip().lower()
        tree.delete(*tree.get_children())
        linha_para_origem.clear()

        resultados = buscar_boletos(termo)
        for arquivo, aba, df in resultados:
            for _, row in df.iterrows():
                item_id = tree.insert("", tk.END, values=(
                    str(row.get("ID", "")),
                    str(row.get("Nome", "")),
                    str(row.get("Emissão", "")),
                    str(row.get("Vencimento", "")),
                    str(row.get("Valor", "")),
                    str(row.get("Status", "")),
                    str(row.get("Parcela", ""))
                ))
                linha_para_origem[item_id] = (arquivo, aba, str(row.get("ID", "")))

    def acao_dar_baixa():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione um boleto para dar baixa.")
            return

        item_id = selected[0]
        if item_id not in linha_para_origem:
            messagebox.showerror("Erro", "Origem do boleto não encontrada.")
            return

        arquivo, aba, id_boleto = linha_para_origem[item_id]
        sucesso = dar_baixa(id_boleto, arquivo, aba)

        if sucesso:
            messagebox.showinfo("Sucesso", f"Boleto {id_boleto} marcado como pago.")
            acao_buscar()
        else:
            messagebox.showerror("Erro", "Não foi possível dar baixa no boleto.")

    def pular_campo(event, proximo_widget):
        proximo_widget.focus()

    # ---------- INTERFACE GRÁFICA ----------
    tk.Label(root, text="Cadastro de Boletos", font=("Arial", 14, "bold")).pack(pady=10)

    form_frame = tk.Frame(root)
    form_frame.pack(pady=5)

    tk.Label(form_frame, text="Tipo de Boleto:").grid(row=0, column=0, sticky="w")
    combo_nome = ttk.Combobox(form_frame, values=TIPOS_BOLETOS, state="readonly", width=30)
    combo_nome.grid(row=0, column=1, padx=5, pady=3, sticky="w")
    combo_nome.bind("<<ComboboxSelected>>", verificar_boletos_faturados)

    tk.Label(form_frame, text="Nome do Boleto:").grid(row=1, column=0, sticky="w")
    entry_nome_boleto = tk.Entry(form_frame, width=33)
    entry_nome_boleto.grid(row=1, column=1, padx=5, pady=3, sticky="w")
    entry_nome_boleto.grid_remove()

    tk.Label(form_frame, text="Nº Parcelas:").grid(row=2, column=0, sticky="w")
    entry_parcelas = tk.Entry(form_frame, width=10)
    entry_parcelas.grid(row=2, column=1, padx=5, pady=3, sticky="w")
    entry_parcelas.grid_remove()

    tk.Label(form_frame, text="Data de Emissão:").grid(row=3, column=0, sticky="w")
    entry_emissao = tk.Entry(form_frame, width=20)
    entry_emissao.grid(row=3, column=1, padx=5, pady=3, sticky="w")

    tk.Label(form_frame, text="Data de Vencimento:").grid(row=4, column=0, sticky="w")
    entry_vencimento = tk.Entry(form_frame, width=20)
    entry_vencimento.grid(row=4, column=1, padx=5, pady=3, sticky="w")

    tk.Label(form_frame, text="Valor Total (R$):").grid(row=5, column=0, sticky="w")
    entry_valor = tk.Entry(form_frame, width=20)
    entry_valor.grid(row=5, column=1, padx=5, pady=3, sticky="w")

    entry_nome_boleto.bind("<Return>", lambda e: pular_campo(e, entry_emissao))
    entry_emissao.bind("<Return>", lambda e: pular_campo(e, entry_vencimento))
    entry_vencimento.bind("<Return>", lambda e: pular_campo(e, entry_valor))
    entry_valor.bind("<Return>", lambda e: pular_campo(e, entry_parcelas))
    entry_parcelas.bind("<Return>", lambda e: pular_campo(e, entry_busca))

    tk.Button(root, text="Salvar Boleto", command=acao_salvar).pack(pady=10)

    tk.Label(root, text="🔍 Buscar por ID, Nome ou Vencimento (vazio = todos):").pack()
    entry_busca = tk.Entry(root)
    entry_busca.pack()
    tk.Button(root, text="Buscar", command=acao_buscar).pack(pady=5)

    colunas = ("ID", "Nome", "Emissão", "Vencimento", "Valor", "Status", "Parcela")
    tree = ttk.Treeview(root, columns=colunas, show="headings", height=12)
    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER, width=80)
    tree.pack(pady=10, fill=tk.BOTH, expand=True)

    tk.Button(root, text="Dar Baixa no Boleto Selecionado", command=acao_dar_baixa).pack(pady=5)

    root.mainloop()
