Algoritmo "Ex. 10 - Bhaskara"

Var

a, b, c, DELTA, X1, X2 :REAL

Inicio

      ESCREVA("Informe a: ")
      LEIA(a)
      SE (a = 0) ENTAO
         ESCREVA("A equação não é de segundo grau, 'a' precisa ser <> 0")
         FIMALGORITMO
      FIMSE
      
      ESCREVA("Informe b: ")
      LEIA(b)
      ESCREVA("Informe c: ")
      LEIA(c)

      DELTA <- (b^2) - (4*a*c)

      SE ( DELTA >=0 ) ENTAO
         X1 <- ( ( - b ) + raizQ(DELTA) ) / (2*a)
         X2 <- ( ( - b ) - raizQ(DELTA) ) / (2*a)
         ESCREVAL("X1 = ", X1:4:2)
         ESCREVA("X2 = ", X2:4:2)
      SENAO
         ESCREVA("Como delta < 0, a equação não possui raízes no conjunto dos números reais.")
      FIMSE
      
Fimalgoritmo