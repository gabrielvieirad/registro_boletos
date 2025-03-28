# Registro de Boletos

Aplicativo desenvolvido em Python com interface gráfica utilizando Tkinter para controle e registro de boletos diversos. Permite o cadastro, visualização, busca, baixa e controle de boletos parcelados, com armazenamento em planilhas Excel.

---

## ✅ Funcionalidades

- Cadastro de boletos com tipo, data de emissão, vencimento e valor.
- Suporte a boletos parcelados com controle individual de vencimentos.
- Interface dinâmica: campos exibidos de acordo com o tipo de boleto selecionado.
- Busca por ID, nome ou data de vencimento.
- Marcação de boletos como pagos diretamente pela interface.
- Armazenamento em planilhas organizadas por semestre e mês de vencimento.
- Com salvamento automático na Área de Trabalho!


---

## 🖥️ Interface Gráfica

- Layout redesenhado com alinhamento consistente e responsivo.
- Janela principal centralizada automaticamente na tela, com ajuste para não sobrepor a barra de tarefas.
- Todos os campos organizados com espaçamento visual adequado.
- O botão "Dar Baixa no Boleto Selecionado" permanece sempre visível, sem necessidade de redimensionar a janela.
- Campos "Nome do Boleto" e "Nº Parcelas" são exibidos apenas quando o tipo selecionado for "Boletos Faturados".
- Formatação automática de datas: aceita formatos como `01012025`, `01/01/2025`, `01.01.2025`.
- Navegação com a tecla Enter entre campos, com formatação automática aplicada nos campos de data.

---

## 📁 Armazenamento dos Dados

- Todos os boletos são armazenados em arquivos Excel organizados por semestre e mês de vencimento.
- Os arquivos são salvos automaticamente em uma pasta `Boletos_Registrados`, criada na Área de Trabalho do sistema.
- Para boletos parcelados, cada parcela possui vencimento próprio, com controle individual.
- IDs são únicos por planilha, com rastreabilidade mantida mesmo entre meses e semestres.


---

## 🛠️ Tecnologias Utilizadas

- Python 3.12+
- Tkinter (interface gráfica)
- Pandas (manipulação de planilhas)
- openpyxl (leitura e escrita em arquivos Excel)

---

## 🚀 Execução

Para iniciar a aplicação:

```bash
python main.py
```

---

## 📌 Requisitos

- Python 3.12 ou superior instalado
- Bibliotecas: `pandas`, `openpyxl`

Você pode instalar as dependências com:

```bash
pip install -r requirements.txt
```

---

## 📎 Observações

- O projeto é modular e permite expansão futura para controle de outros documentos financeiros.
- Interface pensada para uso contínuo, com foco em usabilidade, clareza visual e estabilidade.

---
