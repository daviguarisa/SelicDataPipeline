from brdata.bacen.selic import fetch_selic
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def bronze_selic(
        ano_inicio: int = 2021,
        output_path: str = "data/bronze/selic"
) -> None:
    """
    Extrai informações da selic meta desde o ano informado até a data atual.
    A extração é feita com a biblioteca brdata.
    """
    data_inicio = f"{ano_inicio}-01-01"
    try:
        fetch_selic(
            category="meta",
            start_date=data_inicio,
            path=output_path
        )
        logging.info("Extração Selic Meta bem sucedida!")
    except Exception as e:
        logging.error(f"Falha ao extrair Selic Meta: {e}")
