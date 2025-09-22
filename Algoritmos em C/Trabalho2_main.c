#include <stdio.h>
#include <stdlib.h>

/* run this program using the console pauser or add your own getch, system("pause") or input loop */

int main(int argc, char *argv[]) {
	int a, b, mmc, n, m, cont, mdc;
	char resposta = 'S';
	
	while (resposta == 'S')
	{
		printf("Digite um numero: ");
		scanf("%i", &a);
		while (a < 0)
		{
			printf("Digite um numero maior que zero: ");
			scanf("%i", &a);
		}
		
		printf("Digite outro numero: ");
		scanf("%i", &b);
		while (b < 0)
		{
			printf("Digite um numero maior que zero: ");
			scanf("%i", &b);
		}
		mdc = 1;
		mmc = 1;
		n = a;
		m = b; 
		cont = 2;
		
		while (1)
		{
			while ( n % cont == 0 || m % cont == 0 ) 
			{
				if ( n == 1 && m == 1 )
				{
					break;
				}
				
				mmc = mmc * cont;
				if ( n % cont == 0 && m % cont == 0)
				{
					mdc = mdc * cont;
				}
				if(n % cont != 0) // a
				{
					n = n;
				}
				else
				{
					n = n / cont;
				}
				
				if(m % cont != 0) // b
				{
					m = m;
				}
				else
				{
					m = m / cont;
				}
			}
			cont = cont + 1;
			
			if (mmc % a == 0 && mmc % b == 0)
			{
				break;
			}
		}
		
		printf("O mmc eh: %i\n", mmc);
		printf("o mdc eh: %i\n", mdc);
		printf("Voce deseja avaliar outro conjunto de numeros?[S/N]");
		scanf("%s", &resposta);
	}
	return 0;
}
