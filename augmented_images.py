import numpy as np
from PIL import Image

def carregar_imagem(caminho_imagem):
  # O Pillow abre a imagem e converte para uma matriz númerica
  img_original = Image.open(caminho_imagem).convert("RGB")
  matriz = np.array(img_original, dtype=float)
  altura, largura, _ = matriz.shape
  print("Iniciando Data Augmentation...")
  return matriz

#SEM NUMPY
# CORREÇÃO GAMMA
# altura = len(matriz_imagem)
# largura = len(matriz_imagem[0])
#
# nova_matriz = []
#
# for y in range(altura):
#   nova_linha = []
#   for x in range(largura):
#     pixel = matriz_imagem[y][x]
#     novo_pixel = []
#
#     for canal in pixel:
#       canal_norm = (canal / 255.0) + 1e-5
#       canal_gamma = math.pow(canal_norm, gamma)
#       valor_novo = canal_gamma * 255.0
#       if valor_novo > 255.0:
#         valor_novo = 255.0
#       elif valor_novo < 0.0:
#         valor_novo = 0.0
#       novo_pixel.append(int(valor_novo))
#     nova_linha.append(novo_pixel)
#   nova_matriz.append(nova_linha)

# ESPELHAMENTO
# altura = len(matriz_imagem)
# largura = len(matriz_imagem[0])
#
# matriz_resultado = []
#
# for y in range(altura):
#   linha_original = matriz_imagem[y]
#   linha_invertida = []
#
#   # Percorrer a linha atual de trás para a frente (da direita para a esquerda)
#   for x in range(largura - 1, -1, -1):
#     linha_invertida.append(linha_original[x])
#
#   matriz_resultado.append(linha_invertida)

# BRILHO
#   altura = len(matriz_imagem)
#   largura = len(matriz_imagem[0])
#
#   nova_matriz = []
#
#   for y in range(altura):
#     nova_linha = []
#     for x in range(largura):
#       pixel = matriz_imagem[y][x]
#       novo_pixel = []
#       for canal in pixel:
#         valor_novo = canal + beta
#         if valor_novo > 255:
#           valor_novo = 255
#         elif valor_novo < 0:
#           valor_novo = 0
#
#         novo_pixel.append(valor_novo)
#       nova_linha.append(novo_pixel)
#     nova_matriz.append(nova_linha)

# ZOOM OUT
# altura = len(matriz_imagem)
# largura = len(matriz_imagem[0])
#
# nova_matriz = []
#
# for y in range(0, altura, fator):
#   nova_linha = []
#
#   for x in range(0, largura, fator):
#     nova_linha.append(matriz_imagem[y][x])
#
#   nova_matriz.append(nova_linha)

def espelhar_imagem(matriz, tipo):
  if tipo == "horizontal":
    # Uso o flip do numpy para inverter as colunas da matriz (esquerda vira direita)
    matriz_modificada = np.fliplr(matriz)
  elif tipo == "vertical":
    # Mesma lógica acima só que dessa vez inverto as linhas
    matriz_modificada = np.flipud(matriz)
  else:
    print("Tipo inválido! Escolha 'horizontal' ou 'vertical'.")
    return

  # Clip para assegurar valores e depois mostra a imagem
  print(f"Espelhamento {tipo} foi concluído...")
  img_final = Image.fromarray(
      np.clip(matriz_modificada, 0, 255).astype(np.uint8)
  ).save("Mirroring.png")

def rotacao_90(matriz, k):
  # k=-1 para horário e 1 para anti-horário
  matriz_rot_anti = np.rot90(matriz, k)
  # Mais uma vez, converter e mostrar
  print("Rotação simples de 90º concluída...")
  Image.fromarray(
      np.clip(matriz_rot_anti, 0, 255).astype(np.uint8)
  ).save("90_rotation.png")

def rotacao_arbitraria(matriz_original, angulo_graus):
   altura, largura, canais = matriz_original.shape

   # Converter o ângulo para radianos
   rad = np.radians(angulo_graus)
   cos_t = np.cos(rad)
   sin_t = np.sin(rad)
   # Centro da imagem original
   cx, cy = largura / 2.0, altura / 2.0

   # Criar uma matriz de destino vazia com o mesmo tamanho
   matriz_destino = np.zeros((altura, largura, canais), dtype=float)

   # Mapeamento inverso: percorrer cada píxel da imagem NOVA (destino)
   for y_novo in range(altura):
     for x_novo in range(largura):
       # Transladar para a origem (centro), rodar no sentido inverso e transladar de volta
       x_trans = x_novo - cx
       y_trans = y_novo - cy

       # Fórmulas de rotação inversa com seno e cosseno
       x_origem = int(x_trans * cos_t + y_trans * sin_t + cx)
       y_origem = int(-x_trans * sin_t + y_trans * cos_t + cy)

       # Verificar se o píxel calculado cai dentro dos limites da imagem original
       if 0 <= x_origem < largura and 0 <= y_origem < altura:
         matriz_destino[y_novo, x_novo] = matriz_original[y_origem, x_origem]
   print(f"Rotação concluída em {angulo_graus}º...")
   Image.fromarray(
     np.clip(matriz_destino, 0, 255).astype(np.uint8)
   ).save("free_rotation.png")

def correcao_gama(matriz, gamma):
  if gamma <= 0:
    print("Modificação no valor de gamma, não é possível ser um valor menor que 0")
    gamma = 0.01
  # Normalizar para [0, 1], e converto para uma escala decimal entre 0.0 e 1.0
  matriz_norm = matriz / 255.0
  print(f"Matriz normalizada. Iniciando correção em {gamma} Gamma...")
  # Percorro a matriz elevando os elementos (píxeis) na potência de gamma
  # Como a matriz está normalizada, o preto continua preto e o branco continua branco
  matriz_gamma = np.power(matriz_norm, gamma) * 255.0

  # Mesmo com tudo normalizado faço o clip para garantir e mostro a imagem
  Image.fromarray(
      np.clip(matriz_gamma, 0, 255).astype(np.uint8)
  ).save("gamma.png")

def ajuste_de_brilho(matriz):
  beta = np.random.randint(10, 31) #Gera o valor aleatório

  # Brighter
  matriz_brilho = matriz + beta
  # Aqui o clip é importante, pois o beta pode extrapolar a matriz
  print(f"Apresentando a imagem com aumento de brilho, sendo Beta: {beta}")
  Image.fromarray(
      np.clip(matriz_brilho, 0, 255).astype(np.uint8)
  ).save("brighter.png")

  input("Pressione ENTER para continuar...")

  # Darker
  matriz_escuro = matriz - beta
  print(f"Apresentando a imagem com diminuição de brilho, sendo Beta: {beta}")
  Image.fromarray(
      np.clip(matriz_escuro, 0, 255).astype(np.uint8)
  ).save("darker.png")

def aplicar_zoom_out(matriz, fator):
  # Array Slicing (step) / Stride
  matriz_zoom_out = matriz[::fator, ::fator, :]
  print(f"Zoom out aplicado com foco de: {fator}")
  # Clip para não extrapolar
  Image.fromarray(
      np.clip(matriz_zoom_out, 0, 255).astype(np.uint8)
  ).save("zoom_out.png")

def aplicar_zoom_in(matriz, fator):
  # Repetição do eixo da linha (altura)
  matriz_zoom_in = np.repeat(matriz, fator, axis=0)
  # Repetição do eixo da coluna (largura)
  matriz_zoom_in = np.repeat(matriz_zoom_in, fator, axis=1)
  print(f"Zoom in aplicado com foco de: {fator}")
  # Clip para não extrapolar
  Image.fromarray(
      np.clip(matriz_zoom_in, 0, 255).astype(np.uint8)
  ).save("zoom_in.png")

def crop_central(matriz, fator_corte):
  altura, largura, _ = matriz.shape

  # Faço um Floor Division para tirar um corte fino do centro da imagem (baseado na altura e largura)
  h_margem = altura // (fator_corte * 2)  # Corte vertical
  w_margem = largura // (fator_corte * 2)  # Corte horizontal

  # Fatia para pegar só o miolo
  matriz_recortada = matriz[
      h_margem : altura - h_margem, w_margem : largura - w_margem
  ]

  print(f"Zoom In por Crop com foco de: {fator_corte}.")
  img_final = Image.fromarray(
      np.clip(matriz_recortada, 0, 255).astype(np.uint8)
  )
  img_final.save("zoom_crop_central.jpg")

if __name__ == "__main__":
    matriz = carregar_imagem("Wallpaper/0.jpg")

    #Usar horizontal ou vertical
    espelhar_imagem(matriz, "horizontal")

    # 1 anti-horário e -1 horário
    rotacao_90(matriz, 1)

    #Não deu para testar todos os ângulos
    rotacao_arbitraria(matriz, 45)

    #gamma > 1 = escuro; gamma < 1 = claro; E gamma > 0
    correcao_gama(matriz, gamma=-5)

    #beta deve estar entre 10 <= beta <= 30
    ajuste_de_brilho(matriz)

    #fator é o tanto de zoom aplicado
    aplicar_zoom_out(matriz, fator=5)
    aplicar_zoom_in(matriz, fator=5)
    crop_central(matriz, fator_corte=5)