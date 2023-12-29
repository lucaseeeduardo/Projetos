def leiadinheiro(entrada):
    while True:
        valor = input(entrada).replace(',', '.').strip()
        try:
            return float(valor)
        except ValueError:
            print(f'ERRO! "{valor}" é um preço inválido!')

def resumo(p, aumento, decrescimo):

    print('A metade é: \t\t\t{}'.format(metade(p).replace('.', ',')))
    print('O dobro é: \t\t\t\t{}'.format(dobro(p).replace('.',  ',')))
    print('Acrescentando {}%: \t\t{}'.format(aumento, aumentar(p, aumento).replace('.', ',')))
    print('Tirando {}%: \t\t\t{}'.format(decrescimo, diminuir(p, decrescimo).replace('.', ',')))


def moeda(n):
    return f'R$ {n:.2f}'


def metade(n, formatacao=True):
    if formatacao:
        return f'R$ {n/2:.2f}'
    else:
        return n/2


def dobro(n, formatacao=True):
    if formatacao:
        return f'R$ {n*2:.2f}'
    else:
        return n*2


def aumentar(n, porcentagem, formatacao=True):
    if formatacao:
        return f'R$ {n*(1+porcentagem/100):.2f}'
    else:
        return n*(1+porcentagem/100)


def diminuir(n, porcentagem, formatacao=True):
    if formatacao:
        return f'R$ {n*(1-porcentagem/100):.2f}'
    else:
        return n*(1-porcentagem/100)
