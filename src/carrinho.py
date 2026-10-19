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
        for item in self.itens:
            if item.produto == produto:
                item.quantidade += quantidade
                return
        self.itens.append(ItemCarrinho(produto, quantidade))

    def remover_item(self, produto):
        """Remove um produto do carrinho."""
        self.itens = [item for item in self.itens if item.produto != produto]

    def subtotal(self):
        """Soma o subtotal de todos os itens do carrinho."""
        return sum(item.subtotal for item in self.itens)

    def fechar_pedido(self, id, frete, cupom=None):
        """Transforma o carrinho em um Pedido."""
        if len(self.itens) == 0:
            raise ValueError("Carrinho vazio")

        itens_pedido = []
        for item in self.itens:
            if item.quantidade > item.produto.estoque:
                raise ValueError(f"Estoque insuficiente para {item.produto.nome}")
            itens_pedido.append(ItemPedido(item.produto, item.quantidade, item.produto.preco))

        return Pedido(id, self.cliente, itens_pedido, frete, cupom)
    
    def __len__(self):
        return sum(item.quantidade for item in self.itens)

    def __str__(self):
        return f"Carrinho de {self.cliente.nome} ({len(self)} itens) - R${self.subtotal():.2f}"