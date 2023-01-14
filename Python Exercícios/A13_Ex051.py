# Desafio 050:  primeiro termo da PA e razão, mostrar 10 primeiros termos

a1 = int(input('DIGITE O PRIMEIRO TERMO DA PA: '))

r = int(input('DIGITE A RAZÃO DA PA: '))

for c in range(1, 11):
    print('O {:2}º termo é='.format(c), a1 + ((c-1)*r))
