Algoritmo "Ex. 8 - C�lculo da Ilumina��o"

Var
P, nlamp, L, C, A : REAL
Inicio
      ESCREVA("Digite a largura do quarto em metros: ")
      LEIA(L)
      ESCREVA("Digite o comprimento do quarto em metros: ")
      LEIA(C)
      A <- L*C
      ESCREVA("Digite a pot�ncia das l�mpadas do quarto: ")
      LEIA(P)
      nlamp <- (A*18)/P
      ESCREVA("Para iluminar", A, " metros quadrados, � necess�rio utilizar ", nlamp, " l�mpadas de ", P, " watts")
      
Fimalgoritmo