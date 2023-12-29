def leiaint(stringentrada):
    while True:
        try:
            num = input(stringentrada)
            print(f'Você digitou: {int(num)}')
        except Exception as erro:
            print(f'Deu erro: {erro.__class__}')
        else:
            return num
        finally:
            print('Obrigado!')

def leiafloat(stringentrada):
    while True:
        try:
            num = input(stringentrada)
            print(f'Você digitou: {float(num)}')
        except Exception as erro:
            print(f'Deu erro: {erro.__class__}')
        else:
            return num
        finally:
            print('Obrigado!')


num = float(leiafloat('Digite o float: '))
n = int(leiaint('Digite o int: '))

