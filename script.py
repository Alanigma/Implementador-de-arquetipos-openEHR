vez=1
id = 0
idstring = "at0000"
arquivo = open('fakeADL.txt','w')
arquivo.close()
arquivoOrdem = open('ordem.txt','w')
arquivoOrdem.close()
maior = int(input("Qual é o maior at? Exemplo: se for at0050, digite 50:"))
bugados = []

while True:
    encontrado = False
    contador = 0
    arquivoADL = open('adl.txt', 'r')
    for linha in arquivoADL:
        contador += 1
        if contador>20:
            linha = linha.rstrip()
            arquivo = open('fakeADL.txt', 'a')

            if vez == 3:
                linha = str(linha)
                linha = linha.replace('text = <\"', '')
                linha = linha.replace('\">', '')
                linha = linha.strip(" ")
                arquivo.write(linha+"\n")
                vez = 1
            else:
                if idstring in linha:
                    encontrado = True
                    contadorletra = 0
                    if vez==1:
                       for letra in linha:
                           if letra == ' ':
                               contadorletra+=1
                           else:
                               break
                       linha = linha.split()
                       parar = False
                       arquivo.write(str(contadorletra)+'\n')
                       for letra in linha[0]:
                           if letra!='[' and parar == False:
                               arquivo.write(letra)
                           if letra == '[':
                                parar = True
                       arquivo.write("\n")
                       vez=2
                    elif vez==2:
                        vez=3
            arquivo.close()
    if encontrado==False: bugados.append(id)
    if id==maior:
        break
    else:
        id += 1
        if id < 10:
            idstring = "at000" + str(id)
        if id >= 10 and id < 100:
            idstring = "at00" + str(id)
        if id >= 100 and id < 1000:
            idstring = "at0" + str(id)
        if id >= 1000:
            idstring = "at" + str(id)

    arquivoADL.close()

vez=1
espacos=[]
tipo=[]
texto=[]

arquivo = open('fakeADL.txt', 'r')
for linha in arquivo:
    if len(texto)-1 in bugados:
        espacos.append(0)
        tipo.append('')
        texto.append('')
    if vez==1:
        espacos.append(int(linha))
        vez=2
    elif vez==2:
        tipo.append(linha)
        vez=3
    elif vez == 3:
        texto.append(linha)
        vez = 1
arquivo.close()

contador=0
ignorar=False
arquivoOrdem = open('ordem.txt','a')
arquivoADL = open('adl.txt','r')
for linha in arquivoADL:
    palavra = ''
    if contador > 20 and ignorar == False:
        linha = linha.rstrip()
        pegar=False
        linha.split()
        try:
            for letra in linha:
                if letra == '[':
                    pegar = True
                if letra == ']':
                    pegar = False
                    arquivoOrdem.write(palavra)
                    if int(palavra) == maior: ignorar=True
                    else: arquivoOrdem.write('\n')
                if pegar == True and letra.isnumeric():
                    palavra += letra
        except:
            print('/\/\/\/\/\/\\')
            print('\/\/\/\/\/\/')
    contador+=1
arquivoADL.close()
arquivoOrdem.close()

espacos2=[]
tipo2=[]
texto2=[]
arquivoOrdem = open('ordem.txt','r')
for linha in arquivoOrdem:
    espacos2.append(espacos[int(linha)])
    tipo2.append(tipo[int(linha)])
    texto2.append(texto[int(linha)])

arquivoOrdem.close()

#Geração de HTML
arquivoHTML = open('index.html','w')
arquivoHTML.close()

sectionOn=[0]
entrada=0

arquivoHTML = open('index.html','a')
arquivoHTML.write('<!DOCTYPE html>\n<html>\n<head>\n<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/components/form.css"/>\n</head>\n<body>\n<div class="container">\n<form class="ui form ui grid">\n')

for c in range(0, len(tipo2)):

    if tipo2[c] == "COMPOSITION\n":
        while len(sectionOn) > 1:
            arquivoHTML.write('</fieldset>\n')
            del sectionOn[len(sectionOn) - 1]
        arquivoHTML.write(f'<h1>\n{texto2[c]}</h1>\n')

    if tipo2[c] == "SECTION\n":
        if espacos2[c] > sectionOn[len(sectionOn) - 1]:
            sectionOn.append(espacos2[c])
            arquivoHTML.write(f'<fieldset>\n<legend>\n<h{len(sectionOn)}>\n{texto2[c]}</h{len(sectionOn)}>\n</legend>\n')
        elif espacos2[c] == sectionOn[len(sectionOn) - 1]:
            arquivoHTML.write(f'</fieldset>\n<fieldset>\n<legend>\n<h{len(sectionOn)}>\n{texto2[c]}</h{len(sectionOn)}>\n</legend>\n')
        while espacos2[c] < sectionOn[len(sectionOn) - 1]:
            arquivoHTML.write(f'</fieldset>\n')
            del sectionOn[len(sectionOn)-1]
            if espacos2[c] == sectionOn[len(sectionOn) - 1]:
                arquivoHTML.write(f'</fieldset>\n<fieldset>\n<legend>\n<h{len(sectionOn)}>\n{texto2[c]}</h{len(sectionOn)}>\n</legend>\n')

    if tipo2[c] == "ELEMENT\n":
        arquivoHTML.write(f'<div class="field four wide column">\n<label for="entrada{entrada}">\n{texto2[c]}</label>\n')
        for q in range(0, len(tipo2)):
            if tipo2[q] == "DV_TEXT\n":
                arquivoHTML.write(f'<textarea type="text" name="entrada{entrada}" id="entrada{entrada}"></textarea>\n</div>\n')
                entrada+=1
                espacos2[q] = 0
                tipo2[q] = "vazio"
                texto2[q] = "vazio"
                break
            if tipo2[q] == "DV_DATE_TIME\n":
                arquivoHTML.write(f'<input type="datetime-local" name="entrada{entrada}" id="entrada{entrada}"/>\n</div>\n')
                entrada+=1
                espacos2[q] = 0
                tipo2[q] = "vazio"
                texto2[q] = "vazio"
                break
            if tipo2[q] == "DV_DATE\n":
                arquivoHTML.write(f'<input type="date" name="entrada{entrada}" id="entrada{entrada}"/>\n</div>\n')
                entrada+=1
                espacos2[q] = 0
                tipo2[q] = "vazio"
                texto2[q] = "vazio"
                break
            if tipo2[q] == "DV_BOOLEAN\n":
                arquivoHTML.write(f'<input type="checkbox" value="1" name="entrada{entrada}" id="entrada{entrada}"/>\n</div>\n')
                entrada+=1
                espacos2[q] = 0
                tipo2[q] = "vazio"
                texto2[q] = "vazio"
                break
            if tipo2[q] == "DV_MULTIMEDIA\n":
                arquivoHTML.write(f'<input type="file" value="1" name="entrada{entrada}" id="entrada{entrada}"/>\n</div>\n')
                entrada+=1
                espacos2[q] = 0
                tipo2[q] = "vazio"
                texto2[q] = "vazio"
                break
            if tipo2[q] == "DV_TIME\n":
                arquivoHTML.write(f'<input type="time" value="1" name="entrada{entrada}" id="entrada{entrada}"/>\n</div>\n')
                entrada+=1
                espacos2[q] = 0
                tipo2[q] = "vazio"
                texto2[q] = "vazio"
                break
            if tipo2[q] == "DV_DURATION\n":
                arquivoHTML.write(f'<input type="number" value="1" name="entrada{entrada}" id="entrada{entrada}"/>\n</div>\n')
                entrada+=1
                espacos2[q] = 0
                tipo2[q] = "vazio"
                texto2[q] = "vazio"
                break

while len(sectionOn) > 1:
    arquivoHTML.write('</fieldset>\n')
    del sectionOn[len(sectionOn)-1]
arquivoHTML.write('</form>\n</div>\n</body>\n</html>')
arquivoHTML.close()