def exibir_coracao():
    coracao = [
         "   *     *   ",
        " *   * *   * ",
        "*     *     *",
        "*           *",
        " *         * ",
        "   *     *   ",
        "     * *     ",
        "      *      "
        
    ]

    for linha in coracao:
       print(linha)
# Solicita nome do usuario
nome = input('Digite Seu Nome: ')

#verifica se o nome e sara

if nome == "sara" : 
    exibir_coracao()

else:
    print(f'Ola!, {nome}')


   
