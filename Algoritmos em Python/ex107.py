import moeda

p = float(input('Digite o preço: '))
print(f'A metade é: {moeda.metade(p):.2f}')
print(f'O dobro é: {moeda.dobro(p):.2f}')
print(f'Acrescentando 50%: {moeda.aumentar(p, 50):.2f}')
print(f'Tirando 33%: {moeda.diminuir(p, 33):.2f}')
