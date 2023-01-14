Algoritmo "Ex. 7 - Salário e imposto"

Var

SALARIO, SALARIOLIQUIDO, IR, INSS, SINDICATO: REAL
Inicio
      ESCREVA("Digite o seu salário bruto: ")
      LEIA(SALARIO)
      ESCREVAL("Salário Bruto      : R$", SALARIO)
      IR <- SALARIO*0.15
      ESCREVAL("(-)IR(15%)         : R$", IR)
      INSS <- SALARIO*0.11
      ESCREVAL("(-)INSS(11%)       : R$", INSS)
      SINDICATO <- SALARIO*0.03
      ESCREVAL("(-)Sidicato(3%)    : R$", SINDICATO)
      SALARIOLIQUIDO <- SALARIO - IR - INSS - SINDICATO
      ESCREVAL("Salário líquido    : R$", SALARIOLIQUIDO)
Fimalgoritmo