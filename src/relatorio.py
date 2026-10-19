from dados import carregar_pedidos


def pedidos_por_periodo(inicio, fim):
    """Lista os pedidos entre duas datas (formato 'AAAA-MM-DD') e soma o faturamento."""
    pedidos = carregar_pedidos()
    filtrados = [p for p in pedidos if inicio <= p["data"] <= fim]

    print(f"Pedidos de {inicio} a {fim}:")
    for p in filtrados:
        print(f"- Pedido {p['id']} | {p['cliente']} | {p['status']} | R${p['total']:.2f}")

    faturamento = sum(p["total"] for p in filtrados if p["status"] != "CANCELADO")
    print(f"Total de pedidos: {len(filtrados)}")
    print(f"Faturamento: R${faturamento:.2f}")