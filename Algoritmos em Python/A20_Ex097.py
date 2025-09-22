# fazer uma def que a parte gráfica acompanha o número de letras
def escreva(a, b, c):
    print('-'*len(a))
    print(a)
    print('-'*len(a))
    print('-' * len(b))
    print(b)
    print('-' * len(b))
    print('-' * len(c))
    print(c)
    print('-' * len(c))


escreva(str(input('Digite a frase 1: ')), str(input('Digite a frase 2: ')), str(input('Digite a frase 3: ')))
## em cima como eu fiz, embaixo como o professor fez
def frase(msg):
    tam = len(msg)
    print('-'*tam)
    print(msg)
    print('-'*tam)


frase('Lucas Eduardo Borba')
frase('Gustavo Guanabara')
frase('Curso em Vídeo')
