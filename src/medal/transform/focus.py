from pathlib import Path
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def transform_focus_silver(
        input_path: str = "data/bronze/focus",
        output_path: str = "data/silver/focus.parquet"
) -> None:
    """
    Lê arquivos brutos do Boletim Focus da Camada Bronze, realiza a limpeza, tipagem,
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

    colunas_data = [col for col in df.columns if 'data' in col]
    for col in colunas_data:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    colunas_metricas = ["mediana", "media", "desviopadrao", "minimo", "maximo"]
    for col in colunas_metricas:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.drop_duplicates()
    coluna_data_principal = colunas_data[0] if colunas_data else df.columns[0]
    df = df.sort_values(by=coluna_data_principal).reset_index(drop=True)

    # Salva em Parquet
    df.to_parquet(output_file, index=False, engine="pyarrow")
    logging.info(f"Camada Silver (Focus) gerada em: '{output_file}'")



