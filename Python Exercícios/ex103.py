
jogador = str(input("Nome do jogador: ")).strip()
gols = str(input("Número de gols: ")).strip()

if(jogador == ''):
    jogador = '<desconhecido>'

if(gols == ''):
    gols = 0
elif(gols.isnumeric()):
    gols=int(gols)
else:
    gols = 0
def ficha(jogador="<desconhecido>", gols=0):
    print(f"O jogador {jogador} fez {gols} gol(s) no campeonato")

ficha(jogador, gols)
ficha(jogador)
ficha()