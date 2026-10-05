class ItemCarrinho:
    """Representa um item do carrinho: um produto e a quantidade desejada."""

    def __init__(self, produto, quantidade):
        self.produto = produto
        self.quantidade = quantidade

    @property
    def quantidade(self):
        return self._quantidade

    @quantidade.setter
    def quantidade(self, valor):
        if valor < 1:
            raise ValueError("Quantidade deve ser pelo menos 1")
        self._quantidade = valor

    @property
    def subtotal(self):
        return self.produto.preco * self.quantidade

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} - R${self.subtotal:.2f}"

    def __repr__(self):
        return f"ItemCarrinho(produto='{self.produto.nome}', quantidade={self.quantidade})"