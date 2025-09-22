# A DIFERENÇA ENTRE EX 107 e o EX108 É QUE EU DEI RETURN COMO STRING AO INVES DE INT, ENTÃO JÁ VEM FORMATADO
import moeda

p = float(input('Digite o preço: R$ '))
print(f'A metade é: {moeda.metade(p)}')
print(f'O dobro é: {moeda.dobro(p)}')
print(f'Acrescentando 50%: {moeda.aumentar(p, 50)}')
print(f'Tirando 33%: {moeda.diminuir(p, 33)}')
