#! python3
from PIL import Image
import pyautogui, sys, time


duracao_round = 100 # tempo do round de desenho em segundos
tempo_envio   = 1/3

# configs no arquivo
canto_sup_esq = (0,0)
canto_inf_dir = (0,0)
campo_escrita = (0,0)

def help():
	print(
		"É indicado jogar com a tela dividida ao meio, entre a aba do gartic e o terminal\n"
		"digite:\n"
		"/h ou /help para exibir essa ajuda com os comandos\n"
		"/c ou /config para iniciar os ajustes\n"
		"/t ou /tempo para alterar q quantidade de palavras por segundos\n"
		"/n ou /next indica ao programa q passou o turno\n"
		"/d ou /draw informa q e o round pra desenhar\n"
		"/w ou /word para \n"
		"/q ou /quit para parar o programa\n"
		)

def config_armazenadas():
	print('configs:')
	try:
		arquivo = open('configs.txt','r')
		canto_sup_esq = arquivo.readline()
		canto_inf_dir = arquivo.readline()
		campo_escrita = arquivo.readline()
		# print(canto_sup_esq)
		# print(canto_inf_dir)
		# print(campo_escrita)
		arquivo.close()
	except:
		print("Sem configurações previas, iniciando ajustes")
		time.sleep(2)
		config()

def config():
	print("É indicado jogar com a tela dividida ao meio, entre a aba do gartic e o terminal")
	arquivo = open('configs.txt','w')
	time.sleep(3)
	print("coloque o mouse sobre o canto superior esquerdo da tela de desenho")
	time.sleep(5)
	canto_sup_esq = pyautogui.position()
	arquivo.write(str(canto_sup_esq)+'\n')
	print("posicao capturada")
	time.sleep(1)
	print("coloque o mouse sobre o canto inferior direito da tela de desenho")
	time.sleep(5)
	canto_inf_dir = pyautogui.position()
	arquivo.write(str(canto_inf_dir)+'\n')
	print("posicao capturada")
	time.sleep(1)
	print("coloque o mouse sobre a caixa de envio de resposta")
	time.sleep(5)
	campo_escrita = pyautogui.position()
	arquivo.write(str(campo_escrita))
	print("posicao capturada")
	arquivo.close()
	config_armazenadas()
	print("Configurações foram atualizadas")

def tempo_ajuste():
	tempo_envio = input(
		"quantidade de tempo entra cada envio \n"
		"(recomendado acima de 0.3)"
		)
	print("Tempo foi atualizado com sucesso")

def draw():
	palavra = input("Digite a palavra para ser desenhada")


def loop():
	while True:
		entrada = input()
		if (entrada == "/h" or entrada == "/help"):
			help()
		elif (entrada == "/c" or entrada == "/config"):
			config()
		elif (entrada == "/t" or entrada == "/tempo"):
			tempo_ajuste()
		elif (entrada == "/n" or entrada == "/next"):
			tempo_ajuste()
		elif (entrada == "/d" or entrada == "/draw"):
			draw()
		elif (entrada == "/w" or entrada == "/word"):
			tempo_ajuste()
		elif (entrada == "/q" or entrada == "/quit"):
			break

def main():
	help()
	config_armazenadas()
	loop()

main()
