lista = []
i = 0
while True:
    lista.append(int(input('Digite um valor: ')))
    if lista[i] in lista[0:i]:
        lista.remove(lista[i])
        i = i - 1
        print('Valor duplicado, não vou adicionar...')
    else:
        print('Valor adicionado com sucesso.')
    i = i + 1
    escolha = str(input('Quer continuar? [S/N] '))
    if escolha not in 'Ss':
        break
lista.sort()
print(f'Você digitou os valores: {lista}')
