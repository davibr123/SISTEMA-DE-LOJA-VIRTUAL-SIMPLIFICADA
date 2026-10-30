import os
import dados


class Loja:
    """Guarda os dados da loja enquanto o programa roda: produtos, clientes, cupons, pedidos e carrinhos."""

    def __init__(self):
        # na primeira vez usa os dados de exemplo; depois carrega o que foi salvo
        if not os.path.exists(dados.ARQUIVO_CLIENTES):
            self.produtos, self.clientes, self.cupons = dados.criar_seed()
        else:
            self.produtos = dados.carregar_produtos()
            self.clientes = dados.carregar_clientes()
            self.cupons = dados.carregar_cupons()
        self.pedidos = []
        self.carrinhos = {}  # um carrinho por cliente (a chave é o id do cliente)

    def salvar(self):
        """Grava tudo nos arquivos JSON."""
        dados.salvar_produtos(self.produtos)
        dados.salvar_clientes(self.clientes)
        dados.salvar_cupons(self.cupons)
        dados.salvar_pedidos(self.pedidos)

    def proximo_id_pedido(self):
        """Descobre o número do próximo pedido (continua depois dos pedidos já salvos)."""
        maior = 0
        for resumo in dados.carregar_pedidos():
            if resumo["id"] > maior:
                maior = resumo["id"]
        for pedido in self.pedidos:
            if pedido.id > maior:
                maior = pedido.id
        return maior + 1

    def proximo_id_cliente(self):
        """Descobre o id do próximo cliente (o maior id existente + 1)."""
        maior = 0
        for cliente in self.clientes:
            if int(cliente.id) > maior:
                maior = int(cliente.id)
        return str(maior + 1)