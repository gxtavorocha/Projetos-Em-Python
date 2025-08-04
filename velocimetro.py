from rich import print

velocidade = float(input("Qual a velocidade do carro?"))
multa = (velocidade - 80 )* 7

if velocidade > 80:
    print("[red]VOCE FOI MULTADO!! EM R${:.2f} [/red]".format(multa))
else:
    print('[green]BOA VIAGEM!!!!![/green]')


