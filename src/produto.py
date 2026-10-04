class Produto:
    """Representa um produto do catálogo da loja (SKU, nome, categoria, preço, estoque)."""
   
    def __init__(self, sku, nome, categoria, preco, estoque, ativo=True):
        self.sku = sku
        self.nome = nome
        self.categoria = categoria
        self.preco = preco
        self.estoque = estoque
        self.ativo = ativo

    @property
    def preco(self):
        return self._preco

    @preco.setter
    def preco(self, valor):
        if valor <= 0:
            raise ValueError("Preço deve ser maior que zero")
        self._preco = valor

    @property
    def estoque(self):
        return self._estoque

    @estoque.setter
    def estoque(self, valor):
        if valor < 0:
            raise ValueError("Estoque não pode ser negativo")
        self._estoque = valor

    def __str__(self):
        return f"{self.nome} (SKU: {self.sku}) - R${self.preco:.2f}"

    def __repr__(self):
        return f"Produto(sku='{self.sku}', nome='{self.nome}', preco={self.preco})"

    def __eq__(self, outro):
        return self.sku == outro.sku

    def __lt__(self, outro):
        return self.preco < outro.preco