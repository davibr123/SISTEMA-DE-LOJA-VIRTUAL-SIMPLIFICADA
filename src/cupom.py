from datetime import date


class Cupom:
    """Representa um cupom de desconto (código, tipo, validade, uso máximo)."""

    TIPOS_VALIDOS = ["VALOR", "PERCENTUAL"]

    def __init__(self, codigo, tipo, valor, data_validade, uso_maximo, categorias_elegiveis=None):
        self.codigo = codigo
        self.tipo = tipo
        self.valor = valor
        self.data_validade = data_validade
        self.uso_maximo = uso_maximo
        self.categorias_elegiveis = categorias_elegiveis if categorias_elegiveis else []
        self.usos = 0

    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, valor):
        if valor not in self.TIPOS_VALIDOS:
            raise ValueError(f"Tipo inválido. Use: {self.TIPOS_VALIDOS}")
        self._tipo = valor

    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self, quantia):
        if quantia <= 0:
            raise ValueError("O valor do cupom deve ser maior que zero")
        if self.tipo == "PERCENTUAL" and quantia > 100:
            raise ValueError("Cupom percentual não pode passar de 100%")
        self._valor = quantia

    @property
    def uso_maximo(self):
        return self._uso_maximo

    @uso_maximo.setter
    def uso_maximo(self, quantidade):
        if quantidade < 1:
            raise ValueError("O uso máximo deve ser pelo menos 1")
        self._uso_maximo = quantidade

    def valido(self):
        """Verifica se o cupom ainda pode ser usado (data e uso máximo)."""
        if date.today() > self.data_validade:
            return False
        if self.usos >= self.uso_maximo:
            return False
        return True

    def aplica_a(self, categoria):
        """Verifica se o cupom vale para a categoria (lista vazia = todas)."""
        return not self.categorias_elegiveis or categoria in self.categorias_elegiveis

    def usar(self):
        """Conta mais um uso do cupom."""
        self.usos += 1

    def calcular_desconto(self, subtotal):
        """Calcula o valor de desconto a aplicar sobre um subtotal."""
        if self.tipo == "VALOR":
            return min(self.valor, subtotal)
        return subtotal * (self.valor / 100)

    def __str__(self):
        return f"Cupom {self.codigo} ({self.tipo})"