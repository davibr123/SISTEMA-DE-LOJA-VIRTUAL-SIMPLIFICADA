import json
import os
from datetime import date
from produto import Produto
from produto_fisico import ProdutoFisico
from produto_digital import ProdutoDigital
from cliente import Cliente
from endereco import Endereco
from cupom import Cupom
from produto_hibrido import ProdutoHibrido

ARQUIVO_PRODUTOS = "data/produtos.json"
ARQUIVO_CLIENTES = "data/clientes.json"
ARQUIVO_CUPONS = "data/cupons.json"
ARQUIVO_PEDIDOS = "data/pedidos.json"


def gravar(caminho, lista):
    """Grava uma lista no arquivo JSON (cria a pasta data se ela não existir)."""
    os.makedirs("data", exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(lista, arquivo, indent=2, ensure_ascii=False)


def ler(caminho):
    """Lê a lista do arquivo JSON. Se o arquivo não existir, devolve uma lista vazia."""
    if not os.path.exists(caminho):
        return []
    with open(caminho, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def salvar_produtos(produtos):
    """Salva os produtos, guardando se cada um é físico, digital, híbrido ou comum."""
    lista = []
    for p in produtos:
        dado = {
            "sku": p.sku,
            "nome": p.nome,
            "categoria": p.categoria,
            "preco": p.preco,
            "estoque": p.estoque,
            "ativo": p.ativo,
            "tipo": "comum",
        }
        if isinstance(p, ProdutoHibrido):  # tem que vir antes: o híbrido também é físico e digital
            dado["tipo"] = "hibrido"
            dado["peso"] = p.peso
            dado["link_download"] = p.link_download
        elif isinstance(p, ProdutoFisico):
            dado["tipo"] = "fisico"
            dado["peso"] = p.peso
        elif isinstance(p, ProdutoDigital):
            dado["tipo"] = "digital"
        lista.append(dado)
    gravar(ARQUIVO_PRODUTOS, lista)


def carregar_produtos():
    """Lê os produtos do arquivo e recria cada um com o tipo certo."""
    produtos = []
    for d in ler(ARQUIVO_PRODUTOS):
        if d["tipo"] == "hibrido":
            produto = ProdutoHibrido(d["sku"], d["nome"], d["categoria"], d["preco"], d["estoque"], d["peso"], d["link_download"], d["ativo"])
        elif d["tipo"] == "fisico":
            produto = ProdutoFisico(d["sku"], d["nome"], d["categoria"], d["preco"], d["estoque"], d["peso"], d["ativo"])
        elif d["tipo"] == "digital":
            produto = ProdutoDigital(d["sku"], d["nome"], d["categoria"], d["preco"], d["estoque"], d["ativo"])
        else:
            produto = Produto(d["sku"], d["nome"], d["categoria"], d["preco"], d["estoque"], d["ativo"])
        produtos.append(produto)
    return produtos


def salvar_clientes(clientes):
    """Salva os clientes junto com os endereços de cada um."""
    lista = []
    for c in clientes:
        enderecos = []
        for e in c.enderecos:
            enderecos.append({"cep": e.cep, "cidade": e.cidade, "uf": e.uf})
        lista.append({"id": c.id, "nome": c.nome, "email": c.email, "cpf": c.cpf, "enderecos": enderecos})
    gravar(ARQUIVO_CLIENTES, lista)


def carregar_clientes():
    """Lê os clientes do arquivo."""
    clientes = []
    for d in ler(ARQUIVO_CLIENTES):
        enderecos = []
        for e in d["enderecos"]:
            enderecos.append(Endereco(e["cep"], e["cidade"], e["uf"]))
        clientes.append(Cliente(d["id"], d["nome"], d["email"], d["cpf"], enderecos))
    return clientes


def salvar_cupons(cupons):
    """Salva os cupons, incluindo quantas vezes cada um já foi usado."""
    lista = []
    for c in cupons:
        lista.append({
            "codigo": c.codigo,
            "tipo": c.tipo,
            "valor": c.valor,
            "data_validade": str(c.data_validade),
            "uso_maximo": c.uso_maximo,
            "categorias": c.categorias_elegiveis,
            "usos": c.usos,
        })
    gravar(ARQUIVO_CUPONS, lista)


def carregar_cupons():
    """Lê os cupons do arquivo."""
    cupons = []
    for d in ler(ARQUIVO_CUPONS):
        validade = date.fromisoformat(d["data_validade"])
        cupom = Cupom(d["codigo"], d["tipo"], d["valor"], validade, d["uso_maximo"], d["categorias"])
        cupom.usos = d["usos"]
        cupons.append(cupom)
    return cupons


def carregar_pedidos():
    """Lê o resumo dos pedidos salvos."""
    return ler(ARQUIVO_PEDIDOS)


def salvar_pedidos(pedidos):
    """Salva o resumo dos pedidos. Os pedidos de execuções anteriores continuam no arquivo."""
    salvos = carregar_pedidos()
    for p in pedidos:
        resumo = {
            "id": p.id,
            "cliente": p.cliente.nome,
            "data": str(p.data),
            "status": p.status,
            "total": p.total(),
        }
        # se o pedido já estava no arquivo, troca pelo resumo novo; se não, adiciona
        achou = False
        for i in range(len(salvos)):
            if salvos[i]["id"] == p.id:
                salvos[i] = resumo
                achou = True
        if not achou:
            salvos.append(resumo)
    gravar(ARQUIVO_PEDIDOS, salvos)


def criar_seed():
    """Cria dados de exemplo (produtos, clientes e cupons) para a primeira vez que o programa roda."""
    produtos = [
        ProdutoFisico("SKU001", "Mouse gamer", "Periféricos", 140.0, 20, 0.2),
        ProdutoFisico("SKU002", "Teclado mecânico", "Periféricos", 250.0, 15, 0.9),
        ProdutoDigital("SKU003", "Curso de Python", "Cursos", 99.0, 999),
        ProdutoHibrido("SKU004", "Livro de Python + e-book", "Livros", 80.0, 30, 0.4, "https://exemplo.com/ebook-python"),
    ]
    clientes = [
        Cliente("1", "Ana Souza", "ana@email.com", "111.111.111-11", [Endereco("63100-000", "Crato", "CE")]),
        Cliente("2", "Carlos Lima", "carlos@email.com", "222.222.222-22", [Endereco("50000-000", "Recife", "PE")]),
    ]
    cupons = [
        Cupom("DESC10", "PERCENTUAL", 10, date(2030, 12, 31), 100),
        Cupom("CURSO20", "VALOR", 20, date(2030, 12, 31), 50, ["Cursos"]),
    ]
    return produtos, clientes, cupons