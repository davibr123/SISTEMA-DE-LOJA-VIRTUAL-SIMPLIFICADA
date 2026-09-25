# SISTEMA-DE-LOJA-VIRTUAL-SIMPLIFICADA

## Descrição
Projeto da disciplina de Programação Orientada a Objetos (Tema 9).

## Objetivo
Praticar modelagem orientada a objetos (herança, encapsulamento, composição) 
construindo um sistema de linha de comando (CLI) para gerenciar uma loja virtual: 
cadastro de produtos e clientes, carrinho, pedidos, pagamento, 
cálculo de frete e relatórios de vendas.

### Classes

Produto
- O que é: um item vendido na loja
- Principais dados: sku, nome, preço, estoque

Cliente
- O que é: quem compra
- Principais dados: nome, email, cpf, endereço

Endereco
- O que é: endereço de entrega do cliente

Carrinho
- O que é: lista de produtos que o cliente quer comprar, antes de virar pedido

Pedido
- O que é: a compra "fechada" (depois que sai do carrinho)
- Tem um status: CRIADO → PAGO → ENVIADO → ENTREGUE (ou CANCELADO)

Pagamento
- O que é: o registro de que o pedido foi pago

Cupom
- O que é: desconto que pode ser aplicado no pedido

Frete
- O que é: calcula quanto custa e quanto demora a entrega

### Como se conectam

- Cliente tem um Endereco
- Cliente monta um Carrinho
- Carrinho tem vários Produtos dentro
- Carrinho vira um Pedido
- Pedido pertence a um Cliente
- Pedido pode usar um Cupom (opcional)
- Pedido tem um Pagamento e um Frete

### Métodos principais (previstos)

- Produto: comparar por SKU, comparar por preço
- Cliente: comparar por CPF/email
- Carrinho: adicionar item, remover item, calcular subtotal
- Pedido: fechar pedido, cancelar, gerar resumo
- Pagamento: validar se o valor pago cobre o total
- Cupom: validar se ainda é válido (data, uso)
- Frete: calcular valor e prazo

## Diagrama (UML)

```mermaid
classDiagram
    direction TB

    Cliente --> Endereco
    Cliente --> Carrinho
    Carrinho --> Produto
    Carrinho --> Pedido
    Pedido --> Cupom
    Pedido --> Pagamento
    Pedido --> Frete

    class Cliente {
        nome
        email
        cpf
    }
    class Endereco {
        cep
        cidade
        uf
    }
    class Carrinho {
        itens
    }
    class Produto {
        sku
        nome
        preco
        estoque
    }
    class Pedido {
        status
        total
    }
    class Cupom {
        codigo
        tipo
    }
    class Pagamento {
        forma
        valor
    }
    class Frete {
        valor
        prazo
    }

    classDef default fill:#1e1e2e,stroke:#8899aa,stroke-width:1px,color:#e0e0e0