vez=1
id = 0
idstring = "at0000"
arquivo = open('teste.txt','w')
arquivo.close()
maior = int(input("Qual é o maior at? Exemplo: se for at0050, digite 50:"))

while True:
    contador = 0
    arquivoADL = open('adl.txt', 'r')
    for linha in arquivoADL:
        contador += 1
        if contador>20:
            linha = linha.rstrip()
            arquivo = open('teste.txt', 'a')

            if vez == 3:
                linha = str(linha)
                linha = linha.replace('text = <\"', '')
                linha = linha.replace('\">', '')
                linha = linha.strip(" ")
                arquivo.write(linha+"\n")
                vez = 1
            else:
                if idstring in linha:
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

#Geração de HTML
vez=1
espacos=[]
tipo=[]
texto=[]

arquivo = open('teste.txt', 'r')
for linha in arquivo:
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

arquivoHTML = open('index.html','w')
arquivoHTML.close()

sectionOn=[0]
entrada=0

arquivoHTML = open('index.html','a')
arquivoHTML.write('<!DOCTYPE html>\n<html>\n<head>\n<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/components/form.css"/>\n</head>\n<body>\n<div class="container">\n<form class="ui form ui grid">\n')

for c in range(0, len(tipo)):

    if tipo[c] == "COMPOSITION\n":
        while len(sectionOn) > 1:
            arquivoHTML.write('</fieldset>\n')
            del sectionOn[len(sectionOn) - 1]
        arquivoHTML.write(f'<h1>\n{texto[c]}</h1>\n')

    if tipo[c] == "SECTION\n":
        if espacos[c] > sectionOn[len(sectionOn)-1]:
            sectionOn.append(espacos[c])
            arquivoHTML.write(f'<fieldset>\n<legend>\n<h{len(sectionOn)}>\n{texto[c]}</h{len(sectionOn)}>\n</legend>\n')
        elif espacos[c] == sectionOn[len(sectionOn)-1]:
            arquivoHTML.write(f'</fieldset>\n<fieldset>\n<legend>\n<h{len(sectionOn)}>\n{texto[c]}</h{len(sectionOn)}>\n</legend>\n')
        while espacos[c] < sectionOn[len(sectionOn)-1]:
            arquivoHTML.write(f'</fieldset>\n')
            del sectionOn[len(sectionOn)-1]
            if espacos[c] == sectionOn[len(sectionOn)-1]:
                arquivoHTML.write(f'</fieldset>\n<fieldset>\n<legend>\n<h{len(sectionOn)}>\n{texto[c]}</h{len(sectionOn)}>\n</legend>\n')

    if tipo[c] == "ELEMENT\n":
        arquivoHTML.write(f'<div class="field four wide column">\n<label for="entrada{entrada}">\n{texto[c]}</label>\n')
        for q in range(0, len(tipo)):
            if tipo[q] == "DV_TEXT\n":
                arquivoHTML.write(f'<textarea type="text" name="entrada{entrada}" id="entrada{entrada}"></textarea>\n</div>\n')
                entrada+=1
                espacos[q] = 0
                tipo[q] = "vazio"
                texto[q] = "vazio"
                break
            if tipo[q] == "DV_DATE_TIME\n":
                arquivoHTML.write(f'<input type="datetime-local" name="entrada{entrada}" id="entrada{entrada}"/>\n</div>\n')
                entrada+=1
                espacos[q] = 0
                tipo[q] = "vazio"
                texto[q] = "vazio"
                break
            if tipo[q] == "DV_DATE\n":
                arquivoHTML.write(f'<input type="date" name="entrada{entrada}" id="entrada{entrada}"/>\n</div>\n')
                entrada+=1
                espacos[q] = 0
                tipo[q] = "vazio"
                texto[q] = "vazio"
                break
            if tipo[q] == "DV_BOOLEAN\n":
                arquivoHTML.write(f'<input type="checkbox" value="1" name="entrada{entrada}" id="entrada{entrada}"/>\n</div>\n')
                entrada+=1
                espacos[q] = 0
                tipo[q] = "vazio"
                texto[q] = "vazio"
                break
            if tipo[q] == "DV_MULTIMEDIA\n":
                arquivoHTML.write(f'<input type="file" value="1" name="entrada{entrada}" id="entrada{entrada}"/>\n</div>\n')
                entrada+=1
                espacos[q] = 0
                tipo[q] = "vazio"
                texto[q] = "vazio"
                break
            if tipo[q] == "DV_TIME\n":
                arquivoHTML.write(f'<input type="time" value="1" name="entrada{entrada}" id="entrada{entrada}"/>\n</div>\n')
                entrada+=1
                espacos[q] = 0
                tipo[q] = "vazio"
                texto[q] = "vazio"
                break
            if tipo[q] == "DV_DURATION\n":
                arquivoHTML.write(f'<input type="number" value="1" name="entrada{entrada}" id="entrada{entrada}"/>\n</div>\n')
                entrada+=1
                espacos[q] = 0
                tipo[q] = "vazio"
                texto[q] = "vazio"
                break

while len(sectionOn) > 1:
    arquivoHTML.write('</fieldset>\n')
    del sectionOn[len(sectionOn)-1]
arquivoHTML.write('</form>\n</div>\n</body>\n</html>')
arquivoHTML.close()