def notas(*args, sit=False):
    relatorio = dict()
    soma = 0

    relatorio['total'] = len(args)
    soma = sum(args)
    relatorio['maior'] = max(args)
    relatorio['menor'] = min(args)
    relatorio['média'] = soma/len(args)
    if sit:
        if relatorio['média'] >= 7:
            relatorio['situação'] = 'BOA'
        else:
            relatorio['situação'] = 'RUIM'
    return relatorio


resp = notas(9.9, 9.09, 6, 3, sit=True)
print(resp)
