from datetime import date

class Pedido:
    """Representa um pedido gerado a partir do carrinho (itens, frete, desconto, status)."""
    
    STATUS_VALIDOS = ["CRIADO", "PAGO", "ENVIADO", "ENTREGUE", "CANCELADO"]

    def __init__(self, id, cliente, itens, frete, cupom=None):
        self.id = id
        self.cliente = cliente
        self.itens = itens
        self.frete = frete
        self.cupom = cupom
        self.pagamentos = []
        self.status = "CRIADO"
        self.data = date.today()

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, valor):
        if valor not in self.STATUS_VALIDOS:
            raise ValueError(f"Status inválido. Use: {self.STATUS_VALIDOS}")
        self._status = valor

    def subtotal(self):
        return sum(item.subtotal for item in self.itens)

    def desconto(self):
        if self.cupom and self.cupom.valido():
            return self.cupom.calcular_desconto(self.subtotal())
        return 0

    def total(self):
        return max(self.subtotal() - self.desconto(), 0) + self.frete.valor

    def total_pago(self):
        return sum(p.valor for p in self.pagamentos)

    def pagar(self, pagamento):
        """Registra um pagamento e marca o pedido como PAGO quando cobrir o total."""
        self.pagamentos.append(pagamento)
        if self.total_pago() >= self.total():
            self.status = "PAGO"

    def __str__(self):
        return f"Pedido {self.id} de {self.cliente.nome} - {self.status} - R${self.total():.2f}"

    def __repr__(self):
        return f"Pedido(id={self.id}, status='{self.status}', total={self.total():.2f})"