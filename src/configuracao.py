import json
import os

CAMINHO = os.path.join(os.path.dirname(__file__), "..", "settings.json")

# valores usados se o settings.json não existir (são os mesmos do arquivo)
PADRAO = {
    "frete": {
        "padrao": {"valor": 40.0, "prazo_dias": 10},
        "por_uf": {
            "CE": {"valor": 15.0, "prazo_dias": 3},
            "PE": {"valor": 20.0, "prazo_dias": 5},
            "SP": {"valor": 30.0, "prazo_dias": 7},
        },
        "por_cidade": {
            "Juazeiro do Norte/CE": {"valor": 10.0, "prazo_dias": 2},
        },
    },
    "top_n_produtos": 3,
    "validade_padrao_cupom_dias": 30,
    "janela_cancelamento_horas": 24,
}


def carregar_settings():
    """Lê o settings.json. Se o arquivo não existir, usa os valores padrão."""
    if not os.path.exists(CAMINHO):
        return PADRAO
    with open(CAMINHO, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)