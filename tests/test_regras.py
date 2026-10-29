import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest
from datetime import date
from produto_fisico import ProdutoFisico
from produto_digital import ProdutoDigital
from produto_hibrido import ProdutoHibrido
from cliente import Cliente
from endereco import Endereco
from carrinho import Carrinho
from cupom import Cupom
from frete import Frete
from pagamento import Pagamento


# ---------- funções auxiliares (montam objetos prontos para os testes) ----------

def criar_cliente():
    cliente = Cliente("1", "Ana", "ana@email.com", "11111111111")
    cliente.enderecos.append(Endereco("63100-000", "Crato", "CE"))
    return cliente


def criar_mouse():
    return ProdutoFisico("SKU001", "Mouse", "Periféricos", 100.0, 10, 0.2)


def criar_ebook():
    return ProdutoDigital("SKU002", "Ebook", "Livros", 50.0, 100)


def criar_pedido(produto, quantidade=1, cupom=None):
    carrinho = Carrinho(criar_cliente())
    carrinho.adicionar_item(produto, quantidade)
    return carrinho.fechar_pedido(1, Frete("CE"), cupom)


# ---------- carrinho ----------

def test_carrinho_remover_item():
    mouse = criar_mouse()
    carrinho = Carrinho(criar_cliente())
    carrinho.adicionar_item(mouse, 2)
    carrinho.remover_item(mouse)
    assert len(carrinho) == 0


def test_carrinho_alterar_quantidade():
    mouse = criar_mouse()
    carrinho = Carrinho(criar_cliente())
    carrinho.adicionar_item(mouse, 2)
    carrinho.alterar_quantidade(mouse, 5)
    assert len(carrinho) == 5
    assert carrinho.subtotal() == 500.0


# ---------- estoque ----------

def test_estoque_insuficiente():
    with pytest.raises(ValueError):
        criar_pedido(criar_mouse(), 11)


def test_pagar_baixa_estoque():
    mouse = criar_mouse()
    pedido = criar_pedido(mouse, 2)
    pedido.pagar(Pagamento("PIX", pedido.total()))
    assert mouse.estoque == 8


# ---------- cupom ----------

def test_cupom_percentual():
    cupom = Cupom("DESC10", "PERCENTUAL", 10, date(2099, 12, 31), 5)
    pedido = criar_pedido(criar_mouse(), 1, cupom)
    assert pedido.total() == 105.0  # 100 - 10 de desconto + 15 de frete


def test_cupom_expirado():
    cupom = Cupom("VELHO", "PERCENTUAL", 10, date(2020, 1, 1), 5)
    with pytest.raises(ValueError):
        criar_pedido(criar_mouse(), 1, cupom)


def test_cupom_uso_maximo():
    cupom = Cupom("UNICO", "PERCENTUAL", 10, date(2099, 12, 31), 1)
    criar_pedido(criar_mouse(), 1, cupom)
    with pytest.raises(ValueError):
        criar_pedido(criar_mouse(), 1, cupom)


def test_cupom_categoria_nao_elegivel():
    cupom = Cupom("LIVROS", "PERCENTUAL", 10, date(2099, 12, 31), 5, ["Livros"])
    with pytest.raises(ValueError):
        criar_pedido(criar_mouse(), 1, cupom)  # o mouse é da categoria Periféricos


def test_desconto_nao_deixa_total_negativo():
    cupom = Cupom("GIGANTE", "VALOR", 9999, date(2099, 12, 31), 5)
    pedido = criar_pedido(criar_mouse(), 1, cupom)
    assert pedido.total() == 15.0  # só sobra o frete


# ---------- frete e herança ----------

def test_frete_por_uf():
    assert Frete("CE").valor == 15.0
    assert Frete("CE").prazo_dias == 3
    assert Frete("XX").valor == 40.0  # UF que não está na tabela usa o valor padrão


def test_produto_digital_sem_frete():
    pedido = criar_pedido(criar_ebook())
    assert pedido.total() == 50.0


def test_produto_hibrido_paga_frete():
    livro = ProdutoHibrido("SKU003", "Livro + ebook", "Livros", 80.0, 10, 0.4, "https://exemplo.com/livro")
    assert isinstance(livro, ProdutoFisico)
    assert isinstance(livro, ProdutoDigital)
    pedido = criar_pedido(livro)
    assert pedido.total() == 95.0  # 80 do livro + 15 de frete


# ---------- pagamento e estados do pedido ----------

def test_pagamento_parcial_e_total():
    pedido = criar_pedido(criar_mouse())  # total: 115
    pedido.pagar(Pagamento("PIX", 50))
    assert pedido.status == "CRIADO"
    pedido.pagar(Pagamento("PIX", 65))
    assert pedido.status == "PAGO"


def test_cancelar_pedido_pago_devolve_estoque():
    mouse = criar_mouse()
    pedido = criar_pedido(mouse, 2)
    pedido.pagar(Pagamento("PIX", pedido.total()))
    pedido.cancelar()
    assert pedido.status == "CANCELADO"
    assert mouse.estoque == 10


def test_nao_cancela_pedido_enviado():
    pedido = criar_pedido(criar_mouse())
    pedido.pagar(Pagamento("PIX", pedido.total()))
    pedido.enviar()
    with pytest.raises(ValueError):
        pedido.cancelar()


def test_fluxo_de_estados():
    pedido = criar_pedido(criar_mouse())
    pedido.pagar(Pagamento("PIX", pedido.total()))
    pedido.enviar()
    assert pedido.codigo_rastreio is not None
    pedido.entregar()
    assert pedido.status == "ENTREGUE"
    assert pedido.data_entrega is not None


# ---------- endereço ----------

def test_pedido_sem_endereco():
    cliente = Cliente("2", "Sem Endereco", "sem@email.com", "22222222222")
    carrinho = Carrinho(cliente)
    carrinho.adicionar_item(criar_mouse(), 1)
    with pytest.raises(ValueError):
        carrinho.fechar_pedido(1, Frete("CE"))