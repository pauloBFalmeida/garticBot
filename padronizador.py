#! python3
from PIL import Image, ImageDraw, ImageColor, ImagePalette, ImageEnhance, ImageFilter, ImageStat, ImageOps
import sys

tamanho = (200, 200)

def quebrar_cores(nome):
	# im = Image.open('passaro.jpg')	# teste
	# im = Image.open('asno4.jpg')	# teste
	# im = Image.open(nome)
	im = ajustar_imagem(nome)
	im_rgb = list(Image.Image.split(im))	# red green blue

	# red = im_rgb[0]		# teste extrai somente o vermelho pra mostras
	# print(red.getpixel((0,0)))
	# red = red.convert('RGB')
	# print(red.getpixel((0,0)))
	# saida = []
	# for p in red.getdata():
	# 	saida.append((p[0],0,0))
	# red.putdata(saida)
	# red.show()

	# pixel_valor = 100
	pixel_valor = 255//2
	blur_radio	= 3
	valor_media = 255 - 5	# n usado
	raio_remocao = 2

	data_rgb = []
	# coloco 0 nos pixeis coloridos, e 255 nos sem cor
	# crio uma imagem com a cor preta representando a sua respectiva cor
	for i in range(3):
		# im_rgb[i] = im_rgb[i].filter(ImageFilter.BoxBlur(radius=blur_radio))
		im_rgb[i] = Image.eval(im_rgb[i], (lambda x: 0 if x > (255-pixel_valor) else 255))	# se tiver cor 0, sem cor 255
		data_rgb.append(im_rgb[i].getdata())

	# for i in im_rgb:
		# i.show()
		# print(i.getpixel((0,0)))

	tamanho = len(data_rgb[0])
	# crio a parte preta vendo onde nenhuma das cores se encontram
	pixels_b = [255   for _ in range(tamanho)]
	encontro = [False for _ in range(tamanho)]	# para remover a mistura de mais de uma cor
	for i in range(tamanho):	# i de cada pixel
		soma = 0
		for data in data_rgb:	# passo pelo pixel i das 3 cores
			soma = soma + data[i]
		if 	 soma == 255*3:		# se nao tiver encontro entre as cores (255 = branco = pixel sem cor)
			pixels_b[i] = 0		# pixel preto
		elif soma < 255*2:		# pelo menos 2 cores se encontraram (0+0+255, 0+0+0)
			encontro[i] = True

	# crio uma imagem com a cor preta representando o preto
	im_b = Image.new("L",im_rgb[0].size)
	im_b.putdata(pixels_b)

	# for i in im_rgb:
	# 	i.show()

	# removo onde as cores se encontram (onde tem pixel preto em mais de uma imagem)
	# se tiver 0 em mais de uma das im, removo de ambas
	# removo a mistura de mais de uma cor
	nova_data_rgb = []
	for data in data_rgb:	# data de cada cor
		nova_data = []
		for i in range(tamanho):	# i de cada pixel
			pixel = data[i]
			if encontro[i]:
				pixel = 255	# removo o pixel caso de encontro
			nova_data.append(pixel)
		nova_data_rgb.append(nova_data)	# add a nova data pra nova imagem da cor

	for i in range(3):
		im_t = Image.new("L",im_rgb[0].size)
		im_t.putdata(nova_data_rgb[i])
		im_rgb[i] = im_t

	# calcula a media do valor dos pixels, e adiciona somente os com menos de valor_media
	# saida = [None for _ in range(4)]
	# ims = im_rgb + [im_b]
	# for i in range(4):
	# 	stat = ImageStat.Stat(ims[i])
	# 	if stat.mean[0] < valor_media:
	# 		saida[i] = ims[i]


	#old
	# saida = im_rgb + [im_b]
	# retorno = []
	#
	# j = 0
	# for i in saida:
	# 	try:
	# 		# i.filter(ImageFilter.CONTOUR).show()
	# 		i = i.filter(ImageFilter.BoxBlur(radius=blur_radio))
	# 		i = Image.eval(i, (lambda x: 255 if x > (255-pixel_valor) else 0))	# se tiver cor 0, sem cor 255
	# 		i = i.filter(ImageFilter.CONTOUR)
	# 		i.show()
	# 		# i.save('cavalin'+str(j)+'.jpg')
	# 		retorno.append(i.getdata())
	# 	except:
	# 		print('i')
	# 		retorno.append(None)
	# 	j = j + 1



	contornos = []
	# contorno da imagem preta
	im_b = im_b.filter(ImageFilter.BoxBlur(radius=blur_radio))
	im_b = Image.eval(im_b, (lambda x: 255 if x > (255-pixel_valor) else 0))	# se tiver cor 0, sem cor 255
	im_b = im_b.filter(ImageFilter.CONTOUR)
	contornos = [im_b]


	larg, altu = im_rgb[0].size
	for im in im_rgb:
		# contorno da im
		im = im.filter(ImageFilter.BoxBlur(radius=blur_radio))
		im = Image.eval(im, (lambda x: 255 if x > (255-pixel_valor) else 0))	# se tiver cor 0, sem cor 255
		im = im.filter(ImageFilter.CONTOUR)
		data = im.getdata()
		# removo da im_b os pixeis em volta do contorno preto
		for i in range(raio_remocao, altu-raio_remocao):	# n passo pelos cantos da im
			for j in range(raio_remocao, larg-raio_remocao):
				if data[i*larg + j] == 0:	# se pixel preto, 'removo' os pixeis de im_b no entorno
					for y in range(-raio_remocao,raio_remocao+1):  		# pelas linha acima e abaixo
						for x in range(-raio_remocao,raio_remocao+1):	# pelos lados
							im_b.putpixel( ((j+x),(i+y)), 255 )
		# add im aos contornos
		contornos.append(im)

	# atualizo a im_b (dps de remover os contornos rgb)
	contornos[0] = im_b

	# pego as im data
	retorno = []
	for im in contornos:
		# im.show()
		retorno.append(im.getdata())




	# for j in range(4):
	# 	i = saida[j]
	# 	i = i.filter(ImageFilter.BoxBlur(radius=2))
	# 	i = Image.eval(i, (lambda x: 0 if x > (255-pixel_valor) else 255))	# se tiver cor 0, sem cor 255
	# 	i = ImageOps.invert(i)
	# 	i = i.filter(ImageFilter.CONTOUR)
	# 	i.save('cavalin'+str(j)+'.jpg')






	# print(im_rgb[0].sum())
	# im_b.show()
	# # im_b.filter(ImageFilter.CONTOUR).show()
	# for i in im_rgb:
	# 	i.show()
	# 	# i.filter(ImageFilter.CONTOUR).show()


	# for i in range(len(imagens)):
	# 	imagens[i] = imagens[i].filter(ImageFilter.CONTOUR)
	#
	# for i in range(len(imagens)):
	# 	# imagens[i].save('pas_'+str(i)+'.jpg')
	# 	imagens[i].show()

	retorno.append(im.size)
	#	0	  1		2		3		4
	# [red, green, blue, black, (largura, altura)]
	return retorno



def ajustar_imagem(nome):
	im = Image.open(nome)
	largura, altura = im.size
	multi = tamanho[0] / largura		# proporcao com base na largura (pra alcancar o tamanho)
	if altura*multi > tamanho[1]:		# se a altura passar do tamanho
		multi = tamanho[1] / altura		# proporcao com base na altura
	nova_largura = int(largura*multi)
	nova_altura  = int(altura*multi)
	nova_im = im.resize((nova_largura, nova_altura), Image.LANCZOS)	# mudo o tamanho
	return nova_im

def algo_antigo():
	arquivo = 'palheta3.jpg'
	im = Image.open(arquivo)
	largura, altura = im.size
	multi = tamanho[0] / largura		# proporcao com base na largura (pra alcancar o tamanho)
	if altura*multi > tamanho[1]:		# se a altura passar do tamanho
		multi = tamanho[1] / altura		# proporcao com base na altura
	nova_largura = int(largura*multi)
	nova_altura  = int(altura*multi)
	nova_im = im.resize((nova_largura, nova_altura), Image.LANCZOS)	# mudo o tamanho
	# im = ImageEnhance.Contrast(im)		# aumento o contraste da imagem
	# im.enhance(2.0).show()

	im_b = im.convert('L', palette=Image.ADAPTIVE)
	# p.show()
	# print(im_p.getpixel((0,0)))
	# arquivo = 'fonte2.jpg'	# testo
	# im = Image.open(arquivo)

	im_rgb = Image.Image.split(im)	# red green blue




	# nova_im = [Image.new("RGB",im.size) for _ in range(3)]


	# print(ims[0].getpixel((0,0)))
	# print(nova_im[1].getpixel((0,0)))
	# print(nova_im[2].getpixel((0,0)))
	# print(nova_im[0].getpixel((50,50)))
	# red = nova_im[0].convert('P', palette=Image.ADAPTIVE)
	# red.show()

	# for i in range(3):
	# 	pixels = ims[i].getdata()
	# 	nova = []
	# 	for p in pixels:
	# 		# print(p)
	# 		cor = [0,0,0]
	# 		if p > 255/2:
	# 			cor[i] = 255
	# 		cor = tuple(cor)
	# 		nova.append(cor)
	# 	nova_im[i].putdata(nova)
		# nova_im[i].show()




	pixel_valor = 55

	imagens = [im_b] + list(im_rgb)
	# imagens[0].show()

	for i in range(len(imagens)):
		imagens[i] = imagens[i].filter(ImageFilter.BoxBlur(radius=4))

	imagens[0] = Image.eval(imagens[0], (lambda x: 0 if x < pixel_valor else 255))
	for i in range(1, len(imagens)):
		imagens[i] = Image.eval(imagens[i], (lambda x: 255 if x > (255-pixel_valor) else 0))
		# imagens[i] = Image.eval(imagens[i], (lambda x: 0 if x > (255-pixel_valor) else 255))

	# for i in range(len(imagens)):
	# 	imagens[i] = imagens[i].filter(ImageFilter.CONTOUR)

	for i in range(len(imagens)):
		# imagens[i].save('pas_'+str(i)+'.jpg')
		imagens[i].show()





	# im_temp = Image.eval(im_b, (lambda x: 0 if x < pixel_valor else 255))
	# imagens_tratadas = [im_temp]
	#
	# for i in im_rgb:
	# 	im_temp = Image.eval(i, (lambda x: 255 if x > (255-pixel_valor) else 0))
	# 	imagens_tratadas.append(im_temp)
	#
	# for i in imagens_tratadas:
	# 	i.convert('1',dither=Image.NONE).show()


	# for i in imagens:
	# 	# i_2 = i.filter(ImageFilter.BoxBlur(radius=3))
	# 	i_2 = i
	# 	# i_3 = Image.eval(i_2, (lambda x: 255 if x > 50 else 0))
	# 	i_3 = Image.eval(i_2, (lambda x: 255 if x > 200 else 0))
	# 	# i_4 = i_3.filter(ImageFilter.CONTOUR)
	# 	# imagens_tratadas.append(i_4)
	# 	imagens_tratadas.append(i_3)
	#
	# tempo = imagens[0].filter(ImageFilter.BoxBlur(radius=3))
	# tempo2 = Image.eval(tempo, (lambda x: 0 if x < 55 else 255))
	# imagens_tratadas[0] = tempo2
	#
	# pal = (
	# 	[0,0,0],
	# 	[255,0,0],
	# 	[0,255,0],
	# 	[0,0,0, 0,0,255]
	# 	)
	# imagens_tratadas[0].show()
	# for i in range(1,4):
	# 	palheta = ImagePalette.ImagePalette(mode='P', palette=pal[i], size=len(pal[i]))
	#
	# 	iii = imagens_tratadas[i].convert("P")
	# 	iii.putpalette(palheta)
	# 	iii.show()







	# # pegar os pixeis > 50
	# imagens = [im_b, im_rgb[0], im_rgb[1], im_rgb[2]]
	# imagens_tratadas = []
	# for i in imagens:
	# 	# i_2 = i.filter(ImageFilter.BoxBlur(radius=3))
	# 	i_2 = i
	# 	# i_3 = Image.eval(i_2, (lambda x: 255 if x > 50 else 0))
	# 	i_3 = Image.eval(i_2, (lambda x: 255 if x > 200 else 0))
	# 	# i_4 = i_3.filter(ImageFilter.CONTOUR)
	# 	# imagens_tratadas.append(i_4)
	# 	imagens_tratadas.append(i_3)
	#
	# tempo = imagens[0].filter(ImageFilter.BoxBlur(radius=3))
	# tempo2 = Image.eval(tempo, (lambda x: 0 if x < 55 else 255))
	# imagens_tratadas[0] = tempo2
	#
	# pal = (
	# 	[0,0,0],
	# 	[255,0,0],
	# 	[0,255,0],
	# 	[0,0,0, 0,0,255]
	# 	)
	# imagens_tratadas[0].show()
	# for i in range(1,4):
	# 	palheta = ImagePalette.ImagePalette(mode='P', palette=pal[i], size=len(pal[i]))
	#
	# 	iii = imagens_tratadas[i].convert("P")
	# 	iii.putpalette(palheta)
	# 	iii.show()


	# # funcionando
	# im_b2 = im_b.filter(ImageFilter.BoxBlur(radius=4))
	# im_b3 = Image.eval(im_b2, (lambda x: 255 if x > 50 else 0))
	# im_b3.show()
	# im_b4 = im_b3.filter(ImageFilter.CONTOUR)
	# im_b4.show()
	# #


	# im_b2 = Image.eval(im_b, (lambda x: 255 if x > 50 else 0))
	# im_b3 = im_b2.filter(ImageFilter.BoxBlur(radius=4))
	# im_b3.show()



	# im_b.convert('1', dither=Image.NONE).show()


	# im_b2.show()

	# im_b3 = im_b2.filter(ImageFilter.CONTOUR)
	# im_b3 = im_b2.filter(ImageFilter.UnsharpMask(radius=5, percent=1, threshold=30))

	# im_b2.save('pretobranco.jpg')
	# im_b3 = ImageEnhance.Contrast(im_b2)		# aumento o contraste da imagem
	# im_b3.enhance(2.0).show()

	# im_b.convert('1', dither=Image.NONE).show()
	# im_rgb[2].convert('1', dither=Image.NONE).show()



	# for i in imagens:
		# i.convert('1', dither=Image.FLOYDSTEINBERG).show()

	return None


# quebra a img em nas 3 cores
def testo1():
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


# muda de rgb pra 1 bit
def testo2():
	arquivo = 'fonte2.jpg'	# testo
	im = Image.open(arquivo)
	# Image.convert(mode=None, matrix=None, dither=None, palette=0, colors=256)

	out = im.convert('1', dither=Image.NONE)
	# pixels = out.getdata() # pixeis em linha, comecando do canto sup esq
	# for p in pixels:
	# 	print(p)
	bm = out.tobitmap()
	for linha in bm:
		print(linha)


# muda a palheta de cores
def testo3():
	arquivo = 'cores.jpg'	# testo
	im = Image.open(arquivo)
	im.show()
	# im = im.quantize(colors=50, method=1) # diminuo o num de cores
	# im.show()
	p = im.convert('1', palette=Image.ADAPTIVE)
	p.show()

	# arquivo = 'fonte2.jpg'	# testo
	# im = Image.open(arquivo)

	imgs = Image.Image.split(im)	# red green blue
	nova_img = [Image.new("RGB",im.size) for _ in range(3)]

	# print(nova_img[0].getpixel((50,50)))
	# red = nova_img[0].convert('P', palette=Image.ADAPTIVE)
	# red.show()

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

def testo4():
	# out = im.quantize(colors=256, method=None, kmeans=0, palette=None)
	# p = im.getpixel((0,0))
	# print(ImagePalette.getcolor(color=p))

	arquivo = 'passaro.jpg'	# testo
	im = Image.open(arquivo)
	im.show()

	im2 = ImageEnhance.Contrast(im)
	# im2 = ImageEnhance.Color(im)
	# im2 = ImageEnhance.Brightness(im)
	# im2 = ImageEnhance.Sharpness(im)
	# im2.enhance(0.0).show()
	im2.enhance(2.0).show()
	# im2.enhance(3.0).show()
	# im2.enhance(-10.0).show()
	# im2.enhance(10.0).show()

def main():
	# entrada = input()
	entrada = 'passaro.jpg'
	ajustar_imagem(entrada)

# main()

# quebrar_cores('')

# testo1()
# testo2()
# testo3()
# testo4()
