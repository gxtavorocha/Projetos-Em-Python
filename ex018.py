from random import choice
n1 = str(input('Digite Um Nome: '))
n2 = str(input("Digite um Segundo nome : "))
n3 = str(input('Digite um Terceiro Nome: '))
n4 = str(input('Digite um Quarto nome : '))
lista_de_nomes = [n1,n2,n3,n4]
escolhido = choice(lista_de_nomes)
print('O aluno escolhido para apagar o quadro foi {}'.format(escolhido))