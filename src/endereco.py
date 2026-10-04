class Endereco:
    """Representa um endereço de entrega (CEP, cidade, UF)."""
    
    def __init__(self, cep, cidade, uf):
        self.cep = cep
        self.cidade = cidade
        self.uf = uf

    @property
    def uf(self):
        return self._uf

    @uf.setter
    def uf(self, valor):
        if len(valor) != 2:
            raise ValueError("UF deve ter 2 letras (ex: CE, SP)")
        self._uf = valor.upper()

    def __str__(self):
        return f"{self.cidade}/{self.uf} - CEP {self.cep}"

    def __repr__(self):
        return f"Endereco(cidade='{self.cidade}', uf='{self.uf}')"