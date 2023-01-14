Algoritmo "Exercício 2 - Tempo do piloto"

Var
NOME :CARACTERE
D, T, VM : REAL


Inicio

      ESCREVA("Digite o nome do piloto: ")
      LEIA(NOME)
      ESCREVA("Digite o tempo em horas: ")
      LEIA(T)
      ESCREVA("Digite a distância em quilômetros: ")
      LEIA(D)
      VM <- D/T
      ESCREVA("A velociade media do piloto ", NOME, " foi de ", VM:4:2, "km/h")
      
Fimalgoritmo