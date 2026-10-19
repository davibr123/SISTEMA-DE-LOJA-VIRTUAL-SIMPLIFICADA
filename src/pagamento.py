from datetime import date

class Pagamento:
    """Representa o pagamento de um pedido (data, forma, valor)."""

    FORMAS_VALIDAS = ["PIX", "CREDITO", "DEBITO", "BOLETO"]

    def __init__(self, forma, valor, data_pagamento=None):
        self.forma = forma
        self.valor = valor
        self.data_pagamento = data_pagamento if data_pagamento else date.today()

    @property
    def forma(self):
        return self._forma

    @forma.setter
    def forma(self, valor):
        if valor not in self.FORMAS_VALIDAS:
            raise ValueError(f"Forma de pagamento inválida. Use: {self.FORMAS_VALIDAS}")
        self._forma = valor

    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self, quantia):
        if quantia <= 0:
            raise ValueError("Valor do pagamento deve ser maior que zero")
        self._valor = quantia

    def __str__(self):
        return f"Pagamento {self.forma} de R${self.valor:.2f} em {self.data_pagamento}"