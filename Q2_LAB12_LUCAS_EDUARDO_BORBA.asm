.data 
	prompt: .asciiz "Entre uma string: "
	output: .asciiz "\nVoc� digitou a string: "
	input: .space 81 #endereco com "81 espa�os livres"
 	inputSize: .word 80 #guarda o numero 80 na memoria
 .text
 	la $a0, prompt # aqui estou alocando em $a0 o endere�o da label que cont�m a string de entrada
 	li $v0, 4 # aqui estou printando o conte�do do endere�o lido em $a0
 	syscall
 	
 	la $a0, input # como o conte�do do registrador $a0 � o endere�o de mem�ria onde quero armazenar o conte�do lido, coloquei o endere�o da label "input" em $a0. 
	la $a1, inputSize # em $a1 deve estar o tamanho da string, ent�o aloquei o endere�o da label que cont�m o n�mero do tamanho
	li $v0, 8 # aqui � o comando em v0 para ler uma string
	syscall
 	
 	la $a0, output # aqui estou alocando em $a0 o endere�o da label output
 	li $v0, 4 # aqui estou printando o conte�do do endere�o de mem�ria da label output 
 	syscall
 	
 	la $a0, input # aqui estou colocando em $a0 o endere�o da label "input". 
 	li $v0, 4 # aqui estou pedindo para v0 ler o que est� no endere�o da label "input"
 	syscall
