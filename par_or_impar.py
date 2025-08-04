import math
# Pede para o usuario digitar um numero
numero = int(input('Digite um numero: '))

# realiza o calculo se for divisivel por 2 o resultado tem que ser igual a 0 nesse caso o numero sera impar,  % esse sinal é um módulo aritmético que retona o resto da divisão
if numero % 2 == 0:
    print('O numero e par')
else:
    print('O numero e ímpar')
