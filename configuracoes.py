from PIL import Image
from time import sleep
import pickle
import pyautogui

pasta_config = '.\\configuracoes\\'
arquivo_config = pasta_config+'configs.pckl'

# retorna o valor de um item do arquivo
def get_from_file(item):
	valor = None

	file = open(arquivo_config,'rb')
	while True:
		try:
			conteudo = pickle.load(file)
			if conteudo[0] == item:		# se a 'variavel' for a mesma q item
				valor = conteudo[1]		# pego o valor
				break
		except EOFError: break
	file.close()
	return valor

def size_file():
	contador = 0
	file = open(arquivo_config,'rb')
	while True:
		try:
			conteudo = pickle.load(file)
			contador = contador + 1
		except EOFError: break
	file.close()
	return contador

def get_pasta_config():
	return pasta_config

def get_arquivo_config():
	return arquivo_config

def get_cords(item, gray, confianca, img):
	if img == None: 	# pegar da tela
		cords = pyautogui.locateOnScreen(pasta_config+item, grayscale=gray, confidence=confianca)
	else:
		cords = pyautogui.locate(pasta_config+item, img, grayscale=gray, confidence=confianca)
	if cords != None:	# retorno o centro da img (pra ser uma dupla, visto q a forma manual retorna duplas)
		return pyautogui.center(cords)
	return None

def get_cores(img):
	confianca = 1.0
	cords = None
	while confianca > 0.7:
		cords = get_cords('cores.jpg', False, confianca, img)
		confianca = confianca - 0.05
	return cords

def get_canto_sup_esq(img):
	confianca = 1.0
	cords = None
	while confianca > 0.7:
		cords = get_cords('canto_sup_esq.jpg', True, confianca, img)
		confianca = confianca - 0.05
	return cords

def get_canto_inf_dir(img):
	confianca = 1.0
	cords = None
	while confianca > 0.7:
		cords = get_cords('canto_inf_dir.jpg', True, confianca, img)
		confianca = confianca - 0.05
	return cords

def get_caixa_texto(img):
	confianca = 1.0
	cords = None
	while confianca > 0.7:
		cords = get_cords('caixa_texto.jpg', True, confianca, img)
		confianca = confianca - 0.05
	return cords

def executar(img):
	cores = get_cores(img)
	if cores == None: print("Erro tabela de cores não foram encontradas")

	canto_sup_esq = get_canto_sup_esq(img)
	if canto_sup_esq == None: print("Erro canto sup esq não foi encontrada")

	canto_inf_dir = get_canto_inf_dir(img)
	if canto_inf_dir == None: print("Erro canto inf dir não foi encontrada")

	caixa_texto = get_caixa_texto(img)
	if caixa_texto == None: print("Erro caixa texto não foi encontrada")

	file = open(arquivo_config,'wb')
	pickle.dump(('cores',cores), file)
	pickle.dump(('canto_sup_esq',canto_sup_esq), file)
	pickle.dump(('canto_inf_dir',canto_inf_dir), file)
	pickle.dump(('caixa_texto',caixa_texto), file)
	file.close()

	print("Configurações foram atualizadas")

def automatica():
	print(
		"A forma automatica faz a análise de uma imagem para determinar as "
		"posições dos itens, deseja fazer um scan da tela? (essa forma pode "
		"não funcionar por diferentes fatores). Digite 's' para fazer um scan "
		"da tela ou digite 'i' para enviar uma imagem"
		)
	if input() == "s":		# scan
		executar(None)
	else:
		print("Por favor escreva o caminho para imagem "
			"(se estiver na mesma pasta, o nome da imagem) "
			"seguido da extensão do arquivo (recomendado: .jpg)"
			)
		img = input()
		executar(img)

def manual_exec(item):
	print("Coloque o mouse sobre "+item)
	for i in range(2,0,-1):	# contagem regressiva
		print(i)
		sleep(1)
	print("Posição capturada")
	return pyautogui.position()

def manual():
	print("Escolha o objeto e posicione o mouse, após 5 segundos será salva a posição")
	cores = None
	canto_sup_esq = None
	canto_inf_dir = None
	caixa_texto = None
	algo_mudou = False

	escolha = -1
	while escolha != "0":
		print("Digite:\n"
			"0 para sair e salvar as configurações\n"
			"1 para o canto superior esquerdo da tela de desenho\n"
			"2 para o canto inferior direito da tela de desenho\n"
			"3 para a caixa de envio de resposta"
			)
		escolha = input()
		if   escolha == "1":
			canto_sup_esq = manual_exec("o canto superior esquerdo da tela de desenho")
			algo_mudou = True
		elif escolha == "2":
			canto_inf_dir = manual_exec("o canto inferior direito da tela de desenho")
			algo_mudou = True
		elif escolha == "3":
			caixa_texto = manual_exec("a caixa de envio de resposta")
			algo_mudou = True

	if algo_mudou:			# mudei algo
		print('mudou')
		novas = [
			('cores',cores),
			('canto_sup_esq',canto_sup_esq),
			('canto_inf_dir',canto_inf_dir),
			('caixa_texto',caixa_texto)
			]
		# conteudo do arquivo em 'conteudo'
		file = open(arquivo_config, 'rb')
		unpickler = pickle.Unpickler(file)
		conteudo = []
		while True:
		    try:
		        conteudo.append(unpickler.load())
		    except EOFError: break
		file.close()

		for n in novas:
			if n[1] != None:				# foi atualizada
				for c in conteudo:
					if n[0] == c[0]:		# mesma 'variavel'
						conteudo.remove(c)	# retiro a antiga
				conteudo.append(n)			# add a nova

		# atualizo o arquivo
		file = open(arquivo_config,'wb')
		for c in conteudo:
			pickle.dump(c, file)
		file.close()


def inicio():
	print(
		"Bem vindo as configurações, aqui sao ajustadas as posições da tela de desenho, "
		"cores, caixa de texto pra enviar a resposta. É importante que a página "
		"do gartic.io já esteja na posição desejada. "
		"Digite 'a' para fazer as configurações "
		"de forma automática ou 'm' para a forma manual ou 'c' para cancelar"
		)
	r1 = input()
	if   r1 == "a":		# automatica
		automatica()
	elif r1 == "m":		# manual
		manual()
	else:
		print("Configurações canceladas")


# print o conteudo do arquivo (so usado em testes)
def test():
	print('ini')

	file = open(arquivo_config,'rb')
	saida = []

	while True:
	    try:
	        saida.append(pickle.load(file))
	    except EOFError: break

	file.close()

	for x in saida:
		print(x)

	print('fim')

# inicio()
#test()
# print(get_arquivo_config())
