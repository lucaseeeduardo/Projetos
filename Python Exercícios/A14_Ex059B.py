escolha = 0
primeiro = float(input('Primeiro valor: '))
segundo = float(input('Segundo valor: '))
while escolha != 5:
    print('''[1] SOMAR
[2] MULTIPLICAR
[3] MAIOR
[4] NOVOS NÚMEROS
[5] SAIR DO PROGRAMA''')
    escolha = int(input('>>>> Qual é a sua opção? '))
    while escolha not in [1, 2, 3, 4, 5]:
        escolha = int(input('Opção inválida, tente novamente: '))
    if escolha == 1:
        print(f'A soma entre {primeiro:.2f} e {segundo:.2f} é {primeiro+segundo:.2f}!')
    elif escolha == 2:
        print(f'A multiplicação entre {primeiro:.2f} e {segundo:.2f} é {primeiro*segundo:.2f}')
    elif escolha == 3:
        if primeiro > segundo:
            print(f'O maior entre {primeiro} e {segundo} é {primeiro}.')
        elif segundo > primeiro:
            print(f'O maior entre {primeiro} e {segundo} é {segundo}.')
        else:
            print(f'Não tem maior, são números iguais. {primeiro} = {segundo}')
    elif escolha == 4:
        primeiro = float(input('Primeiro valor: '))
        segundo = float(input('Segundo valor: '))
print('Obrigado por participar!')