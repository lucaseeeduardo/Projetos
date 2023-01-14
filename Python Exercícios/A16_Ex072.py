# faça um programa que leia um número de 0 até 20 e mostre ele por extenso
#num = int(input('Digite o número: '))

#while 0 > num > 20:
#    num = int(input('Número errado, tente novamente, de 0 a 20: '))

# numext = ('Zero', 'Um', 'Dois', 'Três', 'Quatro', 'Cinco', 'Seis', 'Sete', 'Oito', 'Nove',
#          'Dez', 'Onze', 'Doze', 'Treze', 'Quatorze', 'Quinze', 'Dezesseis', 'Dezessete',
#          'Dezoito', 'Dezenove', 'Vinte')

# print(f'Você digitou o número {numext[num]}')
# print(len(numext))
################ acima é como eu gostaria de fazer, e, abaixo é como deu certo kkkk, mas parece mt gambiarra
while True:

    num = int(input('Digite um número [0-20]: '))

    while num > 20 or num < 0:
        num = int(input('Digite somente números entre 0 e 20: '))
        if 0 <= num <= 20:
            break

    numext = ('Zero', 'Um', 'Dois', 'Três', 'Quatro', 'Cinco', 'Seis', 'Sete', 'Oito', 'Nove',
              'Dez', 'Onze', 'Doze', 'Treze', 'Quatorze', 'Quinze', 'Dezesseis', 'Dezessete',
              'Dezoito', 'Dezenove', 'Vinte')
    print(f'Você digitou o número {numext[num]}')
