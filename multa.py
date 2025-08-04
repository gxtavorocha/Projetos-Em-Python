# Verifica quantos km/h o veiculo esta !
velocidade = int(input("Quantos km/h voce esta ? "))

# Verifca se esta dentro do limite permitido , caso não esteja , ele calcula a multa e exibe na tela para o usuario , mas caso esteja do limite so exibe a mensagem boa viagem !
if velocidade > 80:
    excesso =  velocidade - 80
    multa = excesso * 7
    print("Voce excedeu a velocidade da via de 80 km/h permitido, excesso de: {:.2f} km/h.".format(excesso))
    print('O valor da multa foi no valor de R$ {:.2f}'.format(multa))

else:   
    print('Seu carro esta dentro do limite de velocidade , Boa Viagem!')