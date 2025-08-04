from rich import print

distancia = float(input('Digite a distancia de sua viagem:'))
calculokm = (distancia * 0.5)
calculol = (distancia * 0.45)
if distancia <= 200:
    print("O valor de sua viagem é [green]R$ {:.2f}[/green] ".format(calculokm))
else:
    print("O valor de sua viagem é [green]R$ {:.2f}[/green]".format(calculol))