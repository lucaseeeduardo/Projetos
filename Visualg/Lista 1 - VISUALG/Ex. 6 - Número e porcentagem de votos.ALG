Algoritmo "Ex. 6 - N�mero de votos"

Var

B, N, V, TOTAL: REAL
Inicio
      ESCREVA("Digite o n�mero de votos brancos: ")
      LEIA(B)
      ESCREVA("Digite o n�mero de votos nulos: ")
      LEIA(N)
      ESCREVA("Digite o n�mero de votos v�lidos: ")
      LEIA(V)
      TOTAL <- B+N+V
      ESCREVAL("Brancos = ", B/TOTAL*100:4:2, "%")
      ESCREVAL("Nulos = ", N/TOTAL*100:4:2, "%")
      ESCREVAL("V�lidos = ", V/TOTAL*100:4:2, "%")
Fimalgoritmo