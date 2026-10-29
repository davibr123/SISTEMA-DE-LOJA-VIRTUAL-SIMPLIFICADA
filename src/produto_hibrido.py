from produto_fisico import ProdutoFisico
from produto_digital import ProdutoDigital


class ProdutoHibrido(ProdutoFisico, ProdutoDigital):
    """Produto com uma parte física e uma digital (ex.: livro impresso + e-book).

    Herança múltipla: herda o peso do ProdutoFisico e também é um ProdutoDigital.
    Como a parte física precisa ser enviada, o produto híbrido paga frete.
    """

    gera_frete = True  # sem esta linha valeria o False do ProdutoDigital

    def __init__(self, sku, nome, categoria, preco, estoque, peso, link_download, ativo=True):
        super().__init__(sku, nome, categoria, preco, estoque, peso, ativo)
        self.link_download = link_download

    @property
    def link_download(self):
        return self._link_download

    @link_download.setter
    def link_download(self, valor):
        if valor.strip() == "":
            raise ValueError("O link de download não pode ser vazio")
        self._link_download = valor