# Lembre-se de alterar o caminho do arquivo, para o caminho completo da sua máquina!

arquivo = open(
    "C:/Users/Hobbb/OneDrive/Documentos/GitHub/trilha-python-dio/05 - Manipulação de arquivos/lorem.txt",
    "r",
)
print(arquivo.read())
arquivo.close()

arquivo = open("05 - Manipulação de arquivos/lorem.txt", "r")
print(arquivo.readline())
arquivo.close()

arquivo = open("05 - Manipulação de arquivos/lorem.txt", "r")
print(arquivo.readlines())
arquivo.close()

arquivo = open("05 - Manipulação de arquivos/lorem.txt", "r")
# tip
# Read and print each line until the end of the file
while len(linha := arquivo.readline()):
    print(linha)

arquivo.close()
