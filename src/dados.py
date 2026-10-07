import json
from produto import Produto

ARQUIVO = "data/produtos.json"


def salvar_produtos(produtos):
    """Salva a lista de produtos no arquivo JSON."""
    dados = [p.__dict__ for p in produtos]
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)


def carregar_produtos():
    """Carrega a lista de produtos do arquivo JSON."""
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except FileNotFoundError:
        return []

    return [Produto(d["_sku"], d["nome"], d["categoria"], d["_preco"], d["_estoque"], d["ativo"]) for d in dados]