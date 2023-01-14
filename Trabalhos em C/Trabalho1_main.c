#include <stdio.h>
#include <stdlib.h>
#include <locale.h>

int main(int argc, char *argv[]) {
	setlocale(LC_ALL, "Portuguese");
	
	int ano, algano, alganodiv4, mes, meschave, seculochave, dia, soma;
	
	printf("Olá, seja bem-vindo ao analisador de dias da semana!\n");
	
	printf("Digite o ano [de 1800 a 2199]: ");
	scanf("%i", &ano);
	
	if ((1800 <= ano) && (ano <= 2199))
	{
		if ((ano>=1800) && (ano<=1899))// task (4)
		{
			seculochave = 2;
		}
		if ((ano>=1900) && (ano<=1999))
		{
			seculochave = 0;
		}
		if ((ano>=2000) && (ano<=2099))
		{
			seculochave = 6;
		}
		if ((ano>=2100) && (ano<=2199))
		{
			seculochave = 4;
		}
		if ((ano<1800) || (ano>2199))
		{
			printf("Somente anos entre 1800 e 2199!");
		}
		
		int algano = ano%100; // task (1)
		int alganodiv4 = algano/4; // task(2)
	
	//  printf("%i, %i", algano, alganodiv4);  validação de algano e alganodiv4
	// mês abaixo
		
		printf("Digite o número do mês[1 a 12]: ");
		scanf("%i", &mes);
		
		
		if ((mes >= 1) && (mes<=12)) 
		{
			printf("Digite o dia[1 a 31 dependendo do mês em questão]: ");
			scanf("%i", &dia); // task (5)
			
			if ((dia>=1) && (dia<=31))
			{
				if (dia%30 == 1) // aqui eu faço a diferenciação de dias que vão até 30 e 31
				{
					switch (mes) // meschave task (3)
					{ 
						case 1: // janeiro e janeiro bi
							if (((ano)%400 == 0) || ((ano%4 == 0) && (ano%100 != 0)))
							{
							//printf("Esse ano é bissexto."); validação do ano bissexto
								meschave = 0;
							}
							else 
							{
							//	printf("Esse ano não é bissexto."); validação do ano bissexto
								meschave = 1;
							}					
							break;
						case 3:	//março
							meschave = 4;
							break;
						case 5: // maio
							meschave = 2;
							break;
						case 7: // julho
							meschave = 0;
							break;
						case 8: // agosto
							meschave = 3;
							break;
						case 10: // outubro
							meschave = 1;
							break;
						case 12: // dezembro
							meschave = 6;
							break;
					}
				}	
				else // esse else é para meses que não vão até o dia 31, essa analogia me permite poupar trabalho ao fazer a condição, pois, se eu coloco o if com dias que vão somente até 30, tenho que considerar que fevereiro não vai até 30.
				{
					switch (mes)
					{
						case 2: // fevereiro e fevereiro bi
							if (((ano)%400 == 0) || (((ano%4 == 0) && (ano%100 != 0))))
							{
							//	printf("Esse ano é bissexto."); validação do ano bissexto
								meschave = 3;
							//	printf("%i validação do meschave\n", meschave);
							}							
							else 
							{
								printf("Esse ano não é bissexto."); //validação do ano bissexto
								meschave = 4;	
							}
							break;
						case 4: // abril
							meschave = 0;
							break;
						case 6: // junho
							meschave = 5;
							break;
						case 9: // setembro
							meschave = 6;
							break;
						case 11: // novembro
							meschave = 4;
							break;	
					}
				}	
			}	
			else
			{
				printf("O dia precisa estar entre 1 e 31, dependendo do mês. Você digitou %i", dia);				
			}
		}
		else
		{
			printf("O mês precisa estar entre 1 e 12, você digitou %i.", mes);			
		}
		
		//printf("%i esta é a validação da task 1\n", algano); // validação task 1
		//printf("%i esta é a validação da task 2\n", alganodiv4); // validação task 2
		//printf("%i esta é a validação da task 3\n", meschave); // validação task 3
		//printf("%i esta é a validação da task 4\n", seculochave); // validação task 4
		//printf("%i esta é a validação da task 5\n", dia);
		//printf("%i esta é a validação da soma (task6)\n", (algano+alganodiv4+meschave+seculochave+dia));
		
		soma = ((algano + alganodiv4 + meschave + seculochave + dia)%7);
		
		//printf("%i esta é a validação da task 7\n", soma); // validação da soma 

		switch (soma)
		{
			case 0:
				printf("O dia da semana de %i do mês %i de %i é Sábado!", dia, mes, ano);
				break;
			case 1:
				printf("O dia da semana de %i do mês %i de %i é  Domingo!", dia, mes, ano);
				break;
			case 2:
				printf("O dia da semana de %i do mês %i de %i é  Segunda-feira!", dia, mes, ano);
				break;
			case 3:
				printf("O dia da semana de %i do mês %i de %i é  Terça-feira!", dia, mes, ano);
				break;
			case 4:
				printf("O dia da semana de %i do mês %i de %i é  Quarta-feira!", dia, mes, ano);
				break;
			case 5:
				printf("O dia da semana de %i do mês %i de %i é  Quinta-feira!", dia, mes, ano);
				break;
			case 6:
				printf("O dia da semana de %i do mês %i de %i é  Sexta-feira!", dia, mes, ano);
				break;
			default:
				printf("Programa com erro.");
		}
	}
	else 
	{
		printf("O ano precisa estar entre 1800 e 2199, você digitou %i.", ano);		
	}
	return 0;
}
