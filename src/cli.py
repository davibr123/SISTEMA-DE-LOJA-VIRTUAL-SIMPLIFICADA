from datetime import date, timedelta
from produto_fisico import ProdutoFisico
from produto_digital import ProdutoDigital
from produto_hibrido import ProdutoHibrido
from cliente import Cliente
from endereco import Endereco
from cupom import Cupom
from carrinho import Carrinho
from frete import Frete
from pagamento import Pagamento
from configuracao import carregar_settings
from loja import Loja
import relatorio


# ---------- funções auxiliares ----------

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


def perguntar(texto, atual):
    """Pergunta um valor novo. Se a pessoa só apertar Enter, mantém o valor atual."""
    resposta = input(f"{texto} ({atual}): ")
    if resposta == "":
        return atual
    return resposta


def escolher_pedido(loja, status_permitidos):
    """Mostra só os pedidos que estão em um dos status permitidos."""
    disponiveis = []
    for pedido in loja.pedidos:
        if pedido.status in status_permitidos:
            disponiveis.append(pedido)
    return escolher(disponiveis, "Pedidos:")


def escolher_carrinho(loja):
    """Escolhe um cliente e devolve o carrinho dele (se ele tiver um)."""
    cliente = escolher(loja.clientes, "Clientes:")
    if cliente is None:
        return None
    if cliente.id not in loja.carrinhos:
        print("Esse cliente ainda não tem itens no carrinho.")
        return None
    return loja.carrinhos[cliente.id]


def mostrar_carrinho(carrinho):
    print(carrinho)
    for item in carrinho.itens:
        print(f"  - {item}")


# ---------- produtos ----------

def cadastrar_produto(loja):
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

    if produto in loja.produtos:  # usa o __eq__ do Produto (compara pelo SKU)
        print("Já existe um produto com esse SKU.")
        return
    loja.produtos.append(produto)
    print("Produto cadastrado!")


def editar_produto(loja):
    produto = escolher(loja.produtos, "Produtos:")
    if produto is None:
        return
    print("Aperte Enter para manter o valor atual.")
    nome = perguntar("Nome", produto.nome)
    categoria = perguntar("Categoria", produto.categoria)
    preco = float(perguntar("Preço", produto.preco))
    if produto.ativo:
        ativo = perguntar("Ativo (s/n)", "s")
    else:
        ativo = perguntar("Ativo (s/n)", "n")

    produto.preco = preco  # se o preço for inválido dá erro aqui, antes de mudar o resto
    produto.nome = nome
    produto.categoria = categoria
    produto.ativo = (ativo.lower() == "s")
    print("Produto atualizado!")


def remover_produto(loja):
    produto = escolher(loja.produtos, "Produtos:")
    if produto is None:
        return
    for carrinho in loja.carrinhos.values():
        for item in carrinho.itens:
            if item.produto == produto:
                print("Esse produto está em um carrinho aberto. Remova do carrinho primeiro.")
                return
    loja.produtos.remove(produto)
    print("Produto removido!")


def entrada_estoque(loja):
    produto = escolher(loja.produtos, "Produtos:")
    if produto is None:
        return
    quantidade = int(input("Quantidade que chegou do fornecedor: "))
    produto.entrada_estoque(quantidade)
    print(f"Novo estoque de {produto.nome}: {produto.estoque}")


def listar_produtos(loja):
    if len(loja.produtos) == 0:
        print("Nenhum produto cadastrado.")
    for p in loja.produtos:
        situacao = "ativo"
        if not p.ativo:
            situacao = "inativo"
        print(f"{p} | estoque: {p.estoque} | {situacao}")


# ---------- clientes ----------

def cadastrar_cliente(loja):
    nome = input("Nome: ")
    email = input("Email: ")
    cpf = input("CPF: ")
    cliente = Cliente(loja.proximo_id_cliente(), nome, email, cpf)

    if cliente in loja.clientes:  # usa o __eq__ do Cliente (compara por CPF ou email)
        print("Já existe um cliente com esse CPF ou email.")
        return
    cep = input("CEP: ")
    cidade = input("Cidade: ")
    uf = input("UF: ")
    cliente.enderecos.append(Endereco(cep, cidade, uf))
    loja.clientes.append(cliente)
    print("Cliente cadastrado!")


def editar_cliente(loja):
    cliente = escolher(loja.clientes, "Clientes:")
    if cliente is None:
        return
    print("Aperte Enter para manter o valor atual.")
    nome = perguntar("Nome", cliente.nome)
    email = perguntar("Email", cliente.email)
    cpf = perguntar("CPF", cliente.cpf)

    novo = Cliente(cliente.id, nome, email, cpf)  # criar o cliente novo já valida email e CPF
    for outro in loja.clientes:
        if outro is not cliente and outro == novo:
            print("Já existe outro cliente com esse CPF ou email.")
            return
    cliente.nome = nome
    cliente.email = email
    cliente.cpf = cpf
    print("Cliente atualizado!")


def adicionar_endereco(loja):
    cliente = escolher(loja.clientes, "Clientes:")
    if cliente is None:
        return
    cep = input("CEP: ")
    cidade = input("Cidade: ")
    uf = input("UF: ")
    cliente.enderecos.append(Endereco(cep, cidade, uf))
    print("Endereço adicionado!")


def remover_cliente(loja):
    cliente = escolher(loja.clientes, "Clientes:")
    if cliente is None:
        return
    if cliente.id in loja.carrinhos:
        print("Esse cliente tem um carrinho aberto.")
        return
    for pedido in loja.pedidos:
        if pedido.cliente is cliente and pedido.status in ["CRIADO", "PAGO", "ENVIADO"]:
            print("Esse cliente tem pedidos em andamento.")
            return
    loja.clientes.remove(cliente)
    print("Cliente removido!")


def listar_clientes(loja):
    if len(loja.clientes) == 0:
        print("Nenhum cliente cadastrado.")
    for c in loja.clientes:
        print(f"{c} | CPF: {c.cpf}")
        for e in c.enderecos:
            print(f"    endereço: {e}")


# ---------- cupons ----------

def cadastrar_cupom(loja):
    codigo = input("Código: ").strip().upper()
    for existente in loja.cupons:
        if existente.codigo == codigo:
            print("Já existe um cupom com esse código.")
            return
    tipo = input("Tipo (VALOR ou PERCENTUAL): ").strip().upper()
    valor = float(input("Valor (em reais ou em porcentagem): "))
    validade = input("Validade AAAA-MM-DD (Enter = validade padrão): ").strip()
    if validade == "":
        dias = carregar_settings()["validade_padrao_cupom_dias"]
        data_validade = date.today() + timedelta(days=dias)
    else:
        data_validade = date.fromisoformat(validade)
    uso_maximo = int(input("Uso máximo: "))
    texto = input("Categorias elegíveis separadas por vírgula (Enter = todas): ")
    categorias = []
    if texto.strip() != "":
        for categoria in texto.split(","):
            categorias.append(categoria.strip())

    loja.cupons.append(Cupom(codigo, tipo, valor, data_validade, uso_maximo, categorias))
    print(f"Cupom válido até {data_validade}.")


def listar_cupons(loja):
    if len(loja.cupons) == 0:
        print("Nenhum cupom cadastrado.")
    for c in loja.cupons:
        if len(c.categorias_elegiveis) == 0:
            categorias = "todas"
        else:
            categorias = ", ".join(c.categorias_elegiveis)
        print(f"{c} | valor: {c.valor} | validade: {c.data_validade} | usos: {c.usos}/{c.uso_maximo} | categorias: {categorias}")


# ---------- carrinho e pedidos ----------

def adicionar_item(loja):
    cliente = escolher(loja.clientes, "Clientes:")
    if cliente is None:
        return
    produto = escolher(loja.produtos, "Produtos:")
    if produto is None:
        return
    quantidade = int(input("Quantidade: "))

    if cliente.id not in loja.carrinhos:
        loja.carrinhos[cliente.id] = Carrinho(cliente)
    carrinho = loja.carrinhos[cliente.id]
    carrinho.adicionar_item(produto, quantidade)
    mostrar_carrinho(carrinho)


def remover_item(loja):
    carrinho = escolher_carrinho(loja)
    if carrinho is None:
        return
    item = escolher(carrinho.itens, "Itens do carrinho:")
    if item is None:
        return
    carrinho.remover_item(item.produto)
    mostrar_carrinho(carrinho)


def alterar_quantidade(loja):
    carrinho = escolher_carrinho(loja)
    if carrinho is None:
        return
    item = escolher(carrinho.itens, "Itens do carrinho:")
    if item is None:
        return
    quantidade = int(input("Nova quantidade: "))
    carrinho.alterar_quantidade(item.produto, quantidade)
    mostrar_carrinho(carrinho)


def ver_carrinho(loja):
    carrinho = escolher_carrinho(loja)
    if carrinho is not None:
        mostrar_carrinho(carrinho)


def fechar_pedido(loja):
    cliente = escolher(loja.clientes, "Clientes:")
    if cliente is None:
        return
    if cliente.id not in loja.carrinhos:
        print("Esse cliente ainda não tem itens no carrinho.")
        return
    if len(cliente.enderecos) == 0:
        print("Cliente sem endereço cadastrado.")
        return

    if len(cliente.enderecos) == 1:
        endereco = cliente.enderecos[0]
    else:
        endereco = escolher(cliente.enderecos, "Endereços de entrega:")
        if endereco is None:
            return

    if len(loja.cupons) > 0:
        codigos = []
        for c in loja.cupons:
            codigos.append(c.codigo)
        print("Cupons cadastrados: " + ", ".join(codigos))
    codigo = input("Código do cupom (Enter para nenhum): ").strip().upper()
    cupom = None
    for c in loja.cupons:
        if c.codigo == codigo:
            cupom = c
    if codigo != "" and cupom is None:
        print("Cupom não encontrado.")
        return

    frete = Frete(endereco.uf, endereco.cidade)
    carrinho = loja.carrinhos[cliente.id]
    pedido = carrinho.fechar_pedido(loja.proximo_id_pedido(), frete, cupom, endereco)
    loja.pedidos.append(pedido)
    del loja.carrinhos[cliente.id]  # o carrinho virou pedido, então esvazia
    print(pedido.gerar_resumo())


def pagar_pedido(loja):
    pedido = escolher_pedido(loja, ["CRIADO"])
    if pedido is None:
        return
    print(f"Total: R${pedido.total():.2f} | já pago: R${pedido.total_pago():.2f}")
    forma = input("Forma (PIX, CREDITO, DEBITO, BOLETO): ").upper()
    valor = float(input("Valor: "))
    pedido.pagar(Pagamento(forma, valor))
    print(pedido)


def enviar_pedido(loja):
    pedido = escolher_pedido(loja, ["PAGO"])
    if pedido is None:
        return
    pedido.enviar()
    print(f"Pedido enviado! Código de rastreio: {pedido.codigo_rastreio}")


def entregar_pedido(loja):
    pedido = escolher_pedido(loja, ["ENVIADO"])
    if pedido is None:
        return
    pedido.entregar()
    print(f"Pedido entregue em {pedido.data_entrega}")


def cancelar_pedido(loja):
    pedido = escolher_pedido(loja, ["CRIADO", "PAGO"])
    if pedido is None:
        return
    pedido.cancelar()
    print(f"Pedido {pedido.id} cancelado.")


def ver_nota(loja):
    pedido = escolher_pedido(loja, ["CRIADO", "PAGO", "ENVIADO", "ENTREGUE", "CANCELADO"])
    if pedido is not None:
        print(pedido.gerar_resumo())


# ---------- relatórios ----------

def relatorio_periodo(loja):
    inicio = input("Data inicial AAAA-MM-DD (Enter = todas): ")
    if inicio == "":
        inicio = "2000-01-01"
    fim = input("Data final AAAA-MM-DD (Enter = todas): ")
    if fim == "":
        fim = "2999-12-31"
    relatorio.pedidos_por_periodo(inicio, fim)


def relatorio_top(loja):
    relatorio.mostrar_top_produtos()


def relatorio_categoria_uf(loja):
    relatorio.mostrar_vendas_por_categoria_e_uf()


def relatorio_status(loja):
    relatorio.mostrar_pedidos_por_status()


# ---------- menus ----------

def rodar_menu(titulo, opcoes, loja, texto_zero="Voltar"):
    """Mostra um menu e executa a opção escolhida, até a pessoa escolher a opção 0."""
    while True:
        print(f"\n===== {titulo} =====")
        for i in range(len(opcoes)):
            print(f"{i + 1} - {opcoes[i][0]}")
        print(f"0 - {texto_zero}")

        escolha = input("Escolha: ").strip()
        if escolha == "0":
            return
        if not escolha.isdigit() or int(escolha) < 1 or int(escolha) > len(opcoes):
            print("Opção inválida.")
            continue

        funcao = opcoes[int(escolha) - 1][1]
        try:
            funcao(loja)
        except ValueError as erro:
            # as validações das classes (preço, estoque, CPF, cupom...) caem aqui
            print(f"Erro: {erro}")

        loja.salvar()  # salva tudo depois de cada ação


def menu_produtos(loja):
    rodar_menu("PRODUTOS", [
        ("Cadastrar produto", cadastrar_produto),
        ("Editar produto", editar_produto),
        ("Remover produto", remover_produto),
        ("Entrada de estoque", entrada_estoque),
        ("Listar produtos", listar_produtos),
    ], loja)


def menu_clientes(loja):
    rodar_menu("CLIENTES", [
        ("Cadastrar cliente", cadastrar_cliente),
        ("Editar cliente", editar_cliente),
        ("Adicionar endereço a um cliente", adicionar_endereco),
        ("Remover cliente", remover_cliente),
        ("Listar clientes", listar_clientes),
    ], loja)


def menu_cupons(loja):
    rodar_menu("CUPONS", [
        ("Cadastrar cupom", cadastrar_cupom),
        ("Listar cupons", listar_cupons),
    ], loja)


def menu_pedidos(loja):
    rodar_menu("CARRINHO E PEDIDOS", [
        ("Adicionar item ao carrinho", adicionar_item),
        ("Remover item do carrinho", remover_item),
        ("Alterar quantidade de um item", alterar_quantidade),
        ("Ver carrinho", ver_carrinho),
        ("Fechar pedido", fechar_pedido),
        ("Pagar pedido", pagar_pedido),
        ("Enviar pedido", enviar_pedido),
        ("Entregar pedido", entregar_pedido),
        ("Cancelar pedido", cancelar_pedido),
        ("Ver nota do pedido", ver_nota),
    ], loja)


def menu_relatorios(loja):
    rodar_menu("RELATÓRIOS", [
        ("Pedidos, faturamento e ticket médio por período", relatorio_periodo),
        ("Produtos mais vendidos", relatorio_top),
        ("Vendas por categoria e por UF", relatorio_categoria_uf),
        ("Pedidos por status", relatorio_status),
    ], loja)


def main():
    loja = Loja()
    rodar_menu("LOJA VIRTUAL", [
        ("Produtos", menu_produtos),
        ("Clientes", menu_clientes),
        ("Cupons", menu_cupons),
        ("Carrinho e pedidos", menu_pedidos),
        ("Relatórios", menu_relatorios),
    ], loja, "Sair")
    print("Até logo!")


if __name__ == "__main__":  # só roda o menu quando este arquivo é executado diretamente
    main()