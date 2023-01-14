# TOTAL DE PESSOAS, MAIORES E MENORES PESOS COM NOME
pessoas = list()
dados = []
escolha = 'Ss'
lista_maiores = list()
lista_menores = list()
maior = menor = 0
while escolha not in 'Nn' and escolha in 'Ss':
    dados.append(str(input('Nome: ')))
    dados.append(float(input('Peso: ')))
    pessoas.append(dados[:])
    if len(pessoas) == 1:
        maior = menor = dados[1]
    else:
        if dados[1] > maior:
            maior = dados[1]
        if dados[1] < menor:
            menor = dados[1]
    dados.clear()
    escolha = str(input('Quer continuar? [S/N] '))
# nesse ponto, eu vou ter pessoas = [['Lucas', 57], ['Maria', 30], ['Pedro', 60], ['João', 57], ['Luana', 60]]
# e também achei o maior e menor peso
for cadastro in pessoas:
    if cadastro[1] == maior:
        lista_maiores.append(cadastro)
    if cadastro[1] == menor:
        lista_menores.append(cadastro)
# aqui eu faço uma lista dos que possuem os maiores e menores pesos.
# lista_maiores = [['Pedro', 60], ['Luana', 60]]
# lista_menores = [['Maria', 30]]
print(f'Foram {len(pessoas)} pessoas cadastradas.')
print(f'O maior peso foi de {maior} kg. Peso de: ', end='')
for maiores in lista_maiores:
    print(maiores[0], end=' ')
# aqui eu rodo toda a lista de maiores e preciso printar maiores[0] para o nome. Abaixo a mesma coisa.
print(f'\nO menor peso foi de {menor} kg. Peso de: ', end='')
for menores in lista_menores:
    print(menores[0], end=' ')
