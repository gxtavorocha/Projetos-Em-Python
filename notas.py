n1 = float(input('Digite a Primeira Nota: '))
n2 = float(input('Digite a Segunda Nota: '))
notas = float((n1 + n2)/2)
print('Sua media Bimestral foi {:.1f}'.format(notas))
if notas >=6.0:
    print('PARABÉNS SUA NOTA FOI BOAA !! ')
else:
    print('ESTUDE MAIS, NOTA INSUFISCIENTE !!!!')