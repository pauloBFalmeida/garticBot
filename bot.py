####################################################################################
#####                   PROGRAMADO POR: LEANDRO L. MONTANARI                   #####
#####            VÍDEO: https://www.youtube.com/watch?v=GaXMzzYd_Uw            #####
##### DESENHO: https://gartic.com.br/daianaa/desenho-livre/taylor-e-oliver-3-2 #####
####################################################################################

from PIL import Image
import pyautogui as pa
from time import sleep

# Escala 100% - Imagem Total = 509 x 419
# Escala 100% - Imagem até Paleta de Cores = 509 x 280

# Escala 150% - Imagem Total = 763 x 629
# Escala 150% - Imagem até Paleta de Cores = 763 x 421

escala = {
    100 : {
        'tons' : 100,
        'divisao' : 2.55,
        'canvasX' : 580,
        'canvasY' : 328,
        'lumiX' : 698,
        'lumiY' : 619,
        'paletaX' : 510,
        'paletaY' : 582,
        'foraX' : 460,
        'foraY' : 290
        },
    150 : {
        'tons' : 150,
        'divisao' : 1.7,
        'canvasX' : 377,
        'canvasY' : 340,
        'lumiX' : 554,
        'lumiY' : 778,
        'paletaX' : 272,
        'paletaY' : 728,
        'foraX' : 147,
        'foraY' : 271
        }
    }

escolha = 0
intervalo = 0.001 # Anterior: 0.01

while escolha != 100 and escolha != 150:
    escolha = int(input('Usar qual escala? Digite 100 para 100% ou 150 para 150%: '))

d = {}

lis1 = [a for a in range (0, escala[escolha]['tons'] + 1)]
lis2 = [b for b in range (escala[escolha]['tons'], -1, -1)]

for i in lis1:
    d[i] = lis2[i]

fonte = Image.open('fonte.png')
largura, altura = fonte.size

canvasX = escala[escolha]['canvasX']
canvasY = escala[escolha]['canvasY']

lumiX = escala[escolha]['lumiX']
lumiY = escala[escolha]['lumiY']

sleep(5)
atual = 1000

for x in range(largura):
    try:
        for y in range(altura):
            luminosidade = fonte.getpixel((x, y)) # Pega o valor RGB (somente luminosidade, no caso de P&B) do pixel atual (x, y)

            if luminosidade[0] != 255: # Se o pixel não for branco (255 = branco | 0 = preto)...
                convertido = int(luminosidade[0] / escala[escolha]['divisao']) # Pega o valor atual e divide pelo número de tons na escala escolhida
                invertido = d[convertido] # Inverte, pois a barra de tons do Gartic começa com branco (0) e termina no preto (100 ou 150 [escala])

                if luminosidade[0] != atual: # Se o pixel atual for diferente do anterior...
                    pa.click(escala[escolha]['paletaX'], escala[escolha]['paletaY'], button='left') # Clica na paleta
                    sleep(intervalo) # Intervalo
                    pa.click(lumiX, lumiY + invertido, button='left') # Escolha entre os 100/150 níveis de luminosidade da paleta
                    sleep(intervalo) # Intervalo

                pa.click(canvasX, canvasY) # Clica na tela para fazer o pixel
                sleep(intervalo) # Intervalo
                atual = luminosidade[0]

            canvasY += 1
        canvasX += 1
        canvasY -= altura

    except KeyboardInterrupt:
        break
        input('Processo finalizado. Presione <Enter> para sair... ')
