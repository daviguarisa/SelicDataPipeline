import logging
import pandas as pd
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s"
)

def transform_copom_silver(
        input_path: str = "data/bronze/copom",
        output_path: str = "data/silver/copom.parquet"
) -> None:
    """
    Lê arquivos brutos da Tabela de Reuniões do Copom na Camada Bronze, realiza a limpeza, tipagem,
    remoção de duplicatas e salva em Parquet na Camada Silver.
    """
    # configuração de caminhos
    bronze_path = Path(input_path)
    output_file = Path(output_path)

    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Leitura e Concatenação
    arquivos = list(bronze_path.glob("*.json"))
    if not arquivos:
        logging.warning(f"Nenhum arquivo encontrado em {input_path}")
        return
    
    dfs = []
    for arquivo in arquivos:
        try:
            df_temp = pd.read_json(arquivo)
    
            if not df_temp.empty:
                dfs.append(df_temp)
    
        except Exception as e:
            logging.error(f"Erro ao ler o arquivo {arquivo.name}: {e}")
    
    if not dfs:
        logging.error("Nenhum dado válido foi carregado!")
    
    df = pd.concat(dfs, ignore_index=True)

    # Padronização, conversão de tipos, limpeza e ordenação
    df.drop_duplicates()

    df["reuniao_index"] = (
        df["reuniao_num"].str.extract(r"(\d+)")[0].astype("Int64")
    )
    df.drop(columns=["reuniao_num"], inplace=True)

    df["reuniao_data"] = pd.to_datetime(
        df["reuniao_data"], format="%d/%m/%Y", errors="coerce"
    ).dt.date

    df = df.sort_values("reuniao_data", ascending=True).reset_index(drop=True)

    df["reuniao_ano"] = pd.to_datetime(df["reuniao_data"]).dt.year.astype("Int64")
    df["reuniao_num"] = (
        df.groupby("reuniao_ano").cumcount() + 1
    ).astype("Int64")

    df = df.sort_values("reuniao_data", ascending=False).reset_index(drop=True)

    vigencia_split = df["vigencia"].str.split("-", expand=True)

    df["vigencia_inicio"] = pd.to_datetime(
        vigencia_split[0].str.strip(), format="%d/%m/%Y", errors="coerce"
    ).dt.date

    df["vigencia_fim"] = pd.to_datetime(
        vigencia_split[1].str.strip(), format="%d/%m/%Y", errors="coerce"
    ).dt.date

    colunas_float = ["meta_selic", "taxa_selic_pct", "taxa_selic_aa"]
    for col in colunas_float:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").round(2)

    df.drop(columns=["vigencia", "vies", "tban"], inplace=True, errors="ignore")

    colunas = [
        "reuniao_index",
        "reuniao_num",
        "reuniao_ano",
        "reuniao_data",
        "vigencia_inicio",
        "vigencia_fim",
        "meta_selic",
        "taxa_selic_pct",
        "taxa_selic_aa",
    ]
    df = df[colunas]

    # Salva em Parquet
    df.to_parquet(output_file, index=False, engine="pyarrow")
    logging.info(f"Camada Silver (Copom) gerada em: '{output_file}'")
