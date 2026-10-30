from configuracao import carregar_settings


class Frete:
    """Calcula o valor e o prazo de entrega usando a tabela do settings.json."""

    def __init__(self, uf, cidade=None):
        tabela = carregar_settings()["frete"]
        self.uf = uf.upper()
        self.cidade = cidade

        # primeiro procura a cidade, depois a UF; se não achar, usa o valor padrão
        chave_cidade = f"{cidade}/{self.uf}"
        if cidade and chave_cidade in tabela.get("por_cidade", {}):
            regra = tabela["por_cidade"][chave_cidade]
        elif self.uf in tabela["por_uf"]:
            regra = tabela["por_uf"][self.uf]
        else:
            regra = tabela["padrao"]

        self.valor = regra["valor"]
        self.prazo_dias = regra["prazo_dias"]

    def __str__(self):
        return f"Frete para {self.uf}: R${self.valor:.2f} ({self.prazo_dias} dias úteis)"