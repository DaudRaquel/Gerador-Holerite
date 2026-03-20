# 🧾 Gerador de Holerites — TOTVS RM + ReportLab

Geração automática de holerites em PDF com dados extraídos do TOTVS RM (Oracle). Calcula INSS, IRRF e FGTS de forma progressiva e organiza os arquivos por departamento.

## ✨ Funcionalidades

- Extração de dados de funcionários ativos do TOTVS RM (Oracle)
- Cálculo progressivo de INSS, IRRF e FGTS
- Geração de PDFs formatados por competência
- Organização automática em pastas por departamento
- Modo `--mock` para testes sem banco

## 🛠️ Stack

`Python` · `Oracle (cx_Oracle)` · `ReportLab` · `python-dotenv`

## 📁 Estrutura

```
Gerador-Holerite/
├── main.py
├── database/
│   ├── conexao.py          # Conexão Oracle
│   └── mock_data.py        # Dados fictícios
├── utils/
│   └── calculos.py         # INSS, IRRF, FGTS
├── pdf/
│   └── gerador_holerite.py # PDF com ReportLab
├── .env.example
└── requirements.txt
```

## 🚀 Como rodar

```bash
pip install -r requirements.txt
cp .env.example .env

python main.py --mock    # teste
python main.py           # produção
```

---
Desenvolvido por **Raquel Daud** — [LinkedIn](https://www.linkedin.com/in/raquel-daud-72a3991a2/)
