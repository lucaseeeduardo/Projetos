Algoritmo "Ex. 10 - Quantidade de notas para sacar"

Var

n50, n20, n10, n5, n1, DINHEIRO : INTEIRO
n2 : REAL
Inicio
      ESCREVA("Digite o tanto de dinheiro que quer sacar: ")
      LEIA(DINHEIRO)
      
      n50 <- DINHEIRO DIV 50
      n20 <- DINHEIRO MOD 50 DIV 20
      n10 <- DINHEIRO MOD 50 MOD 20 DIV 10
      n5 <- DINHEIRO MOD 50 MOD 20 MOD 10 DIV 5
      n2 <- DINHEIRO MOD 50 MOD 20 MOD 10 MOD 5 DIV 2
      n1 <- DINHEIRO MOD 50 MOD 20 MOD 10 MOD 5 MOD 2 DIV 1
      
      ESCREVAL(n50, " Notas de 50")
      ESCREVAL(n20, " Notas de 20")
      ESCREVAL(n10, " Notas de 10")
      ESCREVAL(n5, " Notas de 5")
      ESCREVAL(n2, " Notas de 2")
      ESCREVAL(n1, " Moedas de 1")


Fimalgoritmo