def ficha(jogador="<desconhecido>", gols=0):
    if (jogador == ''):
        jogador = '<desconhecido>'

    if (gols == ''):
        gols = 0
    elif (gols.isnumeric()):
        gols = int(gols)
    else:
        gols = 0
    print(f"O jogador {jogador} fez {gols} gol(s) no campeonato")

def pyhelp():
    while True:
        entrada = input('Função ou Biblioteca: ')
        if entrada == 'FIM':
            break
        help(entrada)