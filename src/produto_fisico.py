from produto import Produto


class ProdutoFisico(Produto):
    """Produto físico, que tem peso e gera cobrança de frete."""

    def __init__(self, sku, nome, categoria, preco, estoque, peso, ativo=True):
        super().__init__(sku, nome, categoria, preco, estoque, ativo)
        self.peso = peso

    @property
    def peso(self):
        return self._peso

    @peso.setter
    def peso(self, valor):
        if valor <= 0:
            raise ValueError("O peso deve ser maior que zero")
        self._peso = valor




























































        