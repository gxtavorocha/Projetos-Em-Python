from random import randint # Importa a funcao radint(escolhe numeros aleatorios) da biblioteca random
from time import sleep # Importa a funcao(sleep que faz com que o computador durma e congele) da biblioteca time
computador = randint(0,5) # Faz o computador "PENSAR"
print("-=-" * 20)
print('Vou pensar em um numero entre 0 e 5. Tente Adivinhar...')
print('-=-' * 20)
jogador = int(input('Em que numero pensei?'))
print('PROCESSANDO.......')
sleep(3)  # faz com que o computador durma e congele a resposta durante 3 segundos
if jogador == computador:
    print('PARABENS! Voce Conseguiu me vencer!')
else:
    print('GANHEI! eu pensei no numero {} e nao no numero {}'.format(computador, jogador))
