#! python3
from PIL import Image, ImageDraw, ImageColor, ImagePalette, ImageEnhance, ImageFilter
import sys

tamanho = (100, 100)

def quebrar_cores(im):
	im = Image.open('passaro.jpg')	# teste
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

	pixel_valor = 55
	blur_radio	= 2

	data_rgb = []
	for i in range(len(im_rgb)):
		im_rgb[i] = im_rgb[i].filter(ImageFilter.BoxBlur(radius=blur_radio))
		# im_rgb[i] = Image.eval(im_rgb[i], (lambda x: 255 if x > (255-pixel_valor) else 0))
		im_rgb[i] = Image.eval(im_rgb[i], (lambda x: 0 if x > (255-pixel_valor) else 255))		# se tiver cor 0, preto 255
		data_rgb.append(im_rgb[i].getdata())

	for i in im_rgb:
		# i.show()
		print(i.getpixel((0,0)))

	# crio a parte preta vendo onde nenhuma das cores se encontram
	pixels_b = [0 for _ in range(len(data_rgb[0]))]
	for data in data_rgb:
		for i in range(len(data)):	# i de cada pixel
			pixels_b[i] = pixels_b[i] + data[i]
	for i in range(len(pixels_b)):
		if pixels_b[i] == 255*3:
			pixels_b[i] = 0			# pixel com cor preta
		else:
			pixels_b[i] = 255

	im_b = Image.new("L",im_rgb[0].size)
	im_b.putdata(pixels_b)


	# removo onde as cores se encontram (branco ou outra)
	for i in range(len(im_rgb)):
		# se for tiver 0 em mais de uma das im, removo de ambas




	# im_b.show()
	# # im_b.filter(ImageFilter.CONTOUR).show()
	# for i in im_rgb:
	# 	i.show()
		# # i.filter(ImageFilter.CONTOUR).show()

	# for i in range(len(imagens)):
	# 	imagens[i] = imagens[i].filter(ImageFilter.CONTOUR)
	#
	# for i in range(len(imagens)):
	# 	# imagens[i].save('pas_'+str(i)+'.jpg')
	# 	imagens[i].show()



def ajustar_imagem(arquivo):
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

quebrar_cores('')

# testo1()
# testo2()
# testo3()
# testo4()
