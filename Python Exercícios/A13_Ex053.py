# Desafio 053: crie um programa que saiba o que é um palíndromo desconsiderando os espaços.

frase = str(input('Digite uma frase para saber se é palíndromo: ')).strip().upper()

palavras = frase.split()
junto = ''.join(palavras)
inverso = ''
for letra in range(len(junto)-1, -1, -1):
    inverso = inverso + junto[letra]
if inverso == junto:
    print(f'Temos um palíndromo! {junto} é igual a {inverso}')
else:
    print(f'{frase} não é palíndromo :(')