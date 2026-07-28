from datetime import date 
from typing import Generator

def gerar_semestres(
        ano_inicio: int = 2021
) -> Generator[tuple[date, date], None, None]:
    """
    Gera pares de objetos (data_inicio, data_fim) para cada semestre até a data de hoje
    Utiliza geradores para garantir eficiência de memória em pipelines.
    """
    hoje = date.today()

    for ano in range(ano_inicio, hoje.year + 1):
        limites_semestres = [
            (date(ano, 1, 1), date(ano, 6, 30)),
            (date(ano, 7, 1), date(ano, 12, 31)),
        ]

        for inicio, fim in limites_semestres:
            if inicio <= hoje:
                fim_efetivo = min(fim, hoje)
                yield inicio.isoformat(), fim_efetivo.isoformat()
