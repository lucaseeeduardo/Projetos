# TOTAL gasto na compra, qtd produtos > 1000 reais, nome do +barato
soma = 0
m1000 = 0
listapreco = []
listaproduto = []

while True:
    produto = str(input('Nome do produto: ')).strip()
    listaproduto = listaproduto + [produto]
    preco = float(input('Preço: R$ '))
    if preco > 1000:
        m1000 = m1000 + 1
    listapreco = listapreco + [preco]
    soma = soma + preco
    ask = str(input('Quer continuar? [S/N]: ')).strip().upper()
    if ask in 'N':
        break
    while ask not in 'SN':
        ask = str(input('Quer continuar? [S/N]: ')).strip().upper()
        if ask in 'N':
            break
print(f'O total da compra foi R${soma:.2f}.')
print(f'Temos {m1000} produtos custando mais de R$ 1000.00')
print(f'O produto mais barato foi {listaproduto[len([min(listapreco)])-1]} que custa R${min(listapreco):.2f}.')
