import logging

from brdata.bacen.boletim_focus import BoletimFocus
from medal.extractors import bronze_focus

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - [%(levelname)s] - %(message)s"
)

def run_bronze(ano_inicio: int = 2021):
    """
    Função Orquestradora da Camada Bronze.
    Instancia as conexões e executa a extração das fontes (Focus e Selic).
    """
    logging.info("Iniciando pipeline da Camada Bronze")

    try:
        focus_client = BoletimFocus()

        logging.info("--> Executando extração do Boletim Focus...")
        bronze_focus(
            focus=focus_client,
            ano_inicio=ano_inicio
        )

        logging.info("Camada Bronze concluída com sucesso!")

    except Exception as e:
        logging.critical(f"Falha no orquestrador da Camada Bronze: {e}")
        raise e

run_bronze()
