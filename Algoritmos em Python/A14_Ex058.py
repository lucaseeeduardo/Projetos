# Desafio 058: computador vai pensar num número de 0 a 10 e eu tenho qeu adivinhar.
# após isso, aparecerá quantas vezes levou para o jogador acertar
# numero computador, numero jogador(if correto if incorreto), contador de vezes numero jogador

from random import randint
print('Tente adivinhar o número, MWAHAHAHAH, \n'
      '\n'
      ' \033[31mQUE OS JOGOS COMECEM\033[m')

n_jogador = 12
n_computador = randint(0, 10)
tentativas = 0

while n_jogador != n_computador:
    n_jogador = int(input('Qual foi o número? '))
    if n_jogador > 10:
        print('Esse número não está nas alternativas, tente novamente.')
    tentativas = tentativas + 1
print(f'Parabéns, você ganhou! Eu escolhi {n_computador} e você {n_jogador}!')
print(f'O número de tentativas para chegar no resultado foi de: {tentativas}')
