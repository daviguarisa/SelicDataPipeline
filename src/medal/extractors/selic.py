from brdata.bacen.selic import fetch_selic
import logging
from tqdm import tqdm

from medal.utils import gerar_trimestres

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def bronze_selic(
        ano_inicio: int = 2021,
        output_path: str = "data/bronze/selic"
) -> None:
    """
    Extrai informações de expectativas anuais do boletim focus a cada trimestre desde 2021.
    A extração é feita com a biblioteca brdata.
    """
    intervalos = list(gerar_trimestres(ano_inicio=ano_inicio))

    for inicio, fim in tqdm(intervalos, desc="Extraindo Selic", unit="trimestre"):
        try:
            fetch_selic(
                category="meta",
                start_date=inicio,
                end_date=fim,
                path=output_path
            )
        except Exception as e:
            logging.error(f"Falha ao extrair período {inicio} até {fim}: {e}")
