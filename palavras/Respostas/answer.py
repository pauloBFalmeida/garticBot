print("Escolha os temas a serem usados:")
arquivos = {"0" : "resp_alimentos.txt",
            "1" : "resp_animais.txt",
            "2" : "resp_desenho_animado.txt",
            "3" : "resp_filmes.txt",
            "4" : "resp_objetos.txt",
            "5" : "resp_profissoes.txt",
            "6" : "resp_verbos.txt",
            }

answers = []

print("0 - Alimentos\n1 - Animais\n2 - Desenho animado\n3 - Filmes\n4 - Objetos")
print("5 - Profissões\n6 - Verbos")
print("Digite todas suas escolhas em uma linha separadas por vírgula:")

choices = input().split(",")

for i in choices:
    arq = open(arquivos[i.strip()], "r")

    for linha in arq:
        answers.append(linha[:-1])

    arq.close()
answers.sort(key=len)


def match(text, pattern):
    if len(pattern) > len(text): return False
    for i in range(len(pattern)):
        if pattern[i] != "_" and text[i] != pattern[i]:
            return False

    return True

#Query mode

while True:
    query = input().split("+")
    possible_answers = answers.copy()
    quit_flag = False
    for q in query:
        if q.isdigit():
            q = int(q)
            erase_index = 0
            while erase_index < len(possible_answers):
                if len(possible_answers[erase_index]) == q:
                    erase_index += 1
                else:
                    possible_answers.pop(erase_index)
        elif q == "\\quit":
            quit_flag = True
        else:
            erase_index = 0
            while erase_index < len(possible_answers):
                if match(possible_answers[erase_index], q):
                    erase_index += 1
                else:
                    possible_answers.pop(erase_index)
    if quit_flag:
        break
    for i in possible_answers:
        print(i)
