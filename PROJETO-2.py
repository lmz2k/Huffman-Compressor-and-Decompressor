import heapq
import os
import pickle
import timeit


def criarFrequencia(texto):
    frequencia = {}
    inicio = 0
    fim = 4
    frase = texto[inicio:fim]

    for i in range(int(len(texto)/4)):
        if frase in frequencia:
            frequencia[frase] += 1
        else:
            frequencia[frase] = 1
        inicio += 4
        fim += 4
        frase = texto[inicio:fim]
    #print(frequencia)
    lista = []
    for i in frequencia:
        dado = (frequencia[i], i)
        lista.append(dado)
    return lista

def criarArvore(Frequencia_das_letras):
        arvore = []
        for i in Frequencia_das_letras:
            heapq.heappush(arvore, [i])
        while (len(arvore) > 1):
            filho_esquerda = heapq.heappop(arvore)
            filho_direita = heapq.heappop(arvore)
            frequenciaEsquerda, letraEsquerda = filho_esquerda[0]
            frequenciaDireita, letraDireita = filho_direita[0]
            frequencia = frequenciaEsquerda + frequenciaDireita
            letras = ''.join(sorted(letraEsquerda + letraDireita))
            no = [(frequencia, letras), filho_esquerda, filho_direita]
            heapq.heappush(arvore, no)

        return arvore.pop()

def criar_codigo_mapa(arvore):
        codeMap = {}
        percorrer_Arvore(arvore, codeMap, '')
        return codeMap

def percorrer_Arvore(arvore, codeMap, codigo):
        if (len(arvore) == 1):
            frequencia, letras = arvore[0]
            codeMap[letras] = codigo
        else:
            no, filho_esquerda, filho_direita = arvore
            percorrer_Arvore(filho_esquerda, codeMap, codigo + '0')
            percorrer_Arvore(filho_direita, codeMap, codigo + '1')

def codificacao(mapCode, mensagem):
        codeMap = mapCode
        string = ''
        inicio = 0
        fim = 4
        frase = mensagem[inicio:fim]
        for i in range(int(len(mensagem)/4)):
            if frase in mensagem:
                string += codeMap[frase]

            inicio += 4
            fim += 4
            frase = mensagem[inicio:fim]

        return string

def pad_textoCodificar(textoCodificado):
        extra_padding = 8 - len(textoCodificado) % 8
        for i in range(extra_padding):
            textoCodificado += "0"

        padded_info = "{0:08b}".format(extra_padding)
        textoCodificado = padded_info + textoCodificado

        return textoCodificado

def obter_array_byte(padded_text):

        b = bytearray()
        for i in range(0, len(padded_text), 8):
            byte = padded_text[i:i + 8]
            b.append(int(byte, 2))
        return b

def remove_padding(padded_encoded_text):
    padded_info = padded_encoded_text[:8]
    extra_padding = int(padded_info, 2)

    padded_encoded_text = padded_encoded_text[8:]
    encoded_text = padded_encoded_text[:-1 * extra_padding]

    return encoded_text


def decodificacao(mensagemCodificada, arvoreFrequencias):

    codeTree = arvoreCompleta = arvoreFrequencias
    letrasDecodidicada = []

    for digito in mensagemCodificada:
        if (digito == '0'):
            codeTree = codeTree[1]
        else:
            codeTree = codeTree[2]
        if len(codeTree) == 1:
            frequencia, letras = codeTree[0]
            letrasDecodidicada.append(letras)
            codeTree = arvoreCompleta

    return ''.join(letrasDecodidicada)




exec = True
while True:
    diretorio = "C:\Games/"
    if exec == False:
        break
    print('ESCOLHA UMA OPÇÃO: ')
    print('1 - COMPACTAR UM ARQUIVO ')
    print('2 - DESCOMPACTAR UM ARQUIVO ')
    print('3 - ENCERRAR PROGRAMA')
    escolha = input()

    if escolha == '1':
            while True:

                print('DIGITE NOME DO ARQUIVO QUE DESEJA COMPACTAR (EX: musica.mp3):')
                nomeArquivo = input()
                arquivo = diretorio + nomeArquivo
                if os.path.isfile(arquivo):
                    break
                else:
                    print('ERRO!!!, VERIFIQUE SE O ARQUIVO É EXISTENTE NO DIRETORIO E SE A DIGITAÇÃO ESTA CORRETA!')



            filename, file_extension = os.path.splitext(arquivo)
            EX = file_extension
            ArquivoSaida = filename + ".pequeninitoPT1"
            ArquivoSaida2 = filename + ".pequeninitoPT2"
            inicio = timeit.default_timer()
            print('COMPACTANDO O ARQUIVO ({})...'.format(filename[9:]))
            with open(arquivo, 'rb') as file, open(ArquivoSaida, 'wb') as output1, open(ArquivoSaida2, 'wb') as fp:
                texto = file.read().hex()
                frequencia = criarFrequencia(texto)
                arvoreFrequencias = criarArvore(frequencia)
                pickle.dump(arvoreFrequencias, fp)
                mapCode = criar_codigo_mapa(arvoreFrequencias)
                textoCodificado = codificacao(mapCode, texto)
                padded_text = pad_textoCodificar(textoCodificado)

                b = obter_array_byte(padded_text)
                output1.write(bytes(b))
                #print(ArquivoSaida)

                print("\nARQUIVO COMPACTADO COM SUCESSO!")
                fim = timeit.default_timer()
            print('Tempo de execução da compactação: {}'.format(fim - inicio))
            print('DIGITE QUALQUER TECLA PARA UTILIZAR PROGRAMA NOVAMENTE, OU DIGITE "SAIR" PARA ENCERRAR!!!')
            esc = input()
            if esc == 'SAIR' or esc == 'sair':
                break


    elif(escolha == '2'):

        while True:
            print('DIGITE NOME DO ARQUIVO QUE DESEJA DESCOMPACTAR: ')
            nomeArquivo = input()
            arqCompact1 = diretorio + nomeArquivo + '.pequeninitoPT1'
            arqCompact2 = diretorio + nomeArquivo + '.pequeninitoPT2'
            if os.path.isfile(arqCompact1) and os.path.isfile(arqCompact2):
                break
            else:
                print('ERRO!!!, VERIFIQUE SE OS ARQUIVOS COMPACTADOS É EXISTENTE NO DIRETORIO E SE A DIGITAÇÃO ESTA CORRETA!')


        print('DIGITE A EXTENSAO ORIGINAL DO ARQUIVO: ')
        ext = input()
        filename,file_extension = os.path.splitext(arqCompact1)
        output_path = filename + "_descompactado." + ext
        inicio = timeit.default_timer()
        print('DESCOMPACTANDO O ARQUIVO ({})....'.format(filename[9:]))
        with open(arqCompact1, 'rb') as file, open(output_path, 'wb') as output, open(arqCompact2, 'rb') as fp:
            bit_string = ""
            byte = file.read(1)
            while (len(byte) > 0):
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)
            texto_codificado = remove_padding(bit_string)
            FREQ = pickle.load(fp)
            texto_descompactado = decodificacao(texto_codificado, FREQ)
            b = bytearray.fromhex(texto_descompactado)
            output.write(b)
            #print(b)

            print("\nARQUIVO DESCOMPACTADO COM SUCESSO!!!")
            fim = timeit.default_timer()
            print('Tempo de execução da descompactação : {}'.format(fim - inicio))
            print('DIGITE QUALQUER TECLA PARA UTILIZAR PROGRAMA NOVAMENTE, OU DIGITE "SAIR" PARA ENCERRAR!!!')
            esc = input()
            if esc == 'SAIR' or esc == 'sair':
                break

    elif(escolha == '3'):
        exec = False
    else:
        print('ESCOLHA UMA OPÇÃO VALIDA!')