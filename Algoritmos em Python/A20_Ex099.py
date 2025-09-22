# from random import randint
#
#
# def analise():
#     print('-'*20)
#     listavalor = list()
#     for c in range(0, randint(0, 9)):
#         valor = randint(0, 9)
#         print(valor, end=' ')
#         listavalor.append(valor)
#     print(f'Foram informados {len(listavalor)} valores ao todo.')
#     print(f'O maior valor informado foi {max(listavalor)}')
#     listavalor.clear()
#
#
# analise()
# analise()
# ## fiz do jeito acima, mas não é desse jeito que o professor pediu, farei novamente abaixo:
def analise(* num):
    print('=-'*30)
    maior = 0
    print('Analisando os valores passados...')
    for k, v in enumerate(num):
        print(v, end='-')
        if k == 0:
            maior = v
        else:
            if v > maior:
                maior = v
    print(f'Foram informados {len(num)} valores ao todo')
    print(f'O maior valor informado foi {maior}')


analise(0, 2, 4, 6, 19)
analise(3, 4, 1)
analise(3, 2)
analise()
