from rich import print 
n = int(input('Qual o número que voce esta pensando?'))
resultado = n % 2
if resultado == 0:
    print('O numero {} é [cyan]PAR[/cyan]'.format(n))
else:
    print('O numero {} e [cyan]IMPAR[/cyan]'.format(n))




 
