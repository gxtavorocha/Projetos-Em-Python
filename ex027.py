n = str(input("Digite seu nome completo: ")).strip()
nome = n.split()
print("O Primeiro Nome e {}".format(nome[0]))
print("O Ultimo nome e {}".format(nome[len(nome)-1]))