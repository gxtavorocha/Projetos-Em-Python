d = int(input('Quantos Dias Foi Alugado o veiculo ?  '))
k = float(input('Quantos Km Rodados ?  '))
c = (d * 60) + (k * 0.15)
print( "Total a pagar é de R$ {:.2f}".format(c))