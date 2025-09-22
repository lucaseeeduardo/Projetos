# Desafio 049: tabuada com o laço for

print('!'*20, 'TABUADA DO LUCAO', '!'*20)
num = int(input('Digite um número para saber a tabuada: '))
print('='*20)
for c in range(1, 21):
    print('{} x {:2}= {}'.format(num, c, num*c))
print('='*20)
