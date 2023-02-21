from time import sleep
print('Contagem de 1 até 10 de 1 em 1')
for c in range(1, 11):
    print(c, end=' ')
    sleep(0.22)
print('FIM!')
for c in range(10, -1, -2):
    print(c, end=' ')
    sleep(0.22)
print('FIM!')


def contador(inicio, fim, passo):
    if passo < 0:
        passo = passo*-1
    if passo == 0:
        passo = 1

    print('='*35)
    print(f'Contagem de {inicio} até {fim} de {passo} em {passo}.')

    for d in range(inicio, fim-1, -passo):
        print(d, end=' ')
    if inicio >= fim:
        print('FIM!')
    else:
        for d in range(inicio, fim+1, passo):
            print(d, end=' ')
        print('FIM!')


print('Agora é sua vez de personalizar a contagem!')
contador(int(input('Início: ')), int(input('Fim: ')), int(input('Passo: ')))
