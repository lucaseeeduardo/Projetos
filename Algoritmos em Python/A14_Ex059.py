# Desafio 059: informar dois números e somar, multiplicar, maior, novos números, sair do programa - menu.

num1 = int(input('Digite um número: '))
num2 = int(input('Digite outro número: '))

print('''Agora digite o que deseja fazer com eles:

      [1] Somar
      [2] Multiplicar
      [3] Maior deles
      [4] Novos números
      [5] Sair do programa.''')
op = int(input('Opção: '))

while op == 1 or op == 2 or op == 3 or op == 4:

    if op == 1:
        print(f'A soma é: {num1 + num2}')
    if op == 2:
        print(f'O resultado da multiplicação é: {num1 * num2}')
    if op == 3:
        if num1 > num2:
            print(f'O maior número é o: {num1}')
        elif num2 > num1:
            print(f'O maior número é o: {num2}')
        else:
            print('Os dois números são iguais.')
    if op == 4:
        num1 = int(input('Digite um número: '))
        num2 = int(input('Digite outro número: '))

    op = int(input('Opção: '))
if op == 5:
    print('Você saiu do programa, obrigado por sua presença!')
