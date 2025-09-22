Algoritmo "Ex. 3 - Quadrantes Cartesianos"

Var

x, y: REAL

Inicio
      ESCREVA("Digite x: ")
      LEIA(x)
      ESCREVA("Digite y: ")
      LEIA(y)

      // Q1  x= + y = +
      // Q2  x= - y = +
      // Q3  x= - y = -
      // Q4  x= + y = -
      SE (X > 0) E (Y = 0) ENTAO
         ESCREVA("Eixo X")
      FIMSE
      SE (Y > 0) E (X = 0) ENTAO
         ESCREVA("Eixo Y")
      FIMSE
      
      SE (X = 0) E (Y = 0) ENTAO
               ESCREVA("O ponto está na origem")
            FIMSE
      
      SE (x > 0) E (y > 0) ENTAO // Q1
         ESCREVA("Q1")
      FIMSE
      SE (x < 0) E (y > 0) ENTAO // Q2
         ESCREVA("Q2")
      FIMSE
      SE (x < 0) E (y < 0) ENTAO // Q2
         ESCREVA("Q3")
      FIMSE
      SE (x > 0) E (y < 0) ENTAO // Q2
         ESCREVA("Q4")
      FIMSE

Fimalgoritmo