# Desafio 22 - nome completo maiúsculo, minúsculo, quantidade de caracteres sem espaços, letras do primeiro nome

nome = str(input('Insira seu nome completo aqui: ')).strip()

print('Seu nome em letras maiúsculas é: {}.'.format(nome.upper()))
print('Seu nome em letras minúsculas é: {}.'.format(nome.lower()))
print('O seu nome tem {} caracteres sem espaços.'.format(len(''.join(nome.split()))))

print('O primeiro nome tem {} letras.'.format(len(nome.split()[0])))

# ou assim

nom1 = str(input('Digite seu nome: ')).strip()

print('Analisando seu nome ...')

print(f'Seu nome em maiúsculas é: {nom1.upper()}')
print(f'Seu nome em minúsculas é: {nom1.lower()}')
print('Seu nome ao todo tem {} letras'.format(len(''.join(nom1.split()))))
print(f'Seu primeiro nome é {nom1.split()[0]} e ele tem {len(nom1.split()[0])} letras!')
