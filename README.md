# Medallion Selic Analytics

Uma pipeline de dados completa desenvolvida para extração, transformação e análise de dados da taxa **selic**. Estruturada sob a **arquitetura medalhão (bronze, silver, gold)**

O objetivo desde projeto é automatizar o fluxo completo de dados financeiros macroeconômicos *(Selic, Focus, Copom)* através de uma pipeline estruturada sob a **Medallion architecture**. O repositório demonstra o uso de técnicas de **Data Engineering** para transformar séries temporais brutas em tabelas agregadas e modulares, fornecendo a base para **análises estatísticas.**

---

## Arquitetura Medalhão

A pipeline processa os dados em 3 camadas distintas para garantir linhagem, qualidade e eficiência:

1. **Bronze (Raw Layer):**
    - Ingestão de dados brutos consumidos pela biblioteca **BRdata**.
    - Armazenamento em formato json sem qualquer alteração, preservando os dados originais.

2. **Silver (Cleansed Layer):**
    - Limpeza, tratamento de nulos, tipagem de colunas e deduplicação.
    - Consolidação de séries temporais.
    - Dados salvos em formato **Parquet**.

3. **Gold (Analytical Layer):**
    - Os dados limpos da Camada Silver são persistidos no **DuckDB**, onde são executadas consultas SQL e agregações.
    - Tabelas finais otimizadas para consumo direto.

---

## Ferramentas e Tecnologias

- **Linguagem:** Python 3.12+
- **Gerenciador de Pacotes e Ambientes:** [`uv`](https://github.com/astral-sh/uv)
- **Engine de Dados:** [DuckDB](https://duckdb.org/)
- **Extração de Dados:** [BRdata](https://pypi.org/project/brasil-data/)
- **Manipulação de Dados:** Pandas
- **Gerar gráficos interativos:** Plotly

--

## Como Executar o projeto

### Pré-requisitos

Certifique-se de ter o `uv` instalado em sua máquina Linux/macOS ou Windows. Se ainda não tiver, instale via shell:

```bash
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
```

1. **Clonar Repositório**

```bash
git clone [https://github.com/daviguarisa/medallion-selic-analytics.git](https://github.com/daviguarisa/medallion-selic-analytics.git)
cd medal
```

2. **Sincronizar Ambiente Virtual**

O uv gerenciará a versão do Python e todas as dependências automaticamente a partir do arquivo uv.lock

```bash
uv sync
```

3. **Executar a Pipeline**

```bash
uv run python main.py
```

---

## Estrutura do Projeto

medal/
├── data/
│   ├── bronze/     # Arquivos Parquet brutos
│   └── silver/     # Dados limpos e padronizados (Parquet)
├── notebooks/      # Análises das tabelas finais
│   ├── expectativas_vs_realidade.ipynb
│   └──  predicao_selic.ipynb
├── queries/        # Queries SQL modulares com CTEs para a camada Gold
│   ├── copom_gold.sql
│   ├── expectativa_vs_realidade.sql
│   ├── focus_gold.sql
│   └── selic_gold.sql
├── src/medal/
│   ├── extractors/ # Módulos de download e coleta 
│   ├── transform/  # Módulos de limpeza de dados
│   ├── load/       # Funções do DuckDB
│   ├── pipeline/   # Orquestradores das Camadas (bronze -> silver -> gold)
│   └── utils/      # Funções auxiliares 
├── main.py         # Pipeline Completa
├── pyproject.toml  # Configurações do projeto e dependências
├── uv.lock         # Lockfile determinístico das dependências
└── README.md

---

## Principais Análises Disponíveis (Notebooks)
    
- **Expectativa VS Realidade:** Esta análise realiza uma auditoria histórica de Expectativas Macroeconômicas, comparando retroativamente as projeções do mercado financeiro *(Boletim Focus)* com as decisões reais de taxa de juros adotadas pelo Banco Central do Brasil *(COPOM/Selic)*.

- **Predição Selic:** Ferramenta Operacional Preditiva para as decisões da *Taxa Selic* no *COPOM*. Ele estende a auditoria histórica para o horizonte futuro, calibrando as projeções atuais do mercado financeiro via modelo heurístico e gerando gráficos preditivos interativos.
