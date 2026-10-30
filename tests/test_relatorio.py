import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from relatorio import (
    faturamento_por_periodo,
    top_produtos,
    vendas_por_categoria,
    vendas_por_uf,
    pedidos_por_status,
)

# pedidos de exemplo, no mesmo formato em que são salvos no pedidos.json
PEDIDOS = [
    {"id": 1, "cliente": "Ana", "data": "2026-10-01", "status": "ENTREGUE", "total": 195.0, "uf": "CE",
     "itens": [{"sku": "S1", "nome": "Mouse", "categoria": "Periféricos", "quantidade": 2, "preco": 90.0}]},
    {"id": 2, "cliente": "Bia", "data": "2026-10-15", "status": "PAGO", "total": 160.0, "uf": "PE",
     "itens": [{"sku": "S1", "nome": "Mouse", "categoria": "Periféricos", "quantidade": 1, "preco": 90.0},
               {"sku": "S2", "nome": "Livro", "categoria": "Livros", "quantidade": 1, "preco": 50.0}]},
    {"id": 3, "cliente": "Caio", "data": "2026-10-20", "status": "CANCELADO", "total": 265.0, "uf": "CE",
     "itens": [{"sku": "S2", "nome": "Livro", "categoria": "Livros", "quantidade": 5, "preco": 50.0}]},
    {"id": 4, "cliente": "Dani", "data": "2026-10-25", "status": "CRIADO", "total": 99.0, "uf": "CE",
     "itens": [{"sku": "S3", "nome": "Curso", "categoria": "Cursos", "quantidade": 1, "preco": 99.0}]},
]


def test_faturamento_e_ticket_medio_do_periodo():
    quantidade, faturamento, ticket_medio = faturamento_por_periodo(PEDIDOS, "2026-10-01", "2026-10-31")
    assert quantidade == 2  # só contam os pedidos pagos, enviados ou entregues
    assert faturamento == 355.0
    assert ticket_medio == 177.5


def test_faturamento_respeita_as_datas():
    quantidade, faturamento, ticket_medio = faturamento_por_periodo(PEDIDOS, "2026-10-10", "2026-10-31")
    assert quantidade == 1
    assert faturamento == 160.0


def test_faturamento_sem_pedidos():
    assert faturamento_por_periodo([], "2026-01-01", "2026-12-31") == (0, 0, 0)


def test_top_produtos():
    assert top_produtos(PEDIDOS, 2) == [("Mouse", 3), ("Livro", 1)]
    assert top_produtos(PEDIDOS, 1) == [("Mouse", 3)]


def test_vendas_por_categoria():
    assert vendas_por_categoria(PEDIDOS) == {"Periféricos": 270.0, "Livros": 50.0}


def test_vendas_por_uf():
    assert vendas_por_uf(PEDIDOS) == {"CE": 195.0, "PE": 160.0}


def test_pedidos_por_status():
    resultado = pedidos_por_status(PEDIDOS)
    assert resultado["ENTREGUE"] == (1, 25.0)
    assert resultado["CANCELADO"] == (1, 25.0)
    assert len(resultado) == 4


def test_pedidos_por_status_sem_pedidos():
    assert pedidos_por_status([]) == {}