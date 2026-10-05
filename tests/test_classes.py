import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest
from produto import Produto
from cliente import Cliente
from endereco import Endereco
from carrinho import Carrinho


def test_criar_produto_valido():
    p = Produto("SKU001", "Mouse", "Periféricos", 50.0, 10)
    assert p.nome == "Mouse"
    assert p.preco == 50.0


def test_produto_preco_invalido():
    with pytest.raises(ValueError):
        Produto("SKU002", "Teclado", "Periféricos", -10, 5)


def test_produto_estoque_invalido():
    with pytest.raises(ValueError):
        Produto("SKU003", "Monitor", "Periféricos", 800, -1)


def test_produto_eq_por_sku():
    p1 = Produto("SKU001", "Mouse", "Periféricos", 50.0, 10)
    p2 = Produto("SKU001", "Mouse Gamer", "Periféricos", 90.0, 5)
    assert p1 == p2


def test_cliente_email_invalido():
    with pytest.raises(ValueError):
        Cliente("1", "Davi", "email-invalido", "12345678900")


def test_cliente_cpf_invalido():
    with pytest.raises(ValueError):
        Cliente("1", "Davi", "davi@email.com", "123")


def test_endereco_uf_invalido():
    with pytest.raises(ValueError):
        Endereco("63100-000", "Crato", "Ceara")


def test_carrinho_adicionar_item():
    cliente = Cliente("1", "Davi", "davi@email.com", "12345678900")
    carrinho = Carrinho(cliente)
    produto = Produto("SKU001", "Mouse", "Periféricos", 50.0, 10)

    carrinho.adicionar_item(produto, 2)

    assert len(carrinho) == 2
    assert carrinho.subtotal() == 100.0