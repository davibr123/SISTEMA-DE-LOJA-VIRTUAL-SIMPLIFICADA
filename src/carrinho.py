from item_carrinho import ItemCarrinho

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

    def __len__(self):
        return sum(item.quantidade for item in self.itens)

    def __str__(self):
        return f"Carrinho de {self.cliente.nome} ({len(self)} itens) - R${self.subtotal():.2f}"