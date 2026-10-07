from produto import Produto


class ProdutoDigital(Produto):
    """Produto digital, sem peso e sem cobrança de frete."""

    def __init__(self, sku, nome, categoria, preco, estoque, ativo=True):
        super().__init__(sku, nome, categoria, preco, estoque, ativo)