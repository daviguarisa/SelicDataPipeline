import logging
import pandas as pd
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s"
)

def transform_selic_silver(
        input_path: str = "data/bronze/selic",
        output_path: str = "data/silver/selic.parquet"
) -> None:
    """
    Lê arquivos brutos da Selic Meta na Camada Bronze, realiza a limpeza, tipagem,
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
    df.columns = [col.strip().lower() for col in df.columns]

    coluna_data = "data" if "data" in df.columns else df.columns[0]
    df[coluna_data] = pd.to_datetime(
        df[coluna_data],
        format="%d/%m/%Y",
        errors="coerce"
    ).fillna(pd.to_datetime(df[coluna_data], errors="coerce"))

    coluna_valor = "valor" if "valor" in df.columns else df.columns[1]
    if df[coluna_valor].dtype == "object":
        df[coluna_valor] = df[coluna_valor].astype(str).str.replace(",", ".")

    df[coluna_valor] = pd.to_numeric(df[coluna_valor], errors="coerce")

    df = df.rename(columns={
        coluna_data: "data",
        coluna_valor: "selic_meta"
    })

    df = df.dropna(subset=["data", "selic_meta"])
    df = df.drop_duplicates(subset=["data"]).sort_values(by="data").reset_index(drop=True)

    # Salva em Parquet
    df.to_parquet(output_file, index=False, engine="pyarrow")
    logging.info(f"Camada Silver (Selic) gerada em: '{output_file}'")