import time
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def iniciar_janela_exibicao():
    print("Configurando janela exibiço...")
    # Configuração do Matplotlib #Gemini
    plt.ion()
    fig, ax = plt.subplots()
    return fig, ax

def fechar_janela_exibicao():
    # Configuração do Matplotlib #Gemini
    plt.ioff()
    plt.show()

def fade_in_out(caminho_imagem):
    print("--- FADE IN/OUT ---")
    fig, ax = iniciar_janela_exibicao()

    # O Pillow é usado apenas para abrir a imagem (arquivo)
    # e para converter a imagem para um formato RGB.
    img_original = Image.open(caminho_imagem).convert("RGB")

    # Converte a imagem para uma matriz de float
    # para fazer contas matemáticas sem perder precisão.
    matriz = np.array(img_original, dtype=float)

    # Altura (h), a largura (w) e os canais de cores da imagem.
    altura, largura, _ = matriz.shape

    # Aqui é criado uma matriz cheia de zeros (para representar uma imagem de cor preta)
    # com as mesmas dimensões da imagem trabalhada atualmente.
    matriz_preta = np.zeros((altura, largura, 3), dtype=float)

    print("Iniciando efeito de fade-in/fade-out...")
    start = 1
    stop = 0
    for i in range(3):
        print(f"Volta: {i}")
        for alpha in np.linspace(start, stop, 50):
            # R' = R1 * (1 - alpha) + R2 * alpha
            # Como a imagem 2 (matriz_preto) é toda zero, a parte do R2 é anulada,
            resultado = matriz * (1 - alpha) + matriz_preta * alpha

            # Limitar valores para 0 e 255 (formato que o computador entende para pixels: uint8).
            resultado_ajustado = np.clip(resultado, 0, 255).astype(np.uint8)

            # Limpa e redesenha (comando do Plot)
            ax.clear()
            ax.imshow(resultado_ajustado)
            ax.axis("off")
            plt.pause(0.01)
        start, stop = stop, start

    fechar_janela_exibicao()
    print("Efeito fade-in/fade-out finalizado com sucesso!...")

def cross_fade(caminho_imagem_1, caminho_imagem_2):
    print("--- CROSS FADE ---")
    fig, ax = iniciar_janela_exibicao()
    # Novamente com o Pillow uso só para carregar as imagens
    img1 = Image.open(caminho_imagem_1).convert("RGB")
    img2 = Image.open(caminho_imagem_2).convert("RGB")
    img2 = img2.resize(img1.size)

    # Mesma conversão com o numpy
    imagem_1 = np.array(img1, dtype=float)
    imagem_2 = np.array(img2, dtype=float)

    print("Iniciando efeito de sobreposição...")
    img_a = imagem_1
    img_b = imagem_2
    for i in range(3):
        for alpha in np.linspace(1.0, 0.0, 50):
            # R' = R1 * (1 - alpha) + R2 * alpha
            # G' = G1 * (1 - alpha) + G2 * alpha
            # B' = B1 * (1 - alpha) + B2 * alpha

            # r = img_a[:, :, 0] * alpha + img_b[:, :, 0] * (1 - alpha)
            # g = img_a[:, :, 1] * alpha + img_b[:, :, 1] * (1 - alpha)
            # b = img_a[:, :, 2] * alpha + img_b[:, :, 2] * (1 - alpha)
            # resultado = np.stack([r, g, b], axis=-1)

            # Multiplicação de matriz com numpy
            resultado = img_a * alpha + img_b * (1 - alpha)

            # Novamente é limitado os valores para 0 e 255 (além de dar cast para uint8).
            resultado_ajustado = np.clip(resultado, 0, 255).astype(np.uint8)

            # Limpa e redesenha (comando do Plot)
            ax.clear()
            ax.imshow(resultado_ajustado)
            ax.axis("off")
            plt.pause(0.01)
        img_a, img_b = img_b, img_a

    print("Efeito de sobreposição finalizado com sucesso...")
    fechar_janela_exibicao()

if __name__ == "__main__":
    match int(input("Digite 1 para Fade In/Out; 2 para Cross Fade; 3 para sair")):
        case 1: fade_in_out("Wallpaper/0.jpg")
        case 2: cross_fade("Wallpaper/0.jpg", "Wallpaper/5.jpg")
        case _: print("Fechando...")