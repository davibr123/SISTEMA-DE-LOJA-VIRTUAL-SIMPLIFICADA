# SISTEMA-DE-LOJA-VIRTUAL-SIMPLIFICADA

## Descrição
Projeto da disciplina de Programação Orientada a Objetos (Tema 9).
Sistema de linha de comando (CLI) para uma loja virtual, com menu para cadastrar produtos e clientes,
montar o carrinho, fechar pedidos, pagar, enviar, entregar, cancelar e ver a nota e o relatório de vendas.

## Objetivo
Praticar modelagem orientada a objetos (herança, encapsulamento, composição) 
construindo um sistema de linha de comando (CLI) para gerenciar uma loja virtual: 
cadastro de produtos e clientes, carrinho, pedidos, pagamento, 
cálculo de frete e relatórios de vendas.

## Como executar

Os comandos devem ser rodados na pasta raiz do projeto:

```
python src/cli.py        # abre o menu da loja
python -m pytest         # roda os testes (precisa de: pip install pytest)
```

Na primeira execução o programa cria dados de exemplo (produtos, clientes e cupons).
Para recomeçar do zero, apague os arquivos `.json` da pasta `data/`.

Exemplo de uso: opção `4` (adicionar item ao carrinho), `5` (fechar pedido, pode usar o cupom `DESC10`),
`6` (pagar), `7` (enviar), `8` (entregar) e `10` (ver a nota do pedido).

## Estrutura do projeto

```
src/      código (classes, cli.py, dados.py, relatorio.py)
tests/    testes automatizados (pytest)
data/     arquivos JSON gerados pelo programa
```

## Classes

Produto
- O que é: um item vendido na loja
- Principais dados: sku (único), nome, categoria, preço (maior que 0), estoque (0 ou mais)

ProdutoFisico
- O que é: produto que tem peso e precisa ser enviado (herda de Produto)

ProdutoDigital
- O que é: produto que não paga frete (herda de Produto)

ProdutoHibrido
- O que é: produto com parte física e parte digital, como um livro impresso com e-book
- Herança múltipla: herda de ProdutoFisico e de ProdutoDigital
- Principais dados: peso e link de download. Paga frete, porque tem a parte física

Cliente
- O que é: quem compra
- Principais dados: nome, email válido, cpf válido, endereço

Endereco
- O que é: endereço de entrega do cliente
- Principais dados: cep (8 dígitos), cidade e uf (2 letras)

Carrinho
- O que é: lista de produtos que o cliente quer comprar, antes de virar pedido

ItemCarrinho
- O que é: um produto dentro do carrinho, com a quantidade (1 ou mais)

Pedido
- O que é: a compra "fechada" (depois que sai do carrinho)
- Tem um status: CRIADO → PAGO → ENVIADO → ENTREGUE (ou CANCELADO)

ItemPedido
- O que é: um produto dentro do pedido, guardando a quantidade e o preço no dia da compra

Pagamento
- O que é: o registro de que o pedido foi pago
- Principais dados: forma (PIX, CREDITO, DEBITO ou BOLETO), valor e data

Cupom
- O que é: desconto que pode ser aplicado no pedido
- Principais dados: código, tipo (VALOR ou PERCENTUAL), validade, uso máximo e categorias elegíveis

Frete
- O que é: calcula quanto custa e quanto demora a entrega, de acordo com a UF do endereço

### Como se conectam

- Produto é a classe mãe de ProdutoFisico e ProdutoDigital
- ProdutoHibrido herda de ProdutoFisico e ProdutoDigital ao mesmo tempo
- Cliente tem um ou mais Enderecos
- Cliente monta um Carrinho
- Carrinho tem vários ItemCarrinho, e cada um aponta para um Produto
- Carrinho vira um Pedido
- Pedido pertence a um Cliente
- Pedido tem vários ItemPedido
- Pedido pode usar um Cupom (opcional)
- Pedido tem Pagamentos e um Frete

### Métodos principais

- Produto: `__str__`, `__repr__`, `__eq__` (compara pelo SKU) e `__lt__` (compara pelo preço)
- Cliente: `__str__`, `__repr__` e `__eq__` (compara por CPF ou email)
- Endereco: `__str__` e `__repr__`
- Carrinho: adicionar_item, remover_item, alterar_quantidade, subtotal, fechar_pedido, `__len__` (quantidade total de itens) e `__str__`
- Pedido: pagar, enviar, entregar, cancelar, gerar_resumo (a nota do pedido), total, `__str__` e `__repr__`
- Pagamento: valida a forma e o valor
- Cupom: valido, aplica_a, usar e calcular_desconto
- Frete: calcula valor e prazo pela UF

## Regras de negócio

- **Estoque:** só cria o pedido se a quantidade for menor ou igual ao estoque. O estoque baixa quando o pedido é pago e volta se um pedido pago for cancelado.
- **Cupom:** só vale dentro da validade, antes do uso máximo e para itens de categorias elegíveis. O desconto nunca deixa o total negativo.
- **Frete:** calculado ao fechar o pedido, pela UF do endereço do cliente. Produto digital não paga frete.
- **Pagamento:** aceita pagamento parcial. O pedido vira PAGO quando o total pago cobre o total do pedido.
- **Estados:** CRIADO → PAGO → ENVIADO → ENTREGUE. Só dá para cancelar pedido