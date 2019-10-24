elementoAberto = False
modoOpcoes = False
id=0
nome=0
letras = []
letras2 = []
comecar = False
sectionOn=[0]
primeiraSection = 0
tamanho = int(input("Tamanho do título principal (quanto maior o valor, menor o tamanho): "))
tamanhoDaqui = 0+tamanho

arquivoHTML = open('form.html','w')
arquivoHTML.write('<!DOCTYPE html>\n<html>\n<head>\n<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/components/form.css"/>\n'
                  '<script src="http://code.jquery.com/jquery-1.11.3.min.js"></script>\n'
                  '<script type="text/javascript" src="meuscript.js"></script>\n'
                  '</head>\n<body>\n<div class="container">\n<form class="ui form ui grid">\n')
arquivoHTML.close()
arquivoADL = open('adl.txt', 'r')

for linha in arquivoADL:
    arquivoHTML = open('form.html', 'a')
    espacos = 0
    palavra = ""
    deletar = True
    for c in range(len(letras)):
        del letras[0]
    for c in range(len(letras2)):
        del letras2[0]
    if linha == "definition\n":
        comecar = True
    if comecar == True:
        linha = linha.rstrip()
        for letra in linha:
            if letra != " ": break
            else: espacos += 1
        linha = linha.strip()
        if "ontology" == linha: break

        if "COMPOSITION" in linha:
            if modoOpcoes == True:
                arquivoHTML.write('</select>\n')
                modoOpcoes = False
            if elementoAberto == True:
                arquivoHTML.write('</div>\n')
                elementoAberto = False

            for letra in linha:
                letras.append(letra)
            for c in range(len(letras)):
                if deletar == False:
                    letras2.append(letras[c])
                if (letras[c] == " " or letras[c] == "\t") and letras[c-1] == "-" and letras[c-2] == "-":
                    deletar = False
            texto = ''.join(map(str, letras2))

            while len(sectionOn) > 1:
                arquivoHTML.write('</fieldset>\n')
                del sectionOn[len(sectionOn) - 1]
            arquivoHTML.write(f'<h{tamanho}>\n{texto}</h{tamanho}>\n')

        if "SECTION" in linha:
            if modoOpcoes == True:
                arquivoHTML.write('</select>\n')
                modoOpcoes = False
            if elementoAberto == True:
                arquivoHTML.write('</div>\n')
                elementoAberto = False

            for letra in linha:
                letras.append(letra)
            for c in range(len(letras)):
                if deletar == False:
                    letras2.append(letras[c])
                if (letras[c] == " " or letras[c] == "\t") and letras[c-1] == "-" and letras[c-2] == "-":
                    deletar = False

            texto = ''.join(map(str, letras2))

            if sectionOn[len(sectionOn) - 1] == 0:
                tamanhoDaqui = len(sectionOn) + tamanho
                primeiraSection = espacos
                arquivoHTML.write(
                    f'<fieldset class="field four wide column">\n<legend>\n<h{tamanhoDaqui}>\n{texto}</h{tamanhoDaqui}>\n</legend>\n')
                sectionOn.append(espacos)
            elif espacos == primeiraSection:
                while espacos < sectionOn[len(sectionOn) - 1]:
                    arquivoHTML.write(f'</fieldset>\n')
                    del sectionOn[len(sectionOn) - 1]
                if espacos == sectionOn[len(sectionOn) - 1]:
                    tamanhoDaqui = len(sectionOn) + tamanho - 1
                    arquivoHTML.write(
                        f'</fieldset>\n<fieldset class="field four wide column">\n<legend>\n<h{tamanhoDaqui}>\n{texto}</h{tamanhoDaqui}>\n</legend>\n')
            elif espacos < primeiraSection:
                primeiraSection = espacos
                while espacos < sectionOn[len(sectionOn) - 1]:
                    arquivoHTML.write(f'</fieldset>\n')
                    del sectionOn[len(sectionOn) - 1]
                if sectionOn[len(sectionOn) - 1] == 0:
                    tamanhoDaqui = len(sectionOn) + tamanho
                    arquivoHTML.write(
                        f'</fieldset>\n<fieldset class="field four wide column">\n<legend>\n<h{tamanhoDaqui}>\n{texto}</h{tamanhoDaqui}>\n</legend>\n')
                    sectionOn.append(espacos)
            elif espacos > sectionOn[len(sectionOn) - 1]:
                tamanhoDaqui = len(sectionOn) + tamanho
                arquivoHTML.write(
                    f'<fieldset>\n<legend>\n<h{tamanhoDaqui}>\n{texto}</h{tamanhoDaqui}>\n</legend>\n')
                sectionOn.append(espacos)
            elif espacos == sectionOn[len(sectionOn) - 1]:
                tamanhoDaqui = len(sectionOn) + tamanho - 1
                arquivoHTML.write(
                    f'</fieldset>\n<fieldset>\n<legend>\n<h{tamanhoDaqui}>\n{texto}</h{tamanhoDaqui}>\n</legend>\n')
            while espacos< sectionOn[len(sectionOn) - 1]:
                arquivoHTML.write(f'</fieldset>\n')
                del sectionOn[len(sectionOn) - 1]
                if espacos == sectionOn[len(sectionOn) - 1]:
                    tamanhoDaqui = len(sectionOn) + tamanho - 1
                    arquivoHTML.write(
                        f'</fieldset>\n<fieldset>\n<legend>\n<h{tamanhoDaqui}>\n{texto}</h{tamanhoDaqui}>\n</legend>\n')

        if "ELEMENT" in linha:
            if modoOpcoes == True:
                arquivoHTML.write('</select>\n')
                modoOpcoes = False
            if elementoAberto == True:
                arquivoHTML.write('</div>\n')
                elementoAberto = False

            elementoAberto = True
            for letra in linha:
                letras.append(letra)
            for c in range(len(letras)):
                if deletar == False:
                    letras2.append(letras[c])
                if (letras[c] == " " or letras[c] == "\t") and letras[c-1] == "-" and letras[c-2] == "-":
                    deletar = False
            texto = ''.join(map(str, letras2))

            arquivoHTML.write(f'<div class="field fifteen wide column" id="id{id}">\n')
            id += 1
            arquivoHTML.write(f'<label for="id{id}"><h{tamanhoDaqui + 1}>\n{texto}</h{tamanhoDaqui + 1}></label>\n')

        if "DV_TEXT" in linha:
            if modoOpcoes == True:
                arquivoHTML.write('</select>\n')
                modoOpcoes = False

            arquivoHTML.write(f'<input class="field eleven wide column" type="text" name="nome{nome}" id="id{id}">\n</div>\n')
            elementoAberto = False
            id += 1
            nome += 1

            if elementoAberto == True:
                arquivoHTML.write('</div>\n')
                elementoAberto = False

        if "DV_DATE_TIME" in linha:
            if modoOpcoes == True:
                arquivoHTML.write('</select>\n')
                modoOpcoes = False

            arquivoHTML.write(f'<input class="field eleven wide column" type="datetime-local" name="nome{nome}" id="id{id}"/>\n</div>\n')
            elementoAberto = False
            id += 1
            nome += 1

            if elementoAberto == True:
                arquivoHTML.write('</div>\n')
                elementoAberto = False

        if "DV_DATE" in linha:
            if modoOpcoes == True:
                arquivoHTML.write('</select>\n')
                modoOpcoes = False

            arquivoHTML.write(f'<input class="field eleven wide column" type="date" name="nome{nome}" id="id{id}"/>\n</div>\n')
            elementoAberto = False
            id += 1
            nome += 1

            if elementoAberto == True:
                arquivoHTML.write('</div>\n')
                elementoAberto = False

        if "DV_BOOLEAN" in linha:
            if modoOpcoes == True:
                arquivoHTML.write('</select>\n')
                modoOpcoes = False

            arquivoHTML.write(f'<input type="checkbox" value="1" name="nome{nome}" id="id{id}"/>\n</div>\n')
            elementoAberto = False
            id += 1
            nome += 1

            if elementoAberto == True:
                arquivoHTML.write('</div>\n')
                elementoAberto = False

        if "DV_MULTIMEDIA" in linha:
            if modoOpcoes == True:
                arquivoHTML.write('</select>\n')
                modoOpcoes = False

            arquivoHTML.write(f'<input class="field eleven wide column" type="file" name="nome{nome}" id="id{id}"/>\n</div>\n')
            elementoAberto = False
            id += 1
            nome += 1

            if elementoAberto == True:
                arquivoHTML.write('</div>\n')
                elementoAberto = False

        if "DV_DURATION" in linha or "DV_QUANTITY" in linha:
            if modoOpcoes == True:
                arquivoHTML.write('</select>\n')
                modoOpcoes = False

            arquivoHTML.write(f'<input class="field eleven wide column" class="field eleven wide column" type="number" name="nome{nome}" id="id{id}"/>\n</div>\n')
            elementoAberto = False
            id += 1
            nome += 1

            if elementoAberto == True:
                arquivoHTML.write('</div>\n')
                elementoAberto = False

        if "DV_PROPORTION" in linha:
            if modoOpcoes == True:
                arquivoHTML.write('</select>\n')
                modoOpcoes = False

            for q in range(0, 11):
                arquivoHTML.write('<div class="ui radio checkbox">\n')
                arquivoHTML.write(f'<input type="radio" value="{q}" name="nome{nome}" id="id{id}"/>\n<label for="id{id}">\n{q}</label>\n</div>\n')
                id += 1
            nome += 1

            if elementoAberto == True:
                arquivoHTML.write('</div>\n')
                elementoAberto = False

        if "DV_CODED_TEXT" in linha:
            if modoOpcoes == True:
                arquivoHTML.write('</select>\n')
                modoOpcoes = False

            arquivoHTML.write(f'<select id="id{id}">\n')
            arquivoHTML.write(f'<option value=""></option>\n')
            modoOpcoes = True
            id += 1

        if "CODE_PHRASE" in linha:
            arquivoHTML.write(f'<option value="{texto}">{texto}</option>\n')

    arquivoHTML.close()
arquivoHTML = open('form.html', 'a')
if modoOpcoes == True:
    arquivoHTML.write('</select>\n')
    modoOpcoes = False
if elementoAberto == True:
    arquivoHTML.write('</div>\n')
    elementoAberto = False
while len(sectionOn) > 1:
    arquivoHTML.write('</fieldset>\n')
    del sectionOn[len(sectionOn)-1]
arquivoHTML.write('<button type="submit">Enviar</button>\n</form>\n</div>\n</body>\n</html>')
arquivoHTML.close()
arquivoADL.close()