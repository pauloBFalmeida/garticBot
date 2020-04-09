print("digitar o nome de arquivo html (com .txt)")
arquivo_entrada = input()

arq = open(arquivo_entrada,'r')
wri = open("saida_"+arquivo_entrada,'w+')

for linha in arq:
	palavra = ""
	salvando_palavra = False
	button = ""
	salvando_button = False
	for letra in linha:
		if (letra == "<"):
			salvando_palavra = False
			salvando_button = True
		if salvando_palavra:
			palavra = palavra + letra
			# print(palavra)
		if salvando_button:
			button = button + letra
			# print(button)
		if (letra == ">"):
			salvando_palavra = True
			salvando_button = False
			if (button == "</button>"):
				# print(palavra)
				palavra = palavra + "\n"
				wri.write(palavra)
				break
			else:
				palavra = ""
				button = ""

arq.close()
wri.close()
