import tkinter as tk
from tkinter import ttk, messagebox
from config import TIPOS_BOLETOS
from excel_utils import salvar_boletos, buscar_boletos, dar_baixa, salvar_boletos_personalizado
from format_utils import normalizar_data, formatar_data

def formatar_e_avancar(event, campo_atual, campo_proximo, formato_data=False):
    if formato_data:
        valor = campo_atual.get().strip()
        try:
            data_formatada = formatar_data(normalizar_data(valor))
            campo_atual.delete(0, tk.END)
            campo_atual.insert(0, data_formatada)
        except:
            messagebox.showerror("Erro", "Data inválida.")
            return
    campo_proximo.focus_set()

def iniciar_interface():
    root = tk.Tk()
    root.title("Cadastro de Boletos")
    largura_janela = 700
    altura_janela = 680

    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()

    pos_x = int((largura_tela - largura_janela) / 2)
    pos_y = max(int((altura_tela - altura_janela) / 2), 20)

    root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
    root.resizable(False, False)

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
            label_nome_boleto.grid()
            entry_nome_boleto.grid()
            label_parcelas.grid()
            entry_parcelas.grid()
            label_vencimento.grid_remove()
            entry_vencimento.grid_remove()
        else:
            label_nome_boleto.grid_remove()
            entry_nome_boleto.grid_remove()
            label_parcelas.grid_remove()
            entry_parcelas.grid_remove()
            label_vencimento.grid()
            entry_vencimento.grid()

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

            popup_vencimentos(
                root=root,
                nome_boleto=nome_personalizado,
                valor_total=entry_valor.get(),
                num_parcelas=parcelas,
                data_emissao=entry_emissao.get()
            )

            limpar_campos()
            return

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

        # Confirmação antes de prosseguir
        confirmar = messagebox.askyesno("Confirmação", "Deseja realmente marcar este boleto como pago?")
        if not confirmar:
            return

        arquivo, aba, id_boleto = linha_para_origem[item_id]
        sucesso = dar_baixa(id_boleto, arquivo, aba)

        if sucesso:
            messagebox.showinfo("Sucesso", f"Boleto {id_boleto} marcado como pago.")
            acao_buscar()
        else:
            messagebox.showerror("Erro", "Não foi possível dar baixa no boleto.")

    def editar_boleto():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione um boleto para editar.")
            return

        item_id = selected[0]
        if item_id not in linha_para_origem:
            messagebox.showerror("Erro", "Origem do boleto não encontrada.")
            return

        valores = tree.item(item_id, "values")
        id_original = valores[0]
        nome = valores[1]
        emissao = valores[2]
        vencimento = valores[3]
        valor = valores[4]

        arquivo, aba, id_boleto = linha_para_origem[item_id]

        popup = tk.Toplevel(root)
        popup.title("Editar Boleto")
        popup.geometry("400x300")
        popup.transient(root)
        popup.grab_set()

        tk.Label(popup, text=f"ID: {id_original}", font=("Arial", 10, "bold")).pack(pady=5)
        frame = tk.Frame(popup)
        frame.pack(pady=10)

        tk.Label(frame, text="Nome:").grid(row=0, column=0, sticky="e")
        entry_nome = tk.Entry(frame, width=30)
        entry_nome.insert(0, nome)
        entry_nome.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Emissão:").grid(row=1, column=0, sticky="e")
        entry_emissao = tk.Entry(frame, width=30)
        entry_emissao.insert(0, emissao)
        entry_emissao.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="Vencimento:").grid(row=2, column=0, sticky="e")
        entry_vencimento = tk.Entry(frame, width=30)
        entry_vencimento.insert(0, vencimento)
        entry_vencimento.grid(row=2, column=1, pady=5)

        tk.Label(frame, text="Valor:").grid(row=3, column=0, sticky="e")
        entry_valor = tk.Entry(frame, width=30)
        entry_valor.insert(0, valor)
        entry_valor.grid(row=3, column=1, pady=5)

        def salvar_edicao():
            novo_nome = entry_nome.get().strip()
            nova_emissao = entry_emissao.get().strip()
            novo_vencimento = entry_vencimento.get().strip()
            novo_valor = entry_valor.get().strip()

            if not novo_nome or not nova_emissao or not novo_vencimento or not novo_valor:
                messagebox.showerror("Erro", "Preencha todos os campos.")
                return

            sucesso = salvar_boletos(
                nome=novo_nome,
                emissao_str=nova_emissao,
                vencimento_str=novo_vencimento,
                valor_str=novo_valor,
                editar_id=id_boleto,
                arquivo_origem=arquivo,
                aba_origem=aba
            )

            if sucesso:
                messagebox.showinfo("Sucesso", "Boleto editado com sucesso.")
                popup.destroy()
                acao_buscar()
            else:
                messagebox.showerror("Erro", "Não foi possível salvar as alterações.")

        tk.Button(popup, text="Salvar Alterações", command=salvar_edicao).pack(pady=15)

    def popup_vencimentos(root, nome_boleto, valor_total, num_parcelas, data_emissao):
        try:
            num_parcelas = int(num_parcelas)
            valor_total = float(valor_total.replace("R$", "").replace(",", "."))
        except:
            messagebox.showerror("Erro", "Número de parcelas ou valor inválido.")
            return

        valor_parcela = round(valor_total / num_parcelas, 2)
        popup = tk.Toplevel(root)
        popup.title("Vencimentos das Parcelas")
        popup.geometry("400x450")

        tk.Label(popup, text=f"Valor por parcela: R$ {valor_parcela:.2f}", font=("Arial", 10, "bold")).pack(pady=10)

        entries = []

        def formatar_e_avancar_popup(event, atual, proximo):
            valor = atual.get().strip()
            try:
                data_formatada = formatar_data(normalizar_data(valor))
                atual.delete(0, tk.END)
                atual.insert(0, data_formatada)
            except:
                messagebox.showerror("Erro", "Data inválida.")
                return
            proximo.focus_set()

        for i in range(num_parcelas):
            frame = tk.Frame(popup)
            frame.pack(pady=2)
            tk.Label(frame, text=f"Parcela {i+1}/{num_parcelas} - Vencimento:").pack(side=tk.LEFT)
            entry = tk.Entry(frame)
            entry.pack(side=tk.LEFT)
            entries.append(entry)

        for i in range(len(entries)):
            if i < len(entries) - 1:
                entries[i].bind("<Return>", lambda e, idx=i: formatar_e_avancar_popup(e, entries[idx], entries[idx+1]))
            else:
                entries[i].bind("<Return>", lambda e, idx=i: formatar_e_avancar_popup(e, entries[idx], entries[idx]))

        def confirmar():
            datas_vencimentos = [e.get().strip() for e in entries]
            if any(not d for d in datas_vencimentos):
                messagebox.showerror("Erro", "Preencha todas as datas de vencimento.")
                return

            salvar_boletos_personalizado(
                nome=nome_boleto,
                data_emissao=data_emissao,
                valor_total=valor_total,
                vencimentos=datas_vencimentos
            )
            popup.destroy()

        tk.Button(popup, text="Confirmar", command=confirmar).pack(pady=20)
        popup.transient(root)
        popup.grab_set()
        root.wait_window(popup)

    # INTERFACE
    tk.Label(root, text="Cadastro de Boletos", font=("Arial", 14, "bold")).pack(pady=10)

    form_frame = tk.Frame(root)
    form_frame.pack(pady=5)

    tk.Label(form_frame, text="Tipo de Boleto:").grid(row=0, column=0, sticky="w")
    combo_nome = ttk.Combobox(form_frame, values=TIPOS_BOLETOS, state="readonly", width=30)
    combo_nome.grid(row=0, column=1, padx=5, pady=3, sticky="w")
    combo_nome.bind("<<ComboboxSelected>>", verificar_boletos_faturados)

    label_nome_boleto = tk.Label(form_frame, text="Nome do Boleto:")
    label_nome_boleto.grid(row=1, column=0, sticky="w")
    entry_nome_boleto = tk.Entry(form_frame, width=33)
    entry_nome_boleto.grid(row=1, column=1, padx=5, pady=3, sticky="w")
    label_nome_boleto.grid_remove()
    entry_nome_boleto.grid_remove()

    label_parcelas = tk.Label(form_frame, text="Nº Parcelas:")
    label_parcelas.grid(row=2, column=0, sticky="w")
    entry_parcelas = tk.Entry(form_frame, width=10)
    entry_parcelas.grid(row=2, column=1, padx=5, pady=3, sticky="w")
    label_parcelas.grid_remove()
    entry_parcelas.grid_remove()

    tk.Label(form_frame, text="Data de Emissão:").grid(row=3, column=0, sticky="w")
    entry_emissao = tk.Entry(form_frame, width=20)
    entry_emissao.grid(row=3, column=1, padx=5, pady=3, sticky="w")

    label_vencimento = tk.Label(form_frame, text="Data de Vencimento:")
    label_vencimento.grid(row=4, column=0, sticky="w")
    entry_vencimento = tk.Entry(form_frame, width=20)
    entry_vencimento.grid(row=4, column=1, padx=5, pady=3, sticky="w")

    tk.Label(form_frame, text="Valor Total (R$):").grid(row=5, column=0, sticky="w")
    entry_valor = tk.Entry(form_frame, width=20)
    entry_valor.grid(row=5, column=1, padx=5, pady=3, sticky="w")

    # Binds corrigidos
    entry_nome_boleto.bind("<Return>", lambda e: formatar_e_avancar(e, entry_nome_boleto, entry_emissao))
    entry_parcelas.bind("<Return>", lambda e: formatar_e_avancar(e, entry_parcelas, entry_emissao))
    entry_emissao.bind("<Return>", lambda e: formatar_e_avancar(e, entry_emissao, entry_vencimento, formato_data=True))
    entry_vencimento.bind("<Return>", lambda e: formatar_e_avancar(e, entry_vencimento, entry_valor, formato_data=True))
    entry_valor.bind("<Return>", lambda e: formatar_e_avancar(e, entry_valor, entry_busca))

    tk.Button(root, text="Salvar Boleto", command=acao_salvar).pack(pady=10)

    tk.Label(root, text="Buscar por ID, Nome ou Vencimento (vazio = todos):").pack()
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
    tk.Button(root, text="Editar Boleto Selecionado", command=editar_boleto).pack(pady=5)


    root.mainloop()
