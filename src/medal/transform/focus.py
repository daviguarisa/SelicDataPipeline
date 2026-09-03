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
    df = df.rename(
        columns={
            "Indicador": "indicador",
            "Data": "data",
            "Reuniao": "reuniao",
            "Media": "media",
            "Mediana": "mediana",
            "DesvioPadrao": "desvio_padrao",
            "Minimo": "minimo",
            "Maximo": "maximo",
            "numeroRespondentes": "numero_respondentes",
            "baseCalculo": "base_calculo",
        }
    )

    reuniao_split = df["reuniao"].str.extract(r"R(\d+)/(\d+)")
    df["reuniao_num"] = pd.to_numeric(reuniao_split[0], errors="coerce").astype("Int64")
    df["reuniao_ano"] = pd.to_numeric(reuniao_split[1], errors="coerce").astype("Int64")
    df.drop(columns=["reuniao"], inplace=True)

    df["data"] = pd.to_datetime(df["data"], format="%Y-%m-%d", errors="coerce").dt.date

    df["numero_respondentes"] = df["numero_respondentes"].astype("Int64")
    df["base_calculo"] = df["base_calculo"].astype("Int64")

    colunas_float = ["media", "mediana", "desvio_padrao", "minimo", "maximo"]
    df[colunas_float] = df[colunas_float].apply(pd.to_numeric, errors="coerce").round(2)

    colunas_finais = [
        "indicador",
        "data",
        "reuniao_ano",
        "reuniao_num",
        "media",
        "mediana",
        "desvio_padrao",
        "minimo",
        "maximo",
        "numero_respondentes",
        "base_calculo",
    ]
    df = df[colunas_finais]

    # Salva em Parquet
    df.to_parquet(output_file, index=False, engine="pyarrow")
    logging.info(f"Camada Silver (Focus) gerada em: '{output_file}'")



