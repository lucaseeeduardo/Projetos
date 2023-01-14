Algoritmo "Ex. 6 - Número de votos"

Var

B, N, V, TOTAL: REAL
Inicio
      ESCREVA("Digite o número de votos brancos: ")
      LEIA(B)
      ESCREVA("Digite o número de votos nulos: ")
      LEIA(N)
      ESCREVA("Digite o número de votos válidos: ")
      LEIA(V)
      TOTAL <- B+N+V
      ESCREVAL("Brancos = ", B/TOTAL*100:4:2, "%")
      ESCREVAL("Nulos = ", N/TOTAL*100:4:2, "%")
      ESCREVAL("Válidos = ", V/TOTAL*100:4:2, "%")
Fimalgoritmo