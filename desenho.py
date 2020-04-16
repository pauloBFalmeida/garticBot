from PIL import Image
from time import sleep, time
import pyautogui
import configuracoes
import padronizador

def distancia_total(pontos):
	dist = 0		# distancia
	u = pontos[0]	# ultimo (nunca comeca (-1,-1))
	for p in pontos:
		if p != (-1,-1):
			# distancia entre 2 pontos
			d = int( ((p[0] - u[0])**2 + (p[1] - u[1])**2)**(1/2) )
			dist = dist + d	# somo 'd' a distancia total
			u = p			# ultimo recebe atual
	return dist


def borda(nome):
	arquivo = nome			# com base no nome passado
	# img = Image.open('test5.jpg')
	img = Image.open(arquivo)
	largura, altura = img.size
	qtde_pixels = largura * altura
	pixels = img.getdata() # pixeis em linha, comecando do canto sup esq

	# crio uma borda falsa com brancos
	linhas  = (altura+2)
	colunas = (largura+2)
	pixels_pretos = [[False for i in range(colunas)] for j in range(linhas)]

	# percorro as colunas das linhas (ignorando as bordas)
	for i in range(1, altura+1):
		for j in range(1, largura+1):
			pos = (i-1)*largura + (j-1) # posicao na lista de pixels
			cor = sum(list(pixels[pos]))
			if cor < 50: # pixel preto
				pixels_pretos[i][j] = True


	# pixels no interior da imagem (ou seja sem a borda falsa)
	pixels_borda = [[False for i in range(colunas)] for j in range(linhas)] # crio uma borda falsa com brancos
	for i in range(1, altura+1):
		for j in range(1, largura+1): # percorro as colunas das linhas
			if pixels_pretos[i][j]: # se o pixel for preto
				canto_branco = False
				if   not pixels_pretos[i-1][j]: canto_branco = True # pixel de cima eh branco
				elif not pixels_pretos[i+1][j]: canto_branco = True # pixel de baixo eh branco
				elif not pixels_pretos[i][j-1]: canto_branco = True # pixel da esquerda eh branco
				elif not pixels_pretos[i][j+1]: canto_branco = True # pixel da direita eh branco
				if canto_branco: # se o pixel possui algum dos laterais branco
					pixels_borda[i][j] = True # contar com a borda falsa

	# # desenha a borda no terminal (contem borda falsa)
	f = open('saida.txt','w')
	for i in range(altura+2):
		linha = ''
		for j in range(largura+2):
			if (pixels_borda[i][j]):
				linha = linha + '#'
			else:
				linha = linha + '-'
		# print(linha)
		f.write(linha)
		f.write('\n')
	f.close()

	# cria a sequencia de retas

	# lembrar da borda falsa em pixels_borda
	pos_visitar = [(i,j) for i in range(1, altura+1) for j in range(1, largura+1)]
	pontos = []

	# posicao de busca que vai se movendo pela borda criando retas (2 duplas de (i,j))
	while len(pos_visitar) > 0: 			# enquanto tiver posicoes a serem visitadas
		pos = pos_visitar.pop(0)			# pego a primeira pos da lista
		if pixels_borda[pos[0]][pos[1]]:	# se for da borda
			pontos.append(pos)				# add a pos de inicio da seq em 'pontos'
			pos_busca  = list(pos)			# tenho uma posicao de busca q vai se movendo pela borda
			tentativas = 3
			seq_feita = False

			# vejo se ele se moveu, se ele n for pra dir/esq/cima/baixo entao eu paro
			while tentativas > 0:

				# procuro a direita (j+1)
				# print(pos_busca)
				pos_anterior = pos_busca[1] 						# pra ver se ele foi para direita
				pos_busca[1] = pos_busca[1] + 1
				# nao sair da borda a dir, pertence a borda, nao foi visitada ainda
				# print('dir')
				# print(pos_busca)
				while (pos_busca[1] <= largura) and (pixels_borda[pos_busca[0]][pos_busca[1]]) and ((pos_busca[0], pos_busca[1]) in pos_visitar):
					pos_visitar.remove((pos_busca[0], pos_busca[1]))	# marco que a pos foi visitada
					pos_busca[1]  = pos_busca[1] + 1					# passo pra prox a direita

				pos_busca[1] = pos_busca[1]-1							# ajusto a pos_busca pra ultima valida (pois ela estava vendo se a do lado era valida)
				if (pos_anterior != pos_busca[1]):					# encontrou outras a direita
					pontos.append((pos_busca[0], pos_busca[1]))			# add a pos em 'pontos'
					seq_feita = True
					tentativas = 3
				else:
					tentativas = tentativas - 1 						# nao conseguiu ir pra esse lado

				# procuro a baixo (i+1)
				# print(pos_busca)
				pos_anterior = pos_busca[0] 							# pra ver se ele foi para baixo
				pos_busca[0] = pos_busca[0] + 1
				# nao sair da borda em baixo, pertence a borda, nao foi visitada ainda
				# print('baixo')
				# print(pos_busca)
				while (pos_busca[0] <= altura) and (pixels_borda[pos_busca[0]][pos_busca[1]]) and ((pos_busca[0], pos_busca[1]) in pos_visitar):
					pos_visitar.remove((pos_busca[0], pos_busca[1]))	# marco que a pos foi visitada
					pos_busca[0]  = pos_busca[0] + 1					# passo pra prox a baixo

				pos_busca[0] = pos_busca[0]-1							# ajusto a pos_busca pra ultima valida (pois ela estava vendo se a do lado era valida)
				if (pos_anterior != pos_busca[0]):						# encontrou outras a baixo
					pontos.append((pos_busca[0], pos_busca[1]))			# add a pos em 'pontos'
					seq_feita = True
					tentativas = 3
				else:
					tentativas = tentativas - 1 						# nao conseguiu ir pra esse lado

				# procuro a esquerda (j-1)
				# print(pos_busca)
				pos_anterior = pos_busca[1] 							# pra ver se ele foi para esquerda
				pos_busca[1] = pos_busca[1] - 1
				# nao sair da borda a esq, pertence a borda, nao foi visitada ainda
				# print('esq')
				# print(pos_busca)
				while (pos_busca[1] > 0) and (pixels_borda[pos_busca[0]][pos_busca[1]]) and ((pos_busca[0], pos_busca[1]) in pos_visitar):
					pos_visitar.remove((pos_busca[0], pos_busca[1]))	# marco que a pos foi visitada
					pos_busca[1]  = pos_busca[1] - 1					# passo pra prox a esquerda

				pos_busca[1] = pos_busca[1]+1						# ajusto a pos_busca pra ultima valida (pois ela estava vendo se a do lado era valida)
				if (pos_anterior != pos_busca[1]):					# encontrou outras a esquerda
					pontos.append((pos_busca[0], pos_busca[1]))			# add a pos em 'pontos'
					seq_feita = True
					tentativas = 3
				else:
					tentativas = tentativas - 1 						# nao conseguiu ir pra esse lado

				# procuro a cima (i-1)
				# print(pos_busca)
				pos_anterior = pos_busca[0] 							# pra ver se ele foi para cima
				pos_busca[0] = pos_busca[0] - 1
				# nao sair da borda em baixo, pertence a borda, nao foi visitada ainda
				# print('cima')
				# print(pos_busca)
				while (pos_busca[0] > 0) and (pixels_borda[pos_busca[0]][pos_busca[1]]) and ((pos_busca[0], pos_busca[1]) in pos_visitar):
					pos_visitar.remove((pos_busca[0], pos_busca[1]))	# marco que a pos foi visitada
					pos_busca[0]  = pos_busca[0] - 1					# passo pra prox a baixo

				pos_busca[0] = pos_busca[0]+1						# ajusto a pos_busca pra ultima valida (pois ela estava vendo se a do lado era valida)
				if (pos_anterior != pos_busca[0]):					# encontrou outras a cima
					pontos.append((pos_busca[0], pos_busca[1]))			# add a pos em 'pontos'
					seq_feita = True
					tentativas = 3
				else:
					tentativas = tentativas - 1 						# nao conseguiu ir pra esse lado

			# quando acabar a sequencia adiciona o proprio ponto
			if seq_feita: pontos.append((-1,-1))
			# re-arranjo a lista pra ficar mais proxima da ultima posicao buscada
			pos_visitar_2 = []
			for p in pos_visitar:
				# calculo a diferenca entre as posicoes da lista e a ultima posicao
				dif = (p[0] - pos_busca[0])**2 + (p[1] - pos_busca[1])**2
				# triplas contendo a diferenca como ultimo elemento
				pos_visitar_2.append(p + (dif,))
			# organizo com base no ultimo elemento da tripla (dif)
			pos_visitar_2 = sorted(pos_visitar_2, key=lambda p: p[2])
			# removo o ultimo elemento da tripla (dif)
			pos_visitar = []
			for p in pos_visitar_2:
				pos_visitar.append(p[:2])


	# print a seq no terminal
	print()
	for p in pontos:
		print(p)


def sequencia(data, largura, altura):
	# crio uma borda falsa com brancos
	linhas  = (altura+2)
	colunas = (largura+2)
	pixels_borda = [[False for i in range(colunas)] for j in range(linhas)]

	# percorro as colunas das linhas (ignorando as bordas falsas)
	for i in range(1, altura+1):
		for j in range(1, largura+1):
			pos = (i-1)*largura + (j-1) # posicao na lista de pixels
			cor = data[pos]
			if cor == 0: # pixel preto
				pixels_borda[i][j] = True

	# # desenha a borda no terminal (contem borda falsa)
	f = open('saida.txt','w')
	for i in range(altura+2):
		linha = ''
		for j in range(largura+2):
			if (pixels_borda[i][j]):
				linha = linha + '#'
			else:
				linha = linha + '-'
		# print(linha)
		f.write(linha)
		f.write('\n')
	f.close()

	# cria a sequencia de retas

	# lembrar da borda falsa em pixels_borda
	pos_visitar = [(i,j) for i in range(1, altura+1) for j in range(1, largura+1)]
	pontos = []

	# posicao de busca que vai se movendo pela borda criando retas (2 duplas de (i,j))
	while len(pos_visitar) > 0: 			# enquanto tiver posicoes a serem visitadas
		pos = pos_visitar.pop(0)			# pego a primeira pos da lista
		if pixels_borda[pos[0]][pos[1]]:	# se for da borda
			pontos.append(pos)				# add a pos de inicio da seq em 'pontos'
			pos_busca  = list(pos)			# tenho uma posicao de busca q vai se movendo pela borda
			tentativas = 3
			seq_feita = False

			# vejo se ele se moveu, se ele n for pra dir/esq/cima/baixo entao eu paro
			while tentativas > 0:

				# procuro a direita (j+1)
				# print(pos_busca)
				pos_anterior = pos_busca[1] 						# pra ver se ele foi para direita
				pos_busca[1] = pos_busca[1] + 1
				# nao sair da borda a dir, pertence a borda, nao foi visitada ainda
				# print('dir')
				# print(pos_busca)
				while (pos_busca[1] <= largura) and (pixels_borda[pos_busca[0]][pos_busca[1]]) and ((pos_busca[0], pos_busca[1]) in pos_visitar):
					pos_visitar.remove((pos_busca[0], pos_busca[1]))	# marco que a pos foi visitada
					pos_busca[1]  = pos_busca[1] + 1					# passo pra prox a direita

				pos_busca[1] = pos_busca[1]-1							# ajusto a pos_busca pra ultima valida (pois ela estava vendo se a do lado era valida)
				if (pos_anterior != pos_busca[1]):					# encontrou outras a direita
					pontos.append((pos_busca[0], pos_busca[1]))			# add a pos em 'pontos'
					seq_feita = True
					tentativas = 3
				else:
					tentativas = tentativas - 1 						# nao conseguiu ir pra esse lado

				# procuro a baixo (i+1)
				# print(pos_busca)
				pos_anterior = pos_busca[0] 							# pra ver se ele foi para baixo
				pos_busca[0] = pos_busca[0] + 1
				# nao sair da borda em baixo, pertence a borda, nao foi visitada ainda
				# print('baixo')
				# print(pos_busca)
				while (pos_busca[0] <= altura) and (pixels_borda[pos_busca[0]][pos_busca[1]]) and ((pos_busca[0], pos_busca[1]) in pos_visitar):
					pos_visitar.remove((pos_busca[0], pos_busca[1]))	# marco que a pos foi visitada
					pos_busca[0]  = pos_busca[0] + 1					# passo pra prox a baixo

				pos_busca[0] = pos_busca[0]-1							# ajusto a pos_busca pra ultima valida (pois ela estava vendo se a do lado era valida)
				if (pos_anterior != pos_busca[0]):						# encontrou outras a baixo
					pontos.append((pos_busca[0], pos_busca[1]))			# add a pos em 'pontos'
					seq_feita = True
					tentativas = 3
				else:
					tentativas = tentativas - 1 						# nao conseguiu ir pra esse lado

				# procuro a esquerda (j-1)
				# print(pos_busca)
				pos_anterior = pos_busca[1] 							# pra ver se ele foi para esquerda
				pos_busca[1] = pos_busca[1] - 1
				# nao sair da borda a esq, pertence a borda, nao foi visitada ainda
				# print('esq')
				# print(pos_busca)
				while (pos_busca[1] > 0) and (pixels_borda[pos_busca[0]][pos_busca[1]]) and ((pos_busca[0], pos_busca[1]) in pos_visitar):
					pos_visitar.remove((pos_busca[0], pos_busca[1]))	# marco que a pos foi visitada
					pos_busca[1]  = pos_busca[1] - 1					# passo pra prox a esquerda

				pos_busca[1] = pos_busca[1]+1						# ajusto a pos_busca pra ultima valida (pois ela estava vendo se a do lado era valida)
				if (pos_anterior != pos_busca[1]):					# encontrou outras a esquerda
					pontos.append((pos_busca[0], pos_busca[1]))			# add a pos em 'pontos'
					seq_feita = True
					tentativas = 3
				else:
					tentativas = tentativas - 1 						# nao conseguiu ir pra esse lado

				# procuro a cima (i-1)
				# print(pos_busca)
				pos_anterior = pos_busca[0] 							# pra ver se ele foi para cima
				pos_busca[0] = pos_busca[0] - 1
				# nao sair da borda em baixo, pertence a borda, nao foi visitada ainda
				# print('cima')
				# print(pos_busca)
				while (pos_busca[0] > 0) and (pixels_borda[pos_busca[0]][pos_busca[1]]) and ((pos_busca[0], pos_busca[1]) in pos_visitar):
					pos_visitar.remove((pos_busca[0], pos_busca[1]))	# marco que a pos foi visitada
					pos_busca[0]  = pos_busca[0] - 1					# passo pra prox a baixo

				pos_busca[0] = pos_busca[0]+1						# ajusto a pos_busca pra ultima valida (pois ela estava vendo se a do lado era valida)
				if (pos_anterior != pos_busca[0]):					# encontrou outras a cima
					pontos.append((pos_busca[0], pos_busca[1]))			# add a pos em 'pontos'
					seq_feita = True
					tentativas = 3
				else:
					tentativas = tentativas - 1 						# nao conseguiu ir pra esse lado

			# quando acabar a sequencia adiciona o proprio ponto
			if seq_feita: pontos.append((-1,-1))
			# re-arranjo a lista pra ficar mais proxima da ultima posicao buscada
			pos_visitar_2 = []
			for p in pos_visitar:
				# calculo a diferenca entre as posicoes da lista e a ultima posicao
				dif = (p[0] - pos_busca[0])**2 + (p[1] - pos_busca[1])**2
				# triplas contendo a diferenca como ultimo elemento
				pos_visitar_2.append(p + (dif,))
			# organizo com base no ultimo elemento da tripla (dif)
			pos_visitar_2 = sorted(pos_visitar_2, key=lambda p: p[2])
			# removo o ultimo elemento da tripla (dif)
			pos_visitar = []
			for p in pos_visitar_2:
				pos_visitar.append(p[:2])


	# print a seq no terminal
	print()
	for p in pontos:
		print(p)

	# 'pontos' retorna como uma matriz (i,j) (y,x)
	pontosI = []
	for p in pontos:	# inverto pra ser (j,i) (x,y)
		pontosI.append((p[1],p[0]))

	return pontosI

def otimizar(pontos, nivel):
	if nivel == 0:
		valor_colinear = 5
		rem_min = 2
		rem_max = 2 + 1
	if nivel == 1:
		valor_colinear = 10
		rem_min = 2
		rem_max = 3 + 1

	# pontos = list(pontos)
	print('inicio '+str(len(pontos)))

	# otimiza retirando pequenas retas / pontos unicos
	# for i in range(3,5):
	for i in range(rem_min, rem_max):
		qtde_pontos = len(pontos)
		qtde_visitados = 2
		while qtde_visitados < qtde_pontos:
			p1 = pontos[qtde_visitados-2]
			p2 = pontos[qtde_visitados-1]
			p3 = pontos[qtde_visitados]
			# diferenca entre o primeiro e terceiro ponto
			dif = (p1[0] - p3[0])**2 + (p1[1] - p3[1])**2
			#  diferenca for pequena removo o ponto do meio
			if dif < i**2:
				pontos.remove(p2)
				qtde_pontos = qtde_pontos - 1		# remove um ponto na contagem de pontos
			qtde_visitados = qtde_visitados + 1		# add mais um ponto visitado


	print('meio '+str(len(pontos)))

	# otimiza retas que vao na mesma direcao
	# p1 p2 p3 praticamente o colineares
	# for _ in range(3):
	for _ in range(2):
		qtde_pontos = len(pontos)
		qtde_visitados = 2
		while qtde_visitados < qtde_pontos:
			p1 = pontos[qtde_visitados-2]
			p2 = pontos[qtde_visitados-1]
			p3 = pontos[qtde_visitados]
			# mesma variacao em x
			det = p1[0]*p2[1] + p1[1]*p3[0] + p2[0]*p3[1] - p2[1]*p3[0] - p1[0]*p3[1] - p1[1]*p2[0]
			if abs(det) < valor_colinear:
				pontos.remove(p2)
				qtde_pontos = qtde_pontos - 1 		# remove um ponto na contagem de pontos
			qtde_visitados = qtde_visitados + 1		# add mais um ponto visitado


	print('fim '+str(len(pontos)))

	return pontos



def draw(pontos, largura, altura):
	# duracao = configuracoes.get_from_file('duracao')
	inicio 	= configuracoes.get_from_file('canto_sup_esq')
	inicio = (inicio[0], int(inicio[1] + inicio[1] * 0.25))
	fim 	= configuracoes.get_from_file('canto_inf_dir')
	tamanho = (fim[0] - inicio[0], fim[1] - inicio[1])
	print('inicio')
	print (inicio)
	print (fim)
	print (tamanho)

	distancia = distancia_total(pontos)
	dur_dis = 35 / distancia	# duracao por distancia

	duracao = 40 / len(pontos)
	if duracao > 1.5: duracao = 1.5

	# img = Image.open(arquivo)
	# largura, altura = img.size
	# inicio = (250, 200)   # gartic
	# tamanho = (425, 250)
	# inicio = (100, 200)	#paint
	# tamanho = (425, 250)
	multi = tamanho[0]/largura
	if (multi * altura > tamanho[1]):
		multi = tamanho[1]/altura

	# duracao = 0
	arrastar = False
	p_antigo = pyautogui.position()

	for p in pontos:

		print(arrastar)
		# sleep(duracao)
		if (p == (-1,-1)):
			arrastar = False
			print('jump ' + str(p))
			continue

		px = int(p[0]*multi) + inicio[0]
		py = int(p[1]*multi) + inicio[1]

		# duracao
		dis = ((px - p_antigo[0])**2 + (py - p_antigo[1])**2)**(1/2)
		duracao = dis * dur_dis

		if not arrastar:
			print('mover ' + str(p))
			pyautogui.moveTo(px, py, duracao)
			arrastar = True
		else:
			x = px - p_antigo[0]
			y = py - p_antigo[1]
			print('arrastar ' + str(p))
			pyautogui.drag(x,y, duracao)

		p_antigo = (px, py)

	print(duracao)

def principal(nome):
	# padronizador.ajustar_imagem(nome)
	bordas = padronizador.quebrar_cores(nome)
	largura, altura = bordas[4]
	pontos = sequencia(bordas[1], largura, altura)
	print('dist')
	print(distancia_total(pontos))
	# print()
	# print(seq[0])
	# print()

	# if len(pontos) > 50:
	# 	pontos = otimizar(pontos,1)
	pontos = otimizar(pontos, 0)
	print('dist')
	print(distancia_total(pontos))

	sleep(1)
	draw(pontos, largura, altura)

principal('asno2.jpg')

def test():
	pontos = [(3,3),(2,2),(1,1)]
	qtde_visitados = 2
	p1 = pontos[qtde_visitados-2]
	p2 = pontos[qtde_visitados-1]
	p3 = pontos[qtde_visitados]
	# mesma variacao em x
	det = p1[0]*p2[1] + p1[1]*p3[0] + p2[0]*p3[1] - p2[1]*p3[0] - p1[0]*p3[1] - p1[1]*p2[0]
	print(det)
	pri = [[0 for _ in range(5)]for _ in range(5)]
	for i in range(3):
		p = pontos[i]
		pri[p[0]][p[1]] = i+1

	for p in pri:
		print(p)



# millis1 = int(round(time() * 1000))
# desenhar2()
# borda()
# test()
#
# millis2 = int(round(time() * 1000))
# print('time '+str(millis2-millis1))
