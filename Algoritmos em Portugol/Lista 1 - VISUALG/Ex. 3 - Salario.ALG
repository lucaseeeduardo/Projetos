Algoritmo "Exercício 2 - Tempo do piloto"

Var
NOME :CARACTERE
HT, VH, SALARIO : REAL


Inicio
      ESCREVA("Digite o nome do funcionário A: ")
      LEIA(NOME)
      ESCREVA("Digite quantas horas o funcionário trabalha de seg-sexta: ")
      LEIA(HT)
      ESCREVA("Digite o valor por hora: ")
      LEIA(VH)
      SALARIO <- HT*VH
      ESCREVA("O Funcionário A, ", NOME,", recebe ", SALARIO:4:2, " reais por dia")

Fimalgoritmo