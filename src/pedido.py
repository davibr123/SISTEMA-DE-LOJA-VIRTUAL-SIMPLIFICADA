import random
from datetime import date, datetime
from configuracao import carregar_settings


class Pedido:
    """Representa uma compra fechada: cliente, itens, frete, cupom, pagamentos e status."""

    STATUS_VALIDOS = ["CRIADO", "PAGO", "ENVIADO", "ENTREGUE", "CANCELADO"]

    def __init__(self, id, cliente, itens, frete, cupom=None, endereco=None):
        self.id = id
        self.cliente = cliente
        self.itens = itens
        # se nenhum endereço for escolhido, usa o primeiro do cliente
        if endereco is None and len(cliente.enderecos) > 0:
            endereco = cliente.enderecos[0]
        self.endereco = endereco
        self.frete = frete
        self.cupom = cupom
        self.pagamentos = []
        self.status = "CRIADO"
        self.criado_em = datetime.now()
        self.data = date.today()
        self._desconto = self._calcular_desconto()
        self.codigo_rastreio = None
        self.data_entrega = None

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

    def _calcular_desconto(self):
        """Calcula o desconto uma vez só, sobre os itens que o cupom aceita."""
        if self.cupom is None:
            return 0
        base = sum(item.subtotal for item in self.itens if self.cupom.aplica_a(item.produto.categoria))
        return self.cupom.calcular_desconto(base)

    def desconto(self):
        return self._desconto

    def valor_frete(self):
        """Frete é zero se todos os produtos do pedido forem digitais."""
        if any(item.produto.gera_frete for item in self.itens):
            return self.frete.valor
        return 0

    def total(self):
        return max(self.subtotal() - self.desconto(), 0) + self.valor_frete()

    def total_pago(self):
        return sum(p.valor for p in self.pagamentos)

    def baixar_estoque(self):
        """Tira do estoque a quantidade de cada item do pedido."""
        for item in self.itens:
            item.produto.estoque -= item.quantidade

    def repor_estoque(self):
        """Devolve ao estoque a quantidade de cada item do pedido."""
        for item in self.itens:
            item.produto.estoque += item.quantidade

    def pagar(self, pagamento):
        """Registra um pagamento e, ao cobrir o total, marca como PAGO e baixa o estoque."""
        if self.status != "CRIADO":
            raise ValueError("Só é possível pagar um pedido CRIADO")
        self.pagamentos.append(pagamento)
        if self.total_pago() >= self.total():
            self.baixar_estoque()
            self.status = "PAGO"

    def enviar(self):
        """Marca o pedido como ENVIADO e gera um código de rastreio fictício."""
        if self.status != "PAGO":
            raise ValueError("Só é possível enviar um pedido PAGO")
        self.codigo_rastreio = "BR" + str(random.randint(100000000, 999999999))
        self.status = "ENVIADO"

    def entregar(self):
        """Marca o pedido como ENTREGUE e guarda a data de entrega."""
        if self.status != "ENVIADO":
            raise ValueError("Só é possível entregar um pedido ENVIADO")
        self.data_entrega = date.today()
        self.status = "ENTREGUE"

    def cancelar(self):
        """Cancela o pedido. Pedido pago só pode ser cancelado dentro da janela de horas do settings.json."""
        if self.status not in ("CRIADO", "PAGO"):
            raise ValueError("Só é possível cancelar um pedido CRIADO ou PAGO")
        if self.status == "PAGO":
            horas_passadas = (datetime.now() - self.criado_em).total_seconds() / 3600
            janela = carregar_settings()["janela_cancelamento_horas"]
            if horas_passadas > janela:
                raise ValueError(f"A janela de cancelamento ({janela} horas) já passou")
            self.repor_estoque()  # o estoque só tinha saído se o pedido estava pago
        self.status = "CANCELADO"

    def gerar_resumo(self):
        """Monta a nota textual do pedido: itens, valores, endereço e pagamentos."""
        linhas = [f"===== NOTA DO PEDIDO {self.id} ====="]
        linhas.append(f"Cliente: {self.cliente.nome}")
        linhas.append(f"Endereço: {self.endereco}")
        linhas.append(f"Status: {self.status}")
        linhas.append("Itens:")
        for item in self.itens:
            linhas.append(f"  - {item}")
        linhas.append(f"Subtotal: R${self.subtotal():.2f}")
        linhas.append(f"Desconto: R${self.desconto():.2f}")
        if self.valor_frete() > 0:
            linhas.append(f"Frete: R${self.valor_frete():.2f} ({self.frete.prazo_dias} dias úteis)")
        else:
            linhas.append("Frete: R$0.00")
        linhas.append(f"Total: R${self.total():.2f}")
        linhas.append("Pagamentos:")
        if self.pagamentos:
            for pagamento in self.pagamentos:
                linhas.append(f"  - {pagamento}")
        else:
            linhas.append("  (nenhum)")
        if self.codigo_rastreio:
            linhas.append(f"Rastreio: {self.codigo_rastreio}")
        return "\n".join(linhas)

    def __str__(self):
        return f"Pedido {self.id} de {self.cliente.nome} - {self.status} - R${self.total():.2f}"

    def __repr__(self):
        return f"Pedido(id={self.id}, status='{self.status}', total={self.total():.2f})"