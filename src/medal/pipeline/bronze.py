from brdata.bacen.boletim_focus import BoletimFocus
import logging

from medal.extractors import bronze_focus, bronze_selic, bronze_copom

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - [%(levelname)s] - %(message)s"
)

def run_bronze(ano_inicio: int = 2021):
    """
    Função Orquestradora da Camada Bronze.
    Instancia as conexões e executa a extração das fontes (Focus, Selic e Copom).
    """
    logging.info("Iniciando pipeline da Camada Bronze")

    try:
        focus_client = BoletimFocus()

        logging.info("--> Executando extração do Boletim Focus...")
        bronze_focus(
            focus=focus_client,
            ano_inicio=ano_inicio
        )

        logging.info("--> Executando extração da Selic Meta... ")
        bronze_selic(
            ano_inicio=ano_inicio
        )

        logging.info("--> Executando extração da Tabela Copom... ")
        bronze_copom()
        
        logging.info("Camada Bronze concluída com sucesso!")

    except Exception as e:
        logging.critical(f"Falha no orquestrador da Camada Bronze: {e}")
        raise e
