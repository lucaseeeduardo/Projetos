Algoritmo "Ex. 4 - Medias escolares"

Var

n1, n2, n3, n4, media, exame, mediaexame: REAL

Inicio
      ESCREVA("Digite sua nota 1: ")
      LEIA(n1)
      ESCREVA("Digite sua nota 2: ")
      LEIA(n2)
      ESCREVA("Digite sua nota 3: ")
      LEIA(n3)
      ESCREVA("Digite sua nota 4: ")
      LEIA(n4)
      media <- (n1+n2+n3+n4)/4
      SE (media > 30) OU (media <0) ENTAO
         ESCREVA("Voc� digitou alguma nota errada, verifique e tente novamente")
      FIMSE
      SE media > 7 ENTAO
         ESCREVA("Parab�ns, aprovado!")
      SENAO
         ESCREVAL("Como sua m�dia foi", media, ", que � menor que 7, voc� foi para o exame")
         ESCREVA("Digite sua nota do exame: ")
         LEIA(exame)
         mediaexame <- (exame+media)/2
         SE (mediaexame >= 5) ENTAO
            ESCREVA("Parab�ns, voc� foi aprovado no exame.")
         SENAO
            ESCREVA("Infelizmente voc� n�o foi aprovado.")
         FIMSE
      FIMSE
      
Fimalgoritmo