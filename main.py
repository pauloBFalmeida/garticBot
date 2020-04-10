#! python3
from PIL import Image
import pyautogui, sys, time, pickle, os.path
import configuracoes		# arquivo de configuracoes
import desenho

class HUB():

	def __init__(self):
		self.tempo_desenho = 40 	# tempo para fazer o desenho em segundos
		self.tempo_envio   = 1/3	# tempo em segundos entre envio de palavras

	def help(self):
		print(
			"(É indicado jogar com a tela dividida ao meio, entre a aba do gartic e o terminal)\n"
			"Digite:\n"
			"/h ou /help para exibir essa ajuda com os comandos\n"
			"/c ou /config para iniciar os ajustes\n"
			"/t ou /tempo para alterar o tempo de desenho\n"
			"/e ou /envio para alterar o tempo entre o envio de cada palavra\n"
			"/n ou /next indica ao programa q passou o turno\n"
			"/d ou /draw informa q e o round pra desenhar\n"
			"/w ou /word para \n"
			"/q ou /quit para parar o programa\n"
			)

	def config_armazenadas(self):
		try:
			if configuracoes.size_file() > 0: 	# vejo se o arquivo existe
				print('existe')
			print("Configurações carregadas com sucesso")
		except:
			print("Sem configurações previas, iniciando ajustes")
			time.sleep(1)
			self.config()

	def config(self):
		configuracoes.inicio()

	def tempo_desenho_ajuste(self):
		print(
			"tempo para fazer o desenho \n"
			"(recomendado acima de 30)\n"
			"atual: "+tempo_desenho
			)
		tempo_desenho = input()
		tempo_desenho = int(tempo_desenho)

	def tempo_envio_ajuste(self):
		print(
			"quantidade de tempo entra cada envio de palavras\n"
			"(recomendado acima de 0.3)\n"
			"atual: "+tempo_envio
			)
		tempo_envio = input()
		tempo_envio = int(tempo_envio)

	def draw(self):
		print("Digite a palavra para ser desenhada")
		while True:
			palavra = input()
			file = palavra+'.jpg'
			# verifico se existe essa imagem
			if os.path.isfile(file):
				break
			else:
				print("Não foi possível encontrar a imagem")
		# desenho a imagem
		print("Imagem encontrada")
		desenho.borda(file)

	def loop(self):
		while True:
			entrada = input()
			if   (entrada == "/h" or entrada == "/help"):
				self.help()
			elif (entrada == "/c" or entrada == "/config"):
				self.config()
			elif (entrada == "/t" or entrada == "/tempo"):
				self.tempo_desenho_ajuste()
			elif (entrada == "/e" or entrada == "/envio"):
				self.tempo_envio_ajuste()
			elif (entrada == "/n" or entrada == "/next"):
				self.tempo_ajuste()
			elif (entrada == "/d" or entrada == "/draw"):
				self.draw()
			elif (entrada == "/w" or entrada == "/word"):
				self.tempo_ajuste()
			elif (entrada == "/q" or entrada == "/quit"):
				break
			print("(Precisando de ajuda, digite '/help')")

	def executar(self):
		self.help()
		self.config_armazenadas()
		self.loop()


HUB().executar()
