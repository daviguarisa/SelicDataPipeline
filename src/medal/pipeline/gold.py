import logging

from medal.load import connect, create_table

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - [%(levelname)s] - %(message)s"
)

def run_gold():
    """
    Função Orquestradora da Camada Gold.
    Cria conexão com o banco de dados e executa queries para criar tabelas.
    """
    logging.info("Iniciando pipeline da Camada Gold")

    try:
        with connect() as conn:
            logging.info("--> Criando tabelas Gold")
            create_table(conn, "queries/focus_gold.sql", "focus")
            create_table(conn, "queries/selic_gold.sql", "selic")
            create_table(conn, "queries/copom_gold.sql", "copom")
    except Exception as e:
        logging.error(f"Falha na execução de tabelas gold: {e}")

run_gold()