frase = str(input('Digite uma frase')).strip().upper()

print('A letra A aparece {} vezes na frase.'.format(frase.count('A')))

print('A primeira letra A apareceu na posição: {}'.format(frase.find('A')+1))

print('A última letra A apareceu na posição: {} '.format(frase.rfind('A')+1))

# rfind significa procurar a partir do lado direito!
# ou assim:
nome = str(input('Digite uma frase')).strip().upper()

print(f'A letra A aparece {nome.count("A")} vezes!')
print(f'A primeira letra A apareceu na posição {nome.find("A")}!')
print(f'A última letra A apareceu na posição {nome.rfind("A")}!')
