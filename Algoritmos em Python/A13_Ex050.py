# Desafio 050:  ler 6 números inteiros e mostrar a soma de apenas os pares, se for ímpar, desconsiderar
# aperta tab pra colocar o bloco pra direita e shift+tab pra colocar pra esquerda

s = 0
cont = 0
for c in range(1, 7):
    num = int(input(f'Digite o {c} número inteiro: '))
    if num % 2 == 0:
        cont = cont + 1
        s = s + num
    else:
        print('Como esse valor não é par, foi desconsiderado da soma.')
print('='*30)
print(f'A soma total de números pares foi de: {s}, e você me informou {cont} números pares.')
