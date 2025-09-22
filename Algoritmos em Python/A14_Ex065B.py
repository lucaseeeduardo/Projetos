# digitar um número, perguntar se quer continuar e fazer a media, com maior e menor valor aparecendo
ask = 'S'
soma = 0
cont = 0
lista = []

while ask in 'Ss':
    num = int(input('Digite um número: '))
    ask = str(input('Quer continuar? [S/N]: ')).strip().upper()[0]
    soma = soma + num
    cont = cont + 1
    lista = lista + [num]

media = soma/cont
print('Você digitou {} números e a média deles foi {}.'.format(cont, media))
print('O maior valor foi {} e o menor foi {}.'.format(max(lista), min(lista)))
