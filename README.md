# 📘 Sistema de Registro e Controle de Boletos

Este é um sistema desenvolvido em Python com interface gráfica (Tkinter) para **cadastrar, buscar e gerenciar boletos** em planilhas Excel. Ele é ideal para pequenas empresas ou uso pessoal, permitindo organizar pagamentos por semestre, gerar parcelas automaticamente, controlar vencimentos e registrar quitações de forma prática.

---

## ✅ Funcionalidades

### 📋 Cadastro de Boletos
- Seleção de tipos fixos: TINY, Linx, EDP, Aluguel, Vivo, Correios, SABESP, Boletos Faturados.
- Inserção de:
  - Data de emissão
  - Data de vencimento
  - Valor (com formatação `R$`)
- Suporte a múltiplas parcelas (Boletos Faturados), com divisão automática de valores.
- ID sequencial gerado automaticamente (`23`, `23-1`, `23-2`, etc).
- Nome personalizado para Boletos Faturados.
- Armazenamento em arquivos Excel separados por semestre (ex: `boletos_1sem_2025.xlsx`) e organizados por abas mensais (`Janeiro`, `Fevereiro`, etc).

### 🔍 Busca de Boletos
- Campo de busca por:
  - Nome do boleto
  - Data de vencimento
  - ID do boleto (ex: `23`, `23-1`)
- Se a busca for deixada em branco, exibe **todos os boletos cadastrados**.

### ✅ Dar Baixa em Boletos
- Seleção de boleto e alteração do status para **"Pago"**.
- Registro automático da data de baixa.
- Baixa feita com **precisão de origem** (arquivo + mês) para evitar conflitos entre meses e semestres.

---

## ⚙️ Tecnologias Utilizadas

- Python 3.12+
- Tkinter (interface gráfica)
- Pandas + OpenPyXL (para manipulação de planilhas Excel)

---

## 📂 Estrutura do Projeto

```
📁 registro_boletos/
├── main.py                 # Executa o sistema
├── interface.py            # Interface Tkinter
├── excel_utils.py          # Lógica de leitura e escrita em Excel
├── format_utils.py         # Tratamento de datas e valores
├── config.py               # Lista de tipos de boletos
├── boletos_1sem_2025.xlsx  # (Exemplo gerado) Planilha com boletos
```

---

## ⚠️ Dificuldades e Soluções

### 🔁 IDs duplicados entre meses/semestres
- IDs numéricos podem se repetir, por isso implementamos:
  - **Mapeamento completo** entre `ID + mês + arquivo`
  - A função `dar_baixa` atua com precisão no local correto

### 📆 Formato de datas flexível
- O sistema aceita `01/02/2025`, `01.02.2025` ou `01022025`, padronizando internamente para `DD/MM/AAAA`.

### 📊 Interface Tkinter
- Evitamos conflitos entre `pack()` e `grid()` ao refatorar o layout para usar `grid()` consistentemente.

### 🔄 Pesquisa exibida diretamente na interface
- Removemos prints no terminal e implementamos `Treeview` com carregamento dinâmico e responsivo.

---

## 🚀 Como Executar

1. Instale as dependências:
```bash
pip install pandas openpyxl
```

2. Execute o sistema:
```bash
python main.py
```

---

## 📅 Última atualização
25/03/2025
