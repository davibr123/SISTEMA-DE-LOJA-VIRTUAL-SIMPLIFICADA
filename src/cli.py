import os
from produto_fisico import ProdutoFisico
from produto_digital import ProdutoDigital
from produto_hibrido import ProdutoHibrido
from cliente import Cliente
from endereco import Endereco
from carrinho import Carrinho
from frete import Frete
from pagamento import Pagamento
from relatorio import pedidos_por_periodo
import dados


def mostrar_menu():
    print("\n===== LOJA VIRTUAL =====")
    print("1  - Cadastrar produto")
    print("2  - Cadastrar cliente")
    print("3  - Listar produtos")
    print("4  - Adicionar item ao carrinho")
    print("5  - Fechar pedido")
    print("6  - Pagar pedido")
    print("7  - Enviar pedido")
    print("8  - Entregar pedido")
    print("9  - Cancelar pedido")
    print("10 - Ver nota do pedido")
    print("11 - Relatório de pedidos por período")
    print("0  - Sair")


def escolher(lista, titulo):
    """Mostra uma lista numerada e devolve o item que a pessoa escolher."""
    if len(lista) == 0:
        print("Nada disponível.")
        return None
    print(titulo)
    for i in range(len(lista)):
        print(f"  {i + 1} - {lista[i]}")
    escolha = int(input("Número: "))
    if escolha < 1 or escolha > len(lista):
        print("Opção inválida.")
        return None
    return lista[escolha - 1]


def escolher_pedido(pedidos, status_permitidos):
    """Mostra só os pedidos que estão em um dos status permitidos."""
    disponiveis = []
    for pedido in pedidos:
        if pedido.status in status_permitidos:
            disponiveis.append(pedido)
    return escolher(disponiveis, "Pedidos:")


def proximo_id(pedidos):
    """Descobre o número do próximo pedido (continua depois dos pedidos já salvos)."""
    maior = 0
    for resumo in dados.carregar_pedidos():
        if resumo["id"] > maior:
            maior = resumo["id"]
    for pedido in pedidos:
        if pedido.id > maior:
            maior = pedido.id
    return maior + 1


def cadastrar_produto(produtos):
    tipo = input("Tipo (1 - Físico, 2 - Digital, 3 - Híbrido): ")
    sku = input("SKU: ")
    nome = input("Nome: ")
    categoria = input("Categoria: ")
    preco = float(input("Preço: "))
    estoque = int(input("Estoque: "))
    if tipo == "1":
        peso = float(input("Peso (kg): "))
        produto = ProdutoFisico(sku, nome, categoria, preco, estoque, peso)
    elif tipo == "3":
        peso = float(input("Peso (kg): "))
        link = input("Link de download: ")
        produto = ProdutoHibrido(sku, nome, categoria, preco, estoque, peso, link)
    else:
        produto = ProdutoDigital(sku, nome, categoria, preco, estoque)

    if produto in produtos:  # usa o __eq__ do Produto (compara pelo SKU)
        print("Já existe um produto com esse SKU.")
        return
    produtos.append(produto)
    print("Produto cadastrado!")


def cadastrar_cliente(clientes):
    nome = input("Nome: ")
    email = input("Email: ")
    cpf = input("CPF: ")
    cliente = Cliente(str(len(clientes) + 1), nome, email, cpf)

    if cliente in clientes:  # usa o __eq__ do Cliente (compara por CPF ou email)
        print("Já existe um cliente com esse CPF ou email.")
        return
    cep = input("CEP: ")
    cidade = input("Cidade: ")
    uf = input("UF: ")
    cliente.enderecos.append(Endereco(cep, cidade, uf))
    clientes.append(cliente)
    print("Cliente cadastrado!")


def listar_produtos(produtos):
    if len(produtos) == 0:
        print("Nenhum produto cadastrado.")
    for p in produtos:
        print(f"{p} | estoque: {p.estoque}")


def adicionar_item(produtos, clientes, carrinhos):
    cliente = escolher(clientes, "Clientes:")
    if cliente is None:
        return
    produto = escolher(produtos, "Produtos:")
    if produto is None:
        return
    quantidade = int(input("Quantidade: "))

    if cliente.id not in carrinhos:
        carrinhos[cliente.id] = Carrinho(cliente)
    carrinho = carrinhos[cliente.id]
    carrinho.adicionar_item(produto, quantidade)

    print(carrinho)
    for item in carrinho.itens:
        print(f"  - {item}")


def fechar_pedido(clientes, carrinhos, cupons, pedidos):
    cliente = escolher(clientes, "Clientes:")
    if cliente is None:
        return
    if cliente.id not in carrinhos:
        print("Esse cliente ainda não tem itens no carrinho.")
        return
    if len(cliente.enderecos) == 0:
        print("Cliente sem endereço cadastrado.")
        return

    codigo = input("Código do cupom (Enter para nenhum): ").strip().upper()
    cupom = None
    for c in cupons:
        if c.codigo == codigo:
            cupom = c
    if codigo != "" and cupom is None:
        print("Cupom não encontrado.")
        return

    frete = Frete(cliente.enderecos[0].uf)
    pedido = carrinhos[cliente.id].fechar_pedido(proximo_id(pedidos), frete, cupom)
    pedidos.append(pedido)
    del carrinhos[cliente.id]  # o carrinho virou pedido, então esvazia
    print(pedido.gerar_resumo())


def pagar_pedido(pedidos):
    pedido = escolher_pedido(pedidos, ["CRIADO"])
    if pedido is None:
        return
    print(f"Total: R${pedido.total():.2f} | já pago: R${pedido.total_pago():.2f}")
    forma = input("Forma (PIX, CREDITO, DEBITO, BOLETO): ").upper()
    valor = float(input("Valor: "))
    pedido.pagar(Pagamento(forma, valor))
    print(pedido)


def enviar_pedido(pedidos):
    pedido = escolher_pedido(pedidos, ["PAGO"])
    if pedido is None:
        return
    pedido.enviar()
    print(f"Pedido enviado! Código de rastreio: {pedido.codigo_rastreio}")


def entregar_pedido(pedidos):
    pedido = escolher_pedido(pedidos, ["ENVIADO"])
    if pedido is None:
        return
    pedido.entregar()
    print(f"Pedido entregue em {pedido.data_entrega}")


def cancelar_pedido(pedidos):
    pedido = escolher_pedido(pedidos, ["CRIADO", "PAGO"])
    if pedido is None:
        return
    pedido.cancelar()
    print(f"Pedido {pedido.id} cancelado.")


def ver_nota(pedidos):
    pedido = escolher_pedido(pedidos, ["CRIADO", "PAGO", "ENVIADO", "ENTREGUE", "CANCELADO"])
    if pedido is not None:
        print(pedido.gerar_resumo())


def relatorio():
    inicio = input("Data inicial AAAA-MM-DD (Enter = todas): ")
    if inicio == "":
        inicio = "2000-01-01"
    fim = input("Data final AAAA-MM-DD (Enter = todas): ")
    if fim == "":
        fim = "2999-12-31"
    pedidos_por_periodo(inicio, fim)


def main():
    # na primeira vez usa os dados de exemplo; depois carrega o que foi salvo
    if not os.path.exists(dados.ARQUIVO_CLIENTES):
        produtos, clientes, cupons = dados.criar_seed()
    else:
        produtos = dados.carregar_produtos()
        clientes = dados.carregar_clientes()
        cupons = dados.carregar_cupons()
    pedidos = []
    carrinhos = {}  # guarda um carrinho por cliente (a chave é o id do cliente)

    while True:
        mostrar_menu()
        opcao = input("Escolha: ").strip()
        if opcao == "0":
            break

        try:
            if opcao == "1":
                cadastrar_produto(produtos)
            elif opcao == "2":
                cadastrar_cliente(clientes)
            elif opcao == "3":
                listar_produtos(produtos)
            elif opcao == "4":
                adicionar_item(produtos, clientes, carrinhos)
            elif opcao == "5":
                fechar_pedido(clientes, carrinhos, cupons, pedidos)
            elif opcao == "6":
                pagar_pedido(pedidos)
            elif opcao == "7":
                enviar_pedido(pedidos)
            elif opcao == "8":
                entregar_pedido(pedidos)
            elif opcao == "9":
                cancelar_pedido(pedidos)
            elif opcao == "10":
                ver_nota(pedidos)
            elif opcao == "11":
                relatorio()
            else:
                print("Opção inválida.")
        except ValueError as erro:
            # as validações das classes (preço, estoque, CPF, cupom...) caem aqui
            print(f"Erro: {erro}")

        # salva tudo depois de cada ação
        dados.salvar_produtos(produtos)
        dados.salvar_clientes(clientes)
        dados.salvar_cupons(cupons)
        dados.salvar_pedidos(pedidos)

    print("Até logo!")


main()