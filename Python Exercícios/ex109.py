# 108 e 109 ficou igual, mas é só acrescentar o FALSE como parametro de entrada na função que já muda
import moeda

p = float(input('Digite o preço: R$ '))
print(f'A metade é: {moeda.metade(p, False)}')
print(f'O dobro é: {moeda.dobro(p)}')
print(f'Acrescentando 50%: {moeda.aumentar(p, 50, False)}')
print(f'Tirando 33%: {moeda.diminuir(p, 33)}')
