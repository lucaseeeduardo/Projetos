def voto(anoNascimento):
    from datetime import date
    idade = date.today().year - anoNascimento
    print(f"Sua idade é: {idade}")
    if(idade<16):
        print("NEGADO")
    elif(idade<18):
        print("OPCIONAL")
    elif(idade<65):
        print("OBRIGATÓRIO")
    elif(idade>=65):
        print("OPCIONAL")


def fatorial(num, show=False):
    if(num > 1):
        if(show):
            print(f'{num} x ', end='')
        return num * fatorial(num-1, show)
    else:
        if(show):
            print(f'1 = ', end='')
        return 1

def leiaint(stringentrada):
    num = input(stringentrada)
    if not num.isnumeric():
        while True:
            print('ERRO! Digite um número inteiro válido')
            num = input(stringentrada)
            if num.isnumeric():
                return num
    else:
        return num

def notas(*args, sit=False):
    relatorio = dict()
    soma = 0

    relatorio['total'] = len(args)
    soma = sum(args)
    relatorio['maior'] = max(args)
    relatorio['menor'] = min(args)
    relatorio['média'] = soma/len(args)
    if sit:
        if relatorio['média'] >= 7:
            relatorio['situação'] = 'BOA'
        else:
            relatorio['situação'] = 'RUIM'
    return relatorio

