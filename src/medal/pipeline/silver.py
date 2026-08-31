from medal.transform import transform_focus_silver, transform_selic_silver, transform_copom_silver
import logging

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - [%(levelname)s] - %(message)s"
)

def run_silver():
    """
    Função Orquestradora da Camada Silver.
    Executa a leitura e transformações das fontes (Focus e Selic).
    """
    logging.info("Iniciando pipeline da Camada Silver")

    try:
        logging.info("--> Executando Transformação do Boletim Focus")
        transform_focus_silver()

        logging.info("--> Executando Transformação da Selic Meta")
        transform_selic_silver()

        logging.info("--> Executando Transformação da Tabela Copom")
        transform_copom_silver()

        logging.info("Camada Silver concluída com sucesso!")

    except Exception as e:
        logging.critical(f"Falha no orquestrador da Camada Silver: {e}")
        raise e

