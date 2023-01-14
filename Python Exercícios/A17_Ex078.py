# Ler 5 valores, guardar em uma lista e dizer qual é maior e qual é menor
lista = []
maior = menor = 0
# insere itens na lista e vê qual é maior ou menor
for c in range(0, 5):
    lista.append(int(input(f'Digite um valor inteiro para a posição {c}: ')))
    if c == 0:
        maior = menor = lista[0]
    if lista[c] > maior:
        maior = lista[c]
    if lista[c] < menor:
        menor = lista[c]
print(f'Você digitou os valores {lista}')
print(f'O maior valor digitado foi {maior} nas posições ', end='')
for i, v in enumerate(lista):
    if v == maior:
        print(i, end='...')
print()
print(f'O menor valor digitado foi {menor} nas posições ', end='')
for i, v in enumerate(lista):
    if v == menor:
        print(i, end='...')
