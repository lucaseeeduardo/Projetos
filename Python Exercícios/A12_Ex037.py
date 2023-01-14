# Desafio 037: binário, octal e hexadecimal. conversão com base em if

num = int(input('Digite um número inteiro: '))

print('''Escolha uma das bases para conversão: 

[ 1 ] Converter para BINÁRIO
[ 2 ] Converter para OCTAL
[ 3 ] Converter para HEXADECIMAL
''')

escolha = int(input('Sua escolha: '))

print(' ')

if escolha == 1:
    print(f'{num} convertido para BINÁRIO é {bin(num)[2:]}')
elif escolha == 2:
    print(f'{num} convertido para OCTAL é {oct(num)[2:]} ')
elif escolha == 3:
    print(f'{num} convertido para HEXADECIMAL é {hex(num)[2:]}')
else:
    print('Essa opção não existe, tente novamente.')
