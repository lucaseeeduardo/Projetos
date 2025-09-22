# Desafio 024 - Informar uma cidade e saber se ela contém a palavra "SANTO"

city = str(input('Digite o nome de uma cidade: ')).strip()

print('A cidade de {} possui SANTO no nome? {}'.format(city, 'SANTO' in city.upper()))
# ou

cid = str(input('Digite o nome de uma cidade: ')).strip()

print('A cidade possui "SANTO"?: {}'.format(cid[:5].upper() == 'SANTO'))
