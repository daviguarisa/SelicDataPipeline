from datetime import date 
from typing import Generator

def gerar_trimestres(
    ano_inicio: int
) -> Generator[tuple[str, str], None, None]:
    """
    Gera pares de objetos (data_inicio, data_fim) para cada trimestre até a data de hoje.
    Utiliza geradores para garantir eficiência de memória em pipelines.
    """
    hoje = date.today()

    for ano in range(ano_inicio, hoje.year + 1):
        limites_trimestres = [
            (date(ano, 1, 1), date(ano, 3, 31)),   # Q1
            (date(ano, 4, 1), date(ano, 6, 30)),   # Q2
            (date(ano, 7, 1), date(ano, 9, 30)),   # Q3
            (date(ano, 10, 1), date(ano, 12, 31)), # Q4
        ]

        for inicio, fim in limites_trimestres:
            if inicio <= hoje:
                fim_efetivo = min(fim, hoje)
                yield inicio.isoformat(), fim_efetivo.isoformat()
