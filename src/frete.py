class Frete:
    """Calcula o frete de um pedido com base em CEP/UF ou tabela por cidade."""

    TABELA = {
        "CE": (15.0, 3),
        "PE": (20.0, 5),
        "SP": (30.0, 7),
    }
    PADRAO = (40.0, 10)

    def __init__(self, uf):
        self.uf = uf.upper()
        self.valor, self.prazo_dias = self.TABELA.get(self.uf, self.PADRAO)

    def __str__(self):
        return f"Frete para {self.uf}: R${self.valor:.2f} ({self.prazo_dias} dias úteis)"