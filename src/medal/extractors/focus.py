from brdata.bacen.boletim_focus import BoletimFocus
from medal.utils import gerar_semestres
from tqdm import tqdm

focus = BoletimFocus()

def bronze_focus(focus: BoletimFocus):
    """
    Extrai informações de expectativas anuais do boletim focus a cada semestre desde 2021.
    A extração é feita com a biblioteca brdata.
    """

    try:
        intervalos = list(gerar_semestres(2021))
        for inicio, fim in tqdm(intervalos, desc="Processando Focus", unit="semestre"):
            focus.expectativas_anuais(
                indicador="Selic",
                start_date=inicio,
                end_date=fim,
                top=10000,
                path="data/raw/focus"
            )
    except Exception as e:
        print("Erro: {e}")

bronze_focus(focus=focus)