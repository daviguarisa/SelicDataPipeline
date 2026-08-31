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
    df["reuniao_num"] = (
        df["reuniao_num"].str.extract(r"(\d+)")[0].astype(int)
    )

    df["reuniao_data"] = pd.to_datetime(
        df["reuniao_data"], format="%d/%m/%Y"
    ).dt.strftime("%Y-%m-%d")

    vigencia_split = df["vigencia"].str.split("-", expand=True)

    df["vigencia_inicio"] = pd.to_datetime(
        vigencia_split[0].str.strip(), format="%d/%m/%Y", errors="coerce"
    ).dt.strftime("%Y-%m-%d")

    df["vigencia_fim"] = pd.to_datetime(
        vigencia_split[1].str.strip(), format="%d/%m/%Y", errors="coerce"
    ).dt.strftime("%Y-%m-%d")

    colunas_para_remover = ["vigencia", "vies", "tban"]
    df.drop(columns=colunas_para_remover, inplace=True, errors="ignore")

    colunas_ordenadas = [
        "reuniao_num",
        "reuniao_data",
        "vigencia_inicio",
        "vigencia_fim",
        "meta_selic",
        "taxa_selic_pct",
        "taxa_selic_aa",
    ]
    df = df[colunas_ordenadas]

    # Salva em Parquet
    df.to_parquet(output_file, index=False, engine="pyarrow")
    logging.info(f"Camada Silver (Copom) gerada em: '{output_file}'")
