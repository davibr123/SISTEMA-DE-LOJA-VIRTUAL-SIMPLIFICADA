from dados import carregar_pedidos
from configuracao import carregar_settings

# só estes status contam como venda (pedido CRIADO ainda não foi pago e CANCELADO foi desfeito)
STATUS_VENDA = ["PAGO", "ENVIADO", "ENTREGUE"]


# ---------- cálculos (recebem a lista de pedidos e devolvem os resultados) ----------

def faturamento_por_periodo(pedidos, inicio, fim):
    """Devolve a quantidade de vendas, o faturamento e o ticket médio entre duas datas (AAAA-MM-DD)."""
    quantidade = 0
    faturamento = 0
    for p in pedidos:
        if p["status"] in STATUS_VENDA and inicio <= p["data"] <= fim:
            quantidade += 1
            faturamento += p["total"]
    ticket_medio = 0
    if quantidade > 0:
        ticket_medio = faturamento / quantidade
    return quantidade, faturamento, ticket_medio


def quantidade_do_par(par):
    """Auxiliar da ordenação: devolve a quantidade de um par (nome, quantidade)."""
    return par[1]


def top_produtos(pedidos, n):
    """Devolve os n produtos mais vendidos, como lista de pares (nome, quantidade)."""
    quantidades = {}
    for p in pedidos:
        if p["status"] in STATUS_VENDA:
            for item in p.get("itens", []):
                nome = item["nome"]
                quantidades[nome] = quantidades.get(nome, 0) + item["quantidade"]
    lista = list(quantidades.items())
    lista.sort(key=quantidade_do_par, reverse=True)
    return lista[:n]


def vendas_por_categoria(pedidos):
    """Soma o valor vendido (preço x quantidade) de cada categoria."""
    totais = {}
    for p in pedidos:
        if p["status"] in STATUS_VENDA:
            for item in p.get("itens", []):
                categoria = item["categoria"]
                valor = item["preco"] * item["quantidade"]
                totais[categoria] = totais.get(categoria, 0) + valor
    return totais


def vendas_por_uf(pedidos):
    """Soma o total dos pedidos de cada UF."""
    totais = {}
    for p in pedidos:
        if p["status"] in STATUS_VENDA:
            uf = p.get("uf", "")
            totais[uf] = totais.get(uf, 0) + p["total"]
    return totais


def pedidos_por_status(pedidos):
    """Devolve, para cada status, um par (quantidade, percentual do total de pedidos)."""
    contagem = {}
    for p in pedidos:
        contagem[p["status"]] = contagem.get(p["status"], 0) + 1
    resultado = {}
    for status in contagem:
        resultado[status] = (contagem[status], contagem[status] / len(pedidos) * 100)
    return resultado


# ---------- relatórios (leem os pedidos salvos e imprimem na tela) ----------

def pedidos_por_periodo(inicio, fim):
    """Lista os pedidos entre duas datas e mostra faturamento e ticket médio."""
    pedidos = carregar_pedidos()
    print(f"Pedidos de {inicio} a {fim}:")
    quantidade = 0
    for p in pedidos:
        if inicio <= p["data"] <= fim:
            print(f"- Pedido {p['id']} | {p['cliente']} | {p['status']} | R${p['total']:.2f}")
            quantidade += 1
    print(f"Total de pedidos: {quantidade}")

    vendas, faturamento, ticket_medio = faturamento_por_periodo(pedidos, inicio, fim)
    print(f"Vendas (pedidos pagos, enviados ou entregues): {vendas}")
    print(f"Faturamento: R${faturamento:.2f}")
    print(f"Ticket médio: R${ticket_medio:.2f}")


def mostrar_top_produtos():
    """Mostra os produtos mais vendidos (a quantidade de produtos vem do settings.json)."""
    n = carregar_settings()["top_n_produtos"]
    top = top_produtos(carregar_pedidos(), n)
    print(f"Top {n} produtos mais vendidos:")
    if len(top) == 0:
        print("  Nenhuma venda ainda.")
    for i in range(len(top)):
        print(f"  {i + 1}. {top[i][0]} - {top[i][1]} unidades")


def mostrar_vendas_por_categoria_e_uf():
    """Mostra quanto foi vendido em cada categoria e em cada UF."""
    pedidos = carregar_pedidos()
    print("Vendas por categoria:")
    categorias = vendas_por_categoria(pedidos)
    if len(categorias) == 0:
        print("  Nenhuma venda ainda.")
    for categoria in categorias:
        print(f"  {categoria}: R${categorias[categoria]:.2f}")
    print("Vendas por UF:")
    ufs = vendas_por_uf(pedidos)
    if len(ufs) == 0:
        print("  Nenhuma venda ainda.")
    for uf in ufs:
        print(f"  {uf}: R${ufs[uf]:.2f}")


def mostrar_pedidos_por_status():
    """Mostra quantos pedidos existem em cada status, com a porcentagem."""
    resultado = pedidos_por_status(carregar_pedidos())
    print("Pedidos por status:")
    if len(resultado) == 0:
        print("  Nenhum pedido ainda.")
    for status in resultado:
        quantidade, percentual = resultado[status]
        print(f"  {status}: {quantidade} ({percentual:.1f}%)")