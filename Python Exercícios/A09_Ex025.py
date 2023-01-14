# Desafio 025 - identificar nome

# abaixo tá errado

nome = str(input('Qual é o seu nome? ')).strip()

nome2 = nome.upper()

print('{}, seu nome tem "SILVA": {} !'.format(nome, nome2.find('SILVA')))

# ou - aqui tá certo

n3 = str(input('Qual é o seu nome?: ')). strip()

print('Seu nome tem "SILVA"?', 'SILVA' in n3.upper())
