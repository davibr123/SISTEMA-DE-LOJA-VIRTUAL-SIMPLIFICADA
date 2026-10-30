from item_carrinho import ItemCarrinho
from item_pedido import ItemPedido
from pedido import Pedido


class Carrinho:
    """Representa o carrinho de compras de um cliente, com itens (produto + quantidade)."""

    def __init__(self, cliente):
        self.cliente = cliente
        self.itens = []

    def adicionar_item(self, produto, quantidade):
        """Adiciona um produto ao carrinho, ou soma a quantidade se já existir."""
        if not produto.ativo:
            raise ValueError(f"{produto.nome} está inativo e não pode ser vendido")
        for item in self.itens:
            if item.produto == produto:
                item.quantidade += quantidade
                return
        self.itens.append(ItemCarrinho(produto, quantidade))

    def remover_item(self, produto):
        """Remove um produto do carrinho."""
        self.itens = [item for item in self.itens if item.produto != produto]

    def alterar_quantidade(self, produto, quantidade):
        """Muda a quantidade de um produto que já está no carrinho."""
        for item in self.itens:
            if item.produto == produto:
                item.quantidade = quantidade
                return
        raise ValueError("Produto não está no carrinho")

    def subtotal(self):
        """Soma o subtotal de todos os itens do carrinho."""
        return sum(item.subtotal for item in self.itens)

    def fechar_pedido(self, id, frete, cupom=None, endereco=None):
        """Transforma o carrinho em um Pedido."""
        if len(self.itens) == 0:
            raise ValueError("Carrinho vazio")
        if len(self.cliente.enderecos) == 0:
            raise ValueError("Cliente precisa ter um endereço para fechar o pedido")

        itens_pedido = []
        for item in self.itens:
            if not item.produto.ativo:
                raise ValueError(f"{item.produto.nome} está inativo e não pode ser vendido")
            if item.quantidade > item.produto.estoque:
                raise ValueError(f"Estoque insuficiente para {item.produto.nome}")
            itens_pedido.append(ItemPedido(item.produto, item.quantidade, item.produto.preco))

        if cupom:
            if not cupom.valido():
                raise ValueError("Cupom expirado ou sem usos disponíveis")
            if not any(cupom.aplica_a(item.produto.categoria) for item in self.itens):
                raise ValueError("Cupom não vale para nenhum item do carrinho")

        pedido = Pedido(id, self.cliente, itens_pedido, frete, cupom, endereco)
        if cupom:
            cupom.usar()
        return pedido

    def __len__(self):
        return sum(item.quantidade for item in self.itens)

    def __str__(self):
        return f"Carrinho de {self.cliente.nome} ({len(self)} itens) - R${self.subtotal():.2f}"