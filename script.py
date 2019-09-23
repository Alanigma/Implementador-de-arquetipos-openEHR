vez=1
id = 0
idstring = "at0000"
arquivo = open('fakeADL.txt','w')
arquivo.close()
arquivoJS = open('meuscript.js','w')
arquivo.close()
arquivoOrdem = open('ordem.txt','w')
arquivoOrdem.close()
maior = int(input("Qual é o maior at? Exemplo: se for at0050, digite 50:"))
tamanho = int(input("Tamanho do título principal (quanto maior o valor, menor o tamanho): "))
tamanhoDaqui = 3
bugados = []

leitura = open('adl.txt', 'r')
escrita = open('adl2.txt', 'w')
for linha in leitura:
    if 'TERMINOLOGY_ID' not in linha:
        escrita.write(linha)
escrita.close()
leitura.close()

while True:
    contador = 0
    if contador < 1:
        encontrado = False
        arquivoADL = open('adl2.txt', 'r')
        comecar = False
        for linha in arquivoADL:
            if linha == "definition\n":
                comecar = True
            if comecar == True:
                linha = linha.rstrip()
                arquivo = open('fakeADL.txt', 'a')
                if vez == 3:
                    linha = str(linha)
                    linha = linha.replace('text = <\"', '')
                    linha = linha.replace('\">', '')
                    linha = linha.strip(" ")
                    linha = linha.strip("\t")
                    arquivo.write(linha+"\n")
                    vez = 1
                else:
                    if contador >= 2: break
                    if idstring in linha:
                        contador += 1
                        encontrado = True
                        contadorletra = 0
                        if vez==1:
                           palavra = ''
                           for letra in linha:
                               if letra == ' ':
                                   contadorletra+=1
                               elif letra == '\t':
                                   contadorletra+=3
                               else:
                                   break
                           linha = linha.split()
                           parar = False
                           arquivo.write(str(contadorletra)+'\n')
                           for letra in linha[0]:
                               if letra == '[':
                                   parar = True
                               if parar == False:
                                   palavra += letra
                           pegar1 = 0
                           for letra in linha[3]:
                               if pegar1==1:
                                   if letra.isnumeric():
                                       palavra += letra
                                   if letra == '*':
                                       palavra += letra
                                   if letra == '}':
                                       pegar1 = 2
                               if pegar1 == -1:
                                   if letra.isnumeric():
                                       palavra+=letra
                                   else:
                                       pegar1 = 1
                                       palavra += ' '
                               if letra == '{' and pegar1 != 2:
                                   pegar1 = -1
                                   palavra += ' '
                           arquivo.write(palavra+"\n")
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
    linha = linha.replace('\n','')
    while len(texto) in bugados:
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
comecar = False
arquivoOrdem = open('ordem.txt','a')
arquivoADL = open('adl2.txt','r')
for linha in arquivoADL:
    palavra = ''
    if linha == "definition\n":
        comecar = True
    if comecar == True and ignorar == False:
        linha = linha.rstrip()
        pegar=False
        linha.split()
        try:
            if '[at' in linha:
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
arquivoHTML = open('form.html','w')
arquivoHTML.close()

sectionOn=[0]
id=0
nome=0
primeiraSection = 0

arquivoHTML = open('form.html','a')
arquivoHTML.write('<!DOCTYPE html>\n<html>\n<head>\n<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/components/form.css"/>\n'
                  '<script src="http://code.jquery.com/jquery-1.11.3.min.js"></script>\n'
                  '<script type="text/javascript" src="meuscript.js"></script>\n'
                  '</head>\n<body>\n<div class="container">\n<form class="ui form ui grid">\n')

for c in range(0, len(tipo2)):
    if tipo2[c].split()[0] == "COMPOSITION":
        while len(sectionOn) > 1:
            arquivoHTML.write('</fieldset>\n')
            del sectionOn[len(sectionOn) - 1]
        arquivoHTML.write(f'<h{tamanho}>\n{texto2[c]}</h{tamanho}>\n')

    if tipo2[c].split()[0] == "SECTION":
        if sectionOn[len(sectionOn) - 1] == 0:
            tamanhoDaqui = len(sectionOn) + tamanho
            primeiraSection = espacos2[c]
            arquivoHTML.write(f'<fieldset class="field four wide column">\n<legend>\n<h{tamanhoDaqui}>\n{texto2[c]}</h{tamanhoDaqui}>\n</legend>\n')
            sectionOn.append(espacos2[c])
        elif espacos2[c]==primeiraSection:
            while espacos2[c] < sectionOn[len(sectionOn) - 1]:
                arquivoHTML.write(f'</fieldset>\n')
                del sectionOn[len(sectionOn) - 1]
            if espacos2[c] == sectionOn[len(sectionOn) - 1]:
                tamanhoDaqui = len(sectionOn) + tamanho - 1
                arquivoHTML.write(f'</fieldset>\n<fieldset class="field four wide column">\n<legend>\n<h{tamanhoDaqui}>\n{texto2[c]}</h{tamanhoDaqui}>\n</legend>\n')
        elif espacos2[c]<primeiraSection:
            primeiraSection = espacos2[c]
            while espacos2[c] < sectionOn[len(sectionOn) - 1]:
                arquivoHTML.write(f'</fieldset>\n')
                del sectionOn[len(sectionOn) - 1]
            if sectionOn[len(sectionOn) - 1] == 0:
                tamanhoDaqui = len(sectionOn) + tamanho
                arquivoHTML.write(f'</fieldset>\n<fieldset class="field four wide column">\n<legend>\n<h{tamanhoDaqui}>\n{texto2[c]}</h{tamanhoDaqui}>\n</legend>\n')
                sectionOn.append(espacos2[c])
        elif espacos2[c] > sectionOn[len(sectionOn) - 1]:
            tamanhoDaqui = len(sectionOn) + tamanho
            arquivoHTML.write(f'<fieldset>\n<legend>\n<h{tamanhoDaqui}>\n{texto2[c]}</h{tamanhoDaqui}>\n</legend>\n')
            sectionOn.append(espacos2[c])
        elif espacos2[c] == sectionOn[len(sectionOn) - 1]:
            tamanhoDaqui = len(sectionOn) + tamanho-1
            arquivoHTML.write(f'</fieldset>\n<fieldset>\n<legend>\n<h{tamanhoDaqui}>\n{texto2[c]}</h{tamanhoDaqui}>\n</legend>\n')
        while espacos2[c] < sectionOn[len(sectionOn) - 1]:
            arquivoHTML.write(f'</fieldset>\n')
            del sectionOn[len(sectionOn)-1]
            if espacos2[c] == sectionOn[len(sectionOn) - 1]:
                tamanhoDaqui = len(sectionOn) + tamanho - 1
                arquivoHTML.write(f'</fieldset>\n<fieldset>\n<legend>\n<h{tamanhoDaqui}>\n{texto2[c]}</h{tamanhoDaqui}>\n</legend>\n')

    if tipo2[c].split()[0] == "ELEMENT":
        arquivoElemento = open('Elemento.html', 'w')
        arquivoElemento.close()
        arquivoElemento2 = open('Elemento2.html', 'w')
        arquivoElemento2.close()
        arquivoJS = open('meuscript.js', 'a')
        arquivoElemento = open('Elemento.html', 'a')
        arquivoElemento2 = open('Elemento2.html', 'a')
        arquivoElemento.write(f'<div class="field fifteen wide column" id="id{id}">\n')
        idBotao=id
        id+=1
        arquivoElemento.write(f'<label for="id{id}"><h{tamanhoDaqui + 1}>\n{texto2[c]}</h{tamanhoDaqui + 1}></label>\n')
        arquivoElemento2.write(f'<label for="id\'+id+\'"><h{tamanhoDaqui + 1}>\n{texto2[c]}</h{tamanhoDaqui + 1}></label>\n')
        for q in range(0, len(tipo2)):
            if tipo2[q].split()[0] == "DV_TEXT":
                arquivoElemento.write(f'<input class="field eleven wide column" type="text" name="nome{nome}" id="id{id}">\n</div>\n')
                arquivoElemento2.write(f'<input class="field eleven wide column" type="text" name="nome\'+nome+\'" id="id\'+id+\'">\n</div>\n')
                id+=1
                espacos2[q] = 0
                tipo2[q] = "vazio"
                texto2[q] = "vazio"
                break
            if tipo2[q].split()[0] == "DV_DATE_TIME":
                arquivoElemento.write(f'<input class="field eleven wide column" type="datetime-local" name="nome{nome}" id="id{id}"/>\n</div>\n')
                arquivoElemento2.write(f'<input class="field eleven wide column" type="datetime-local" name="nome\'+nome+\'" id="id\'+id+\'"/>\n</div>\n')
                id+=1
                espacos2[q] = 0
                tipo2[q] = "vazio"
                texto2[q] = "vazio"
                break
            if tipo2[q].split()[0] == "DV_DATE":
                arquivoElemento.write(f'<input class="field eleven wide column" type="date" name="nome{nome}" id="id{id}"/>\n</div>\n')
                arquivoElemento2.write(f'<input class="field eleven wide column" type="date" name="nome\'+nome+\'" id="id\'+id+\'"/>\n</div>\n')
                id+=1
                espacos2[q] = 0
                tipo2[q] = "vazio"
                texto2[q] = "vazio"
                break
            if tipo2[q].split()[0] == "DV_BOOLEAN":
                arquivoElemento.write(f'<input type="checkbox" value="1" name="nome{nome}" id="id{id}"/>\n</div>\n')
                arquivoElemento2.write(f'<input type="checkbox" value="1" name="nome\'+nome+\'" id="id\'+id+\'"/>\n</div>\n')
                id+=1
                espacos2[q] = 0
                tipo2[q] = "vazio"
                texto2[q] = "vazio"
                break
            if tipo2[q].split()[0] == "DV_MULTIMEDIA":
                arquivoElemento.write(f'<input class="field eleven wide column" type="file" name="nome{nome}" id="id{id}"/>\n</div>\n')
                arquivoElemento2.write(f'<input class="field eleven wide column" type="file" name="nome\'+nome+\'" id="id\'+id+\'"/>\n</div>\n')
                id+=1
                espacos2[q] = 0
                tipo2[q] = "vazio"
                texto2[q] = "vazio"
                break
            if tipo2[q].split()[0] == "DV_TIME":
                arquivoElemento.write(f'<input class="field eleven wide column" type="time" name="nome{nome}" id="id{id}"/>\n</div>\n')
                arquivoElemento2.write(f'<input class="field eleven wide column" type="time" name="nome\'+nome+\'" id="id\'+id+\'"/>\n</div>\n')
                id+=1
                espacos2[q] = 0
                tipo2[q] = "vazio"
                texto2[q] = "vazio"
                break
            if tipo2[q].split()[0] == "DV_DURATION" or tipo2[q] == "DV_QUANTITY":
                arquivoElemento.write(f'<input class="field eleven wide column" class="field eleven wide column" type="number" name="nome{nome}" id="id{id}"/>\n</div>\n')
                arquivoElemento2.write(f'<input class="field eleven wide column" class="field eleven wide column" type="number" name="nome\'+nome+\'" id="id\'+id+\'"/>\n</div>\n')
                id+=1
                espacos2[q] = 0
                tipo2[q] = "vazio"
                texto2[q] = "vazio"
                break
            if tipo2[q].split()[0] == "DV_PROPORTION":
                espacos2[q] = 0
                tipo2[q] = "vazio"
                texto2[q] = "vazio"
                for q2 in range(0, 11):
                    arquivoElemento.write('<div class="ui radio checkbox">\n')
                    arquivoElemento2.write('<div class="ui radio checkbox">\n')
                    arquivoElemento.write(f'<input class="field eleven wide column" type="radio" value="{q2}" name="nome{nome}" id="id{id}"/>\n<label for="id{id}">\n{q2}</label>\n</div>\n')
                    arquivoElemento2.write(f'<input class="field eleven wide column" type="radio" value="{q2}" name="nome\'+nome+\'" id="id\'+id+\'"/>\n<label for="id\'+id+\'">\n{q2}</label>\n</div>\n')
                    id += 1
                break
            if tipo2[q].split()[0] == "DV_CODED_TEXT":
                arquivoElemento.write(f'<select id="id{id}">\n')
                arquivoElemento2.write(f'<select id="id\'+id+\'">\n')
                id+=1
                arquivoElemento.write(f'<option value=""></option>\n')
                arquivoElemento2.write(f'<option value=""></option>\n')
                espacos2[q] = 0
                tipo2[q] = "vazio"
                texto2[q] = "vazio"
                for q2 in range(q + 1, len(tipo2)):
                    if tipo2[q2].split()[0] == "CODE_PHRASE":
                         arquivoElemento.write(f'<option value="{texto2[q2]}">{texto2[q2]}</option>\n')
                         arquivoElemento2.write(f'<option value="{texto2[q2]}">{texto2[q2]}</option>\n')
                         espacos2[q2] = 0
                         tipo2[q2] = "vazio"
                         texto2[q2] = "vazio"
                    else: break
                arquivoElemento.write('</select>\n')
                arquivoElemento.write('</div>\n')
                arquivoElemento2.write('</select>\n')
                arquivoElemento2.write('</div>\n')
                break
        arquivoElemento.close()
        arquivoElemento2.close()
        linhaID=id
        linhaNome=nome
        contador=0
        contadorNome=0

        arquivoHTML.write(f'<div class="field fifteen wide column" id="id{id-2}">\n')
        id += 1

        for vezes in range(int(tipo2[c].split()[1])):
            arquivoElemento = open('Elemento.html', 'r')
            for linha in arquivoElemento:
                if '<div' not in linha and '</div>' not in linha:
                    if f'id{linhaID}' in linha:
                        contador+=1
                    if contador == 2:
                        linhaID += 1
                        contador = 0
                    if f'id{linhaID-1}' in linha:
                        linha = linha.replace(f'id{linhaID-1}', f'id{linhaID+vezes-1}')
                    if f'nome{linhaNome}' in linha:
                        contadorNome+=1
                    if contadorNome == 2:
                        linhaNome += 1
                        contadorNome = 0
                    if f'nome{linhaNome-1}' in linha:
                        linha = linha.replace(f'nome{linhaNome-1}', f'nome{linhaNome+vezes-1}')
                    arquivoHTML.write(linha)
            arquivoElemento.close()
            id=linhaID+vezes
            nome=linhaNome+vezes
        arquivoHTML.write('</div>\n')
        arquivoElemento2 = open('Elemento2.html', 'r')
        if tipo2[c].split()[2] == "*" or tipo2[c].split()[2] > tipo2[c].split()[1]:
            arquivoJS.write(f'function funcao{idBotao}()' + '{'+f'\n$("#id{idBotao}").append(\'')
            for linha in arquivoElemento2:
                if '<div' not in linha and '</div>' not in linha:
                    linha = linha.replace('\n',' ')
                    arquivoJS.write(f'{linha}')
            arquivoJS.write('\');\nid+=1\nnome+=1\n}\n')
            arquivoHTML.write(f'<a style="color:white;background-color:grey;padding:3px" onclick="funcao{idBotao}()">Adicionar {texto2[c]}</a>\n')
        arquivoElemento2.close()
        nome+=1
        arquivoJS.close()

while len(sectionOn) > 1:
    arquivoHTML.write('</fieldset>\n')
    del sectionOn[len(sectionOn)-1]
arquivoJS = open('meuscript.js', 'a')
arquivoJS.write(f'id={id}\nnome={nome}\n')
arquivoJS.close()
arquivoHTML.write('<button type="submit">Enviar</button>\n</form>\n</div>\n</body>\n</html>')
arquivoHTML.close()