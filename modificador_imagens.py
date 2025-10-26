from PIL import Image
import matplotlib.pyplot as plt

def carregar_imagem_binaria(caminho):
    img = Image.open(caminho).convert("L") 
    largura, altura = img.size
    matriz = []
    for y in range(altura):
        linha = []
        for x in range(largura):
            pixel = img.getpixel((x, y))
            linha.append(1 if pixel < 128 else 0)  
        matriz.append(linha)
    return matriz, largura, altura

def criar_matriz(linhas, colunas, valor=0):
    return [[valor for _ in range(colunas)] for _ in range(linhas)]

def refletir_elemento_estruturante(B):
    linhas = len(B)
    colunas = len(B[0])
    refletido = criar_matriz(linhas, colunas)
    for i in range(linhas):
        for j in range(colunas):
            refletido[i][j] = B[linhas - 1 - i][colunas - 1 - j]
    return refletido

def erosao(A, B):
    linhas_A, colunas_A = len(A), len(A[0])
    linhas_B, colunas_B = len(B), len(B[0])
    offset_l, offset_c = linhas_B // 2, colunas_B // 2

    resultado = criar_matriz(linhas_A, colunas_A, 0)

    for i in range(offset_l, linhas_A - offset_l):
        for j in range(offset_c, colunas_A - offset_c):
            corresponde = True
            for m in range(linhas_B):
                for n in range(colunas_B):
                    if B[m][n] == 1 and A[i + m - offset_l][j + n - offset_c] != 1:
                        corresponde = False
                        break
                if not corresponde:
                    break
            resultado[i][j] = 1 if corresponde else 0
    return resultado


def dilatacao(A, B):
    linhas_A, colunas_A = len(A), len(A[0])
    linhas_B, colunas_B = len(B), len(B[0])
    offset_l, offset_c = linhas_B // 2, colunas_B // 2
    B_refletido = refletir_elemento_estruturante(B)

    resultado = criar_matriz(linhas_A, colunas_A, 0)

    for i in range(offset_l, linhas_A - offset_l):
        for j in range(offset_c, colunas_A - offset_c):
            encontrou = False
            for m in range(linhas_B):
                for n in range(colunas_B):
                    if B_refletido[m][n] == 1 and A[i + m - offset_l][j + n - offset_c] == 1:
                        encontrou = True
                        break
                if encontrou:
                    break
            resultado[i][j] = 1 if encontrou else 0
    return resultado


def mostrar_resultados(erodida, dilatada):
    imagens = []
    titulos = ["Erosão", "Dilatação"]
    for matriz in [erodida, dilatada]:
        altura = len(matriz)
        largura = len(matriz[0])
        img = Image.new("L", (largura, altura))
        for y in range(altura):
            for x in range(largura):
                valor = 0 if matriz[y][x] == 1 else 255
                img.putpixel((x, y), valor)
        imagens.append(img)

    plt.figure(figsize=(12, 4))
    for i, (img, titulo) in enumerate(zip(imagens, titulos)):
        plt.subplot(1, 3, i + 1)
        plt.imshow(img, cmap='gray')
        plt.title(titulo)
        plt.axis('off')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    entrada = "paisagem3.jpg"     

    A, largura, altura = carregar_imagem_binaria(entrada)

    B = [
        [1,1,1],
        [1,1,1],
        [1,1,1]
    ]

    erodida = erosao(A, B)
    dilatada = dilatacao(A, B)

    mostrar_resultados(erodida, dilatada)