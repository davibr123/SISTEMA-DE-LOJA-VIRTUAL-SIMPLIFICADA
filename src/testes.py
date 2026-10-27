from datetime import date
from produto_fisico import ProdutoFisico
from produto_digital import ProdutoDigital
from cliente import Cliente
from carrinho import Carrinho
from frete import Frete
from cupom import Cupom
from endereco import Endereco
from pagamento import Pagamento
from dados import salvar_produtos, carregar_produtos, salvar_pedidos
from relatorio import pedidos_por_periodo

# Herança: produto físico e digital
mouse = ProdutoFisico("SKU001", "Mouse gamer", "Periféricos", 140.0, 10, 0.2)
ebook = ProdutoDigital("SKU002", "Teclado gamer", "Periféricos", 120.0, 100)

# Persistência de produtos
salvar_produtos([mouse, ebook])
print(carregar_produtos())

# Carrinho -> Pedido
cliente = Cliente("1", "Davi", "davi@email.com", "12345678900")
cliente.enderecos.append(Endereco("63101-240", "Crato", "CE"))
carrinho = Carrinho(cliente)
carrinho.adicionar_item(mouse, 2)
carrinho.adicionar_item(ebook, 1)

cupom = Cupom("DESC10", "PERCENTUAL", 10, date(2030, 12, 31), 5)
pedido = carrinho.fechar_pedido(1, Frete("CE"), cupom)
print(pedido)

# Pagamento
pedido.pagar(Pagamento("PIX", pedido.total()))
print(pedido)

# Persistência de pedidos e relatório
salvar_pedidos([pedido])
pedidos_por_periodo("2026-01-01", "2030-12-31")
print(pedido.gerar_resumo())