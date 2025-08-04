frase = str(input('Digite uma frase: ')).upper().strip()
print('A letra A aparece {} na frase.'.format(frase.count("A")))
print("A letra a foi encontrada na primeira posicao {}".format(frase.find("A")+1))
print('A ultima posicao foi encontrada na {}'.format(frase.rfind('A')+1))