#! python3
from PIL import Image, ImageDraw, ImageColor
import sys

tamanho = (100, 100)

def ajustar_imagem(arquivo):
	img = Image.open(arquivo)
	largura, altura = img.size
	multi = tamanho[0] / largura		# proporcao com base na largura (pra alcancar o tamanho)
	if altura*multi > tamanho[1]:		# se a altura passar do tamanho
		multi = tamanho[1] / altura		# proporcao com base na altura
	nova_largura = int(largura*multi)
	nova_altura  = int(altura*multi)
	nova_img = img.resize((nova_largura, nova_altura), Image.LANCZOS)

	news = [(255,0,0) for _ in range(50)]

	nova_img.putdata(news)

	nova_img.save('image_500.jpg')

# 1500*x = 100
# 100 / 1500 = x


def testo():
	arquivo = 'fonte2.jpg'	# testo
	im = Image.open(arquivo)

	imgs = Image.Image.split(im)	# red green blue
	nova_img = [Image.new("RGB",im.size) for _ in range(3)]

	for i in range(3):
		pixels = imgs[i].getdata()
		nova = []
		for p in pixels:
			# print(p)
			cor = [0,0,0]
			if p > 255/2:
				cor[i] = 255
			cor = tuple(cor)
			nova.append(cor)
		nova_img[i].putdata(nova)
		nova_img[i].show()





	# imgs[0]
	# for i in imgs:
	# 	i.show()


	# Image.convert(mode=None, matrix=None, dither=None, palette=0, colors=256)

	# out = im.convert('1', dither=Image.NONE)
	# pixels = out.getdata() # pixeis em linha, comecando do canto sup esq
	# for p in pixels:
	# 	print(p)


	# rgb2xyz = (
    # 0.412453, 0.357580, 0.180423, 0,
    # 0.212671, 0.715160, 0.072169, 0,
    # 0.019334, 0.119193, 0.950227, 0 )
	# out = im.convert("RGB", rgb2xyz)
	# out.save('falaMeuBom.jpg')

def main():
	# entrada = input()
	entrada = 'paulao_result.jpg'
	ajustar_imagem(entrada)

# main()
testo()
