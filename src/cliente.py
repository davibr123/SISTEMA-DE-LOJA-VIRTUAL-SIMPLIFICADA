import re

class Cliente:
    """Representa um cliente da loja (id, nome, email, CPF, endereços)."""

    def __init__(self, id, nome, email, cpf, enderecos=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.enderecos = enderecos if enderecos is not None else []

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        if "@" not in valor or "." not in valor:
            raise ValueError("Email inválido")
        self._email = valor

    @property
    def cpf(self):
        return self._cpf

    @cpf.setter
    def cpf(self, valor):
        apenas_numeros = re.sub(r"\D", "", valor)
        if len(apenas_numeros) != 11:
            raise ValueError("CPF inválido (deve ter 11 dígitos)")
        self._cpf = valor

    def __str__(self):
        return f"{self.nome} ({self.email})"

    def __repr__(self):
        return f"Cliente(nome='{self.nome}', cpf='{self.cpf}')"

    def __eq__(self, outro):
        return self.cpf == outro.cpf or self.email == outro.email