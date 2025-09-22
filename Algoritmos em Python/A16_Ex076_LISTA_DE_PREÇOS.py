print(f'{"-"*40:}')
print(f'{"LISTAGEM DE PREÇOS":^40}')
print(f'{"-"*40:}')
listagem = ('Pão', 0.90, 'Queijo KG', 42.90, 'Presunto KG', 30.50,
            'Café 500g', 17.90, 'Suco de poupa', 5.50)
for alimento in range(0, len(listagem)):
    if alimento % 2 == 0:
        print(f'{listagem[alimento]:.<30}', end='')
    else:
        print(f'R$ {listagem[alimento]:<10.2f}')
