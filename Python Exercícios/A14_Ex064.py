# DIGITE UM NÚMERO A SER SOMADO E 999 PARA PARAR

num = 0
soma = 0
cont = -1

while num != 999:
    soma = soma + num
    num = int(input('Digite um número [999 para parar]: '))
    cont = cont + 1
if cont == 1:
    print('Você digitou {} número e a soma foi ele mesmo {}.'.format(cont, soma))
else:
    print('Você digitou {} números e a soma entre eles foi {}.'.format(cont, soma))
