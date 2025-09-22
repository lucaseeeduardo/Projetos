# fazer novamente no sábado!!! 07/08/22 feito!! foi no domingo, terminei todos os exercícios no sabado e fiz a prova no domingo, revisando alguns mais importantes!
a1 = int(input('Primeiro termo: '))
r = int(input('Razão da PA: '))
# an = a1 + r*(n-1)
termo = -1
while termo < 9:
    termo = termo + 1
    print(a1+(termo*r), '→' if termo < 9 else '', end=' ')
