Algoritmo "Ex. 8 - Empresa XYZ"
 //nome do funcionário
 //% de aumento
 //salário atual
 // novo salário
Var

SALARIO, NOVOSALARIO, aumento: REAL
NOME :CARACTERE
Inicio
      ESCREVA("Digite o seu nome: ")
      LEIA(NOME)
      ESCREVA("Digite o seu salário atual: ")
      LEIA(SALARIO)

      SE (SALARIO <= 400) ENTAO
         NOVOSALARIO <- SALARIO*1.15
         aumento <- 15
      FIMSE

      SE (SALARIO > 400) E (SALARIO <=700) ENTAO
         NOVOSALARIO <- SALARIO*1.12
         aumento <- 12
      FIMSE

      SE (SALARIO > 700) E (SALARIO <=1000) ENTAO
         NOVOSALARIO <- SALARIO*1.10
         aumento <- 10
      FIMSE

      SE (SALARIO > 1000) E (SALARIO <=1800) ENTAO
         NOVOSALARIO <- SALARIO*1.07
         aumento <- 7
      FIMSE

      SE (SALARIO > 1800) E (SALARIO <=2500) ENTAO
         NOVOSALARIO <- SALARIO*1.04
         aumento <- 4
      FIMSE
      
      SE (SALARIO <= 2500) ENTAO
         ESCREVAL("Prezado ", NOME, ", seu salário teve aumento.")
         ESCREVAL("Você ganha", SALARIO," e passará a ganhar ", NOVOSALARIO)
         ESCREVAL("Isso significa um aumento de ", aumento, "%.")
      SENAO
         ESCREVA("Você não teve aumento de salário.")
      FIMSE
      
Fimalgoritmo