from random import shuffle
n1 = str(input('Digite Um Nome: '))
n2 = str(input("Digite um Segundo nome : "))
n3 = str(input('Digite um Terceiro Nome: '))
n4 = str(input('Digite um Quarto nome : '))
lista_de_nomes = [n1,n2,n3,n4]
shuffle(lista_de_nomes)
print("A Ordem de apresentacao sera ")
str(print(lista_de_nomes))