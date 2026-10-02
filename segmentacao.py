import numpy as np
from PIL import Image

def segmentar_mm(caminho_imagem, cor_usuario):
  # O Pillow abre a imagem e converte para uma matriz númerica
  img_original = Image.open(caminho_imagem).convert("RGB")
  matriz = np.array(img_original, dtype=float)
  altura, largura, _ = matriz.shape

  # Aqui é criado uma matriz cheia de zeros (para representar uma imagem de cor preta)
  # com as mesmas dimensões da imagem trabalhada atualmente.
  matriz_preta = np.zeros((altura, largura, 3), dtype=float)

  # Extrair os canais individualmente para facilitar as regras de cor
  r = matriz[:, :, 0]
  g = matriz[:, :, 1]
  b = matriz[:, :, 2]

  # Níveis de tons dá matiz
  # Durante os testes identifiquei alguns vazamentos, fiz uma pesquisa para tentar
  # contornar o problema, mas não cheguei nem próximo de um resultado perfeito
  match cor_usuario:
    case "vermelho":
      mascara = (r > 130) & (r < 255) & (g < 60) & (b < 60)
    case "laranja":
      mascara = (r > 150) & (g > 60) & (g < 140) & (b < 50)
    case "amarelo":
      mascara = (r > 150) & (g > 150) & (b < 80) & (abs(r - g) < 50)
    case "verde":
      mascara = (g > r) & (g > b) & (g > 100)
    case "azul":
      mascara = (b > r) & (b > g)
    case "marrom":
      mascara = (r > 80) & (r < 160) & (g > 40) & (g < 110) & (b < 80)
    case _:
      print("Digite uma cor de M&M válida.")
      return

  # Indexação Booleana / Masking
  matriz_preta[mascara] = matriz[mascara]

  # Sem a técnica de Masking (exemplo do vermelho)
  # for i in range(altura):
  #   for j in range(largura):
  #     if r > 150 and g < 100 and b < 100:
  #       resultado[i][j] = matriz[i][j] # Copia o pixel
  #     else:
  #       resultado[i][j] = 0 # Fica preto

  # Faz o clip (só por garantia) e converte
  resultado_ajustado = np.clip(matriz_preta, 0, 255).astype(np.uint8)
  # Como é simples agora, mostra a imagem com o próprio Pillow mesmo
  Image.fromarray(resultado_ajustado).show()

if __name__ == "__main__":
  print("\n--- SEGMENTATION ---")

  while True:
    print("Cores disponíveis: Laranja, Vermelho, Amarelo, Verde, Azul, Marrom")

    entrada = input("Digite a cor que deseja segmentar (ou digite 'n' para encerrar): ").strip()

    if entrada.lower() == "n":
      print("Segmentação encerrada com sucesso!")
      break

    # Guarda a cor escolhida
    cor_usuario = entrada
    caminho = "MMs.jpg"  # Certifique-se de que o nome do arquivo está correto (maiúsculas/minúsculas)

    # Chama a função passando a escolha recolhida
    segmentar_mm(caminho, cor_usuario)

  # Problemas de vazamento
  # Amarelo: tranquilo
  # Azul: vaza muito branco
  # Laranja: bastante amarelo, se "subir" demais não cobre a cor.
  # Marrom: um pouco de amarelo e quase não cobre a cor por completo, somente onde "desce" para o amarelo
  # Verde: um pouco de amarelo
  # Vermelho: muito laranja e não cobre a cor por completo vermelho se "descer" demais