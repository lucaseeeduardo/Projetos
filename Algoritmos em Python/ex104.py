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


n = int(leiaint('Digite um número: '))
print(f'Você digitou: {n}')
