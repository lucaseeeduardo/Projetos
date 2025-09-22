# Desafio 033: faça um programa que mostre se um número é maior que outro

a = int(input('Número 1: '))
b = int(input('Número 2: '))
c = int(input('Número 3: '))

lista = [a, b, c]
lista_ordenada = sorted(lista)

print('O maior valor é {}!'.format(lista_ordenada[2]))
print('O menor valor é {}'.format(lista_ordenada[0]))

# ou assim

n1 = int(input('Digite um valor inteiro: '))
n2 = int(input('Digite um valor inteiro: '))
n3 = int(input('Digite um valor inteiro: '))

if n1 > n2 > n3:
    print(f'{n1} é o maior valor! Enquanto {n3} é o menor.')
if n1 > n3 > n2:
    print(f'{n1} é o maior valor! Enquanto {n2} é o menor')
if n2 > n3 > n1:
    print(f'{n2} é o maior valor! Enquanto {n1} é o menor')
if n2 > n1 > n3:
    print(f'{n2} é o maior valor! Enquanto {n3} é o menor')
if n3 > n1 > n2:
    print(f'{n3} é o maior valor! Enquanto {n2} é o menor')
if n3 > n2 > n1:
    print(f'{n3} é o maior valor! Enquanto {n1} é o menor')

# ou

na1 = float(input('Digite um número: '))
na2 = float(input('Digite outro número: '))
na3 = float(input('Digite mais um número: '))

menor = na1
maior = na3

if na2 < na1 and na2 < na3:
    menor = na2
if na3 < na1 and na3 < na2:
    menor = na3
if na1 > na2 and na1 > na3:
    maior = na1
if na2 > na1 and na2 > na3:
    maior = na2

print(f'O maior número é {maior}')
print(f'O menor número é {menor}')
