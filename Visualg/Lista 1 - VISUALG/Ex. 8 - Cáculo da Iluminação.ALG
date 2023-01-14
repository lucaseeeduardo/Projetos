Algoritmo "Ex. 8 - Cálculo da Iluminação"

Var
P, nlamp, L, C, A : REAL
Inicio
      ESCREVA("Digite a largura do quarto em metros: ")
      LEIA(L)
      ESCREVA("Digite o comprimento do quarto em metros: ")
      LEIA(C)
      A <- L*C
      ESCREVA("Digite a potência das lâmpadas do quarto: ")
      LEIA(P)
      nlamp <- (A*18)/P
      ESCREVA("Para iluminar", A, " metros quadrados, é necessário utilizar ", nlamp, " lâmpadas de ", P, " watts")
      
Fimalgoritmo