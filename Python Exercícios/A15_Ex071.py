# pergunta valor sacado (num inteiro) e informar quantas cedulas de cada valor serão entregues
# disp apenas 50, 20, 10 e 1.
valor = int(input('Qual valor você quer sacar? R$ '))

n50 = valor // 50
n20 = valor % 50 // 20
n10 = valor % 50 % 20 // 10
n01 = valor % 50 % 20 % 10 // 1

if n50 >= 1:
    print(f'Total de {n50} cédulas de R$50.')
if n20 >= 1:
    print(f'Total de {n20} cédulas de R$20.')
if n10 >= 1:
    print(f'Total de {n10} cédulas de R$10.')
if n01 >= 1:
    print(f'Total de {n01} cédulas de R$1.')
