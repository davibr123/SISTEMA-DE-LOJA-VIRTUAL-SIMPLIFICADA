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

    return [Produto(d["sku"], d["nome"], d["categoria"], d["_preco"], d["_estoque"], d["ativo"]) for d in dados]

ARQUIVO_PEDIDOS = "data/pedidos.json"

def salvar_pedidos(pedidos):
    """Salva um resumo dos pedidos no arquivo JSON."""
    dados = []
    for p in pedidos:
        dados.append({
            "id": p.id,
            "cliente": p.cliente.nome,
            "data": str(p.data),
            "status": p.status,
            "total": p.total(),
        })
    with open(ARQUIVO_PEDIDOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

def carregar_pedidos():
    """Carrega o resumo dos pedidos do arquivo JSON."""
    try:
        with open(ARQUIVO_PEDIDOS, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []