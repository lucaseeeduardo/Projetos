# fazer novamente no sábado!!! 07/08/22 feito!! foi no
# domingo, terminei todos os exercícios no sabado e fiz
# a prova no domingo, revisando alguns mais importantes!
primeiro = int(input('Primeiro termo: '))
r = int(input('Razão da PA: '))
# a1 + (r*(n-1))
n = 0
termo = 1
total = 10
mais = 0

while n < total:
    n += 1
    termo = primeiro + (r*(n-1))
    print(termo, end=' ')
    if n >= total:
        print()
        mais = int(input('Quantos termos você quer a mais? '))
        total = total + mais
