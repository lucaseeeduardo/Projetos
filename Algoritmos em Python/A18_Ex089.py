# fazer um boletim
# a minha ideia foi fazer igual matriz, matriz = [[], [], []]
# dessa forma, matriz[0][0] = numero; matriz[0][1] = nome; matriz[0][2] = media
# ex: matriz[[0, 'Lucas', 9.7], [1, 'Eduardo', 9.8], matriz.append(cadastro)]
matriz = list()
cadastro = list()
escolha = 'Ss'
somanota = 0
i = 0
notasgeral = list()
notasindividual = list()
while escolha in 'Ss':
    cadastro.append(i)  # cadastro = [i]
    cadastro.append(str(input('Digite seu nome: ')))  # cadastro = [0, 'Lucas']
    for n in range(1, 3):
        notasindividual.append(float(input(f'Digite sua nota {n}: ')))
    notasgeral.append(notasindividual[:])
    somanota = somanota + notasindividual[0]  # notas[0] = [[10, 8]]
    somanota = somanota + notasindividual[1]  # somanota = 18
    media = somanota/2
    cadastro.append(media)  # cadastro = [0, 'Lucas', 10]
    matriz.append(cadastro[:])  # matriz = [[0, 'Lucas', 10]]
    # aqui é muito importante lembrar que precisa adicionar a lista como cópia, se não fica
    # interligado, tem que colocar cadastro[:] ao invés de cadastro[]
    print(matriz)
    cadastro.clear()
    notasindividual.clear()
    somanota = 0
    i += 1
    escolha = str(input('Quer continuar? [S/N]: '))
    while escolha not in 'Ss' and escolha not in 'Nn':
        escolha = str(input('DIGITE CORRETAMENTE DENTRO DAS OPÇÕES [S/N]: '))
print('No   NOME    MÉDIA')
print('-'*20)
for num in range(0, len(matriz)):
    print(matriz[num][0], end='    ')
    print(matriz[num][1], end='  ')
    print(f'{matriz[num][2]}')
descubranota = 0
while descubranota != 999:
    descubranota = int(input('Mostrar notas de qual aluno? (999 interrompe): '))
    if descubranota == 999:
        break
    while descubranota > len(matriz) - 1 or descubranota < 0:
        descubranota = int(input('Não existe essa quantidade de alunos, digite novamente (999 interrompe): '))
        if descubranota == 999:
            break
    print(f'Notas de {matriz[descubranota][1]} são {notasgeral[descubranota]}')
