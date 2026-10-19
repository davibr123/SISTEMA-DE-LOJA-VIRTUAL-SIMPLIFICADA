class ItemPedido:
    """Item de um pedido fechado: produto, quantidade e preço na data da compra."""

    def __init__(self, produto, quantidade, preco_na_data):
        self.produto = produto
        self.quantidade = quantidade
        self.preco_na_data = preco_na_data

    @property
    def subtotal(self):
        return self.preco_na_data * self.quantidade

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} - R${self.subtotal:.2f}"