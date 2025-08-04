from rich import print
salario = float(input('Qual o salario do funcionario? R$'))
n = salario / 0.85
b = salario / 0.80
if salario<1.250:
   print('---Novo salario sera R$[blue]{:.2f}[/blue]---'.format(n))
else:
   print("---Novo salario sera R$[blue]{:.2f}[/blue]---".format(b))