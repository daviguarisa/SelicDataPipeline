from brdata.bacen.boletim_focus import BoletimFocus
from tqdm import tqdm
import logging

from medal.utils import gerar_trimestres

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def bronze_focus(
    focus: BoletimFocus,
    ano_inicio: int = 2021,
    indicador: str = "Selic",
    output_path: str = "data/bronze/focus"
) -> None:
    """
    Extrai informações de expectativas anuais do boletim focus a cada semestre desde 2021.
    A extração é feita com a biblioteca brdata.
    """
    intervalos = list(gerar_trimestres(ano_inicio))

    for inicio, fim in tqdm(intervalos, desc="Processando Focus", unit="trimestre"):
        try:
            focus.expectativas_anuais(
                indicador=indicador,
                start_date=inicio,
                end_date=fim,
                top=10000,
                path=output_path
            )
        except Exception as e:
            logging.error(f"Falha ao extrair período {inicio} até {fim}: {e}")
