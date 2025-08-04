#Desenvolva um programa que pergunta a distancia de uma viagem em km. Calcule o preco da passagem.cobrando R$ 0,50 por Km para viagens de ate 200km e R$ 0,45 para viagens mais longas.
km = float(input('Quantos Km voce ira percorrer para chegar ao seu destino ? '))
if km <= 200:
    calculo = (km * 0.50)
    print('O valor da sua viagem sera de {:.2f}'.format(calculo))

else:
    c = (km * 0.45)
    print('O valor da sua viagem sera de {:.2f}'.format(c))


    
