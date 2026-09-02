from brdata.bacen.copom import fetch_copom_table
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def bronze_copom(
        output_path: str = "data/bronze/copom"
) -> None:
    """
    Extrai a tabela de reuniões do copom.
    A extração é feita com a biblioteca brdata.
    """
    try:
        fetch_copom_table(path=output_path)
        logging.info("Extração Tabela Copom bem sucedida!")
    except Exception as e:
        logging.error(f"Falha ao extrair Tabela Copom: {e}")