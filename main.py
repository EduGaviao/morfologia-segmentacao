#===============================================================================
# Trabalho 3
#-------------------------------------------------------------------------------
# Autor: Eduarda Simonis Gavião
# UNICAMP
#===============================================================================
# Importando bibliotecas
import statistics
import sys
import numpy as np
import cv2
import os


# imagem
IMAGEM_OBJETO =  'objetos.pbm'
IMAGEM_TEXTO = 'texto1.pbm'

#parametros de componentes conexos
NEGATIVO = True


#Declaração dos elementos estruturantes para objetos
Kernel1= np.ones((1,100),np.uint8) #elemento estruturante de 1 pixel de altura e 100 pixels de largura
Kernel2= np.ones((200,1),np.uint8) #elemento estruturante de 200 pixels de altura e 1 pixel de largura
Kernel3= np.ones((1,30),np.uint8) #elemento estruturante de 1 pixel de altura e 30 pixels de largura

#Declaração do elemento estruturante para textos
Kernel4= np.ones((3,3),np.uint8) 

#Função de dilatação 
def dilatacao(img,kernel): 
   img_dilation=cv2.dilate(img, kernel, iterations=1) # dilatacao via opencv

   #Para salvar a imagem basta descomentar as linhas abaixo
   #filename='dilatacao2.png'
   #cv2.imwrite(filename, img_dilation) 
   
   return(img_dilation)

#Função de erosão 
def erosao(img,kernel): 
   img_erosion=cv2.erode(img, kernel, iterations=1) # erosao via opencv

   #Para salvar a imagem basta descomentar as linhas abaixo
   #filename='erode.png'
   #cv2.imwrite(filename, img_erosion)
   return(img_erosion)

#função de fechamento (processo requerido nos passos 2 e 4 do trabalho)
def fechamentoManual(img,k): # dilatação seguida de erosão
    ## Processo manual realizado
    img_dilatacao= dilatacao(img,k)
    img_final= erosao(img_dilatacao,k)
    
    #Para salvar a imagem basta descomentar as linhas abaixo
    #filename='erosao2.png'
    #cv2.imwrite(filename, img_final)

    return(img_final)

#Função de intersecção
def interseccaoAND(img,k1,k2): 
   #Aplicação da erosão com ambos elementros estruturantes
   img_erosion1= fechamentoManual(img,k1)
   img_erosion2= fechamentoManual(img,k2)
   
   #Processo de a intersecção
   img_AND = cv2.bitwise_and(img_erosion1, img_erosion2)
   
   #Para salvar a imagem basta descomentar as linhas abaixo
   #filename='AND.png'
   #cv2.imwrite(filename, img_AND)

   return(img_AND)

#contagem de conexos por meio dos contornos
def conexos(img,original):
    
    componetes,_ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.RETR_EXTERNAL = conta apenas os contornos externos
    
    desenho= cv2.drawContours(original, componetes, -1, (255,0,0), 4)#desenha os contornos na copia da imagem original
    
    area_m=[cv2.contourArea(contador) for contador in componetes]#área dos contornos fechados
    
    mediana=statistics.median(area_m) #mediana das áreas do contorno
    
    count = 0
    for i in range(len(componetes)): #for para os contornos do componetes
        area = cv2.contourArea(componetes[i]) #acha a área de cada contorno
        if area >mediana: #compara com a área mediana, se for maior, que dizer que tem mais de um componente 
            count += round(area/mediana) #faz a divisão da área pela mediana para estimar a quantidade de componentes
        else: #caso contrário
            count += 1 #soma mais um 
            
    
    print ('Elementos Encontrados:',count) #printa o número de componetes
    cv2.imshow("Detectados", desenho)#mostra a imagem com contornos 

    #Para salvar a imagem basta descomentar as linhas abaixo
    filename='bordas.png'
    cv2.imwrite(filename, desenho)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def extraiTexto(img,original):
    #primeiro se identifica constornos menores, tais como números e letras
    letras,_ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.RETR_EXTERNAL = conta apenas os contornos externos
    
    desenho= cv2.drawContours(original, letras, -1, (255,0,0), 2)#desenha os contornos encontras na copia da imagem original
    
    area_m=[cv2.contourArea(contador) for contador in letras] #área dos contornos fechados
    
    mediana=statistics.median(area_m) #mediana das áreas do contorno
    
    count = 0
    for i in range(len(letras)): #for para os contornos do letras
        area = cv2.contourArea(letras[i]) #acha a área de cada contorno
        if area >mediana: #compara com a área mediana, se for maior, que dizer que tem mais de um componente 
            count += round(area/mediana) #faz a divisão da área pela mediana para estimar a quantidade de componentes
        else: #caso contrário
            count += 1 #soma mais um 
            
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7)) #cria um elemento estruturante para realizar o fechamento da imagem
 
    # Aplica dilatação na imagem
    close=fechamentoManual(img,rect_kernel)
 
    # Encontra os contornos das palavras
    contours, hierarchy = cv2.findContours(close, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
     
        # Desenha retângulos na imagem original
        rect = cv2.rectangle(original, (x, y), (x + w, y + h), (0, 255, 0), 4)

    print ('Letras Encontradas:',count) #printa o número de letras
    print ('Palavras Encontrados:',len(contours)) #printa o número de palvras, ou bloco de palavras encontradas
    cv2.imshow("Letras, e Blocos encontrados", desenho) #mostra a imagem de letras e blocos de palavras encontrados
    
    #Para salvar a imagem basta descomentar as linhas abaixo
    #filename='palavras2.png'
    #cv2.imwrite(filename, desenho)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main ():

    print('Prática 3- Operações Morfológicas')
    print('Deseja realizar a operação em que componentes?')
    print('Objetos - 1')
    print('Textos - 2')
    print('Sair - 0')
    
    op_1 = input("Indique a operação ")

    if op_1 == "1":
        os.system('cls')
        print('Escolha um dos métodos de Morfologia:')
        print('Dilatação - 1')
        print('Erosão - 2')
        print('Fechamento - 3')
        print('Intersecção - 4')
        print('Contagem de Componentes Conexos - 5')
        print('Sair - 0')
        op = input("Indique a operação ")
        #tratamento de opções
        if op == "1":
            img = cv2.imread (IMAGEM_OBJETO,cv2.IMREAD_GRAYSCALE)
            if img is None:
                print ('Erro abrindo a imagem.\n')
                sys.exit () 
            
            # Segmenta a imagem, quando o fundo é branco
            #if NEGATIVO:
            #   img = 255 - img

            # para mudar o elemento estruturante basta trocar o número final da variável "Kernel" para (1 ou 2)
            imgDilatation=dilatacao(img,Kernel2)    
            cv2.imshow("Dilatacao",imgDilatation)
            cv2.imshow("Original",img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        elif op =="2":
            img = cv2.imread (IMAGEM_OBJETO,cv2.IMREAD_GRAYSCALE)
            if img is None:
                print ('Erro abrindo a imagem.\n')
                sys.exit ()
            
            # Segmenta a imagem, quando o fundo é branco
            #if NEGATIVO:
            #   img = 255 - img
                
            # para mudar o elemento estruturante basta trocar o número final da variável "Kernel" para (1 ou 2)     
            imgErosion=erosao(img,Kernel1)    
            cv2.imshow("Erosao",imgErosion)
            cv2.imshow("Original",img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        elif op == "3":
            img = cv2.imread (IMAGEM_OBJETO,cv2.IMREAD_GRAYSCALE)
            if img is None:
                print ('Erro abrindo a imagem.\n')
                sys.exit ()
            
            # Segmenta a imagem, quando o fundo é branco
            #if NEGATIVO:
            #   img = 255 - img

            close_manual= fechamentoManual(img,Kernel2)  
            cv2.imshow("Erosao apos dilatacao (Fechamento)",close_manual)

            # O mesmo processo pode ser realizado via open cv
            closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, Kernel2)
            cv2.imshow("Resultado obtido com fechamento do OpenCV",closing)

            cv2.imshow("Original",img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


        elif op == "4":
            img = cv2.imread (IMAGEM_OBJETO,cv2.IMREAD_GRAYSCALE)
            if img is None:
                print ('Erro abrindo a imagem.\n')
                sys.exit ()

            # Segmenta a imagem, quando o fundo é branco
            #if NEGATIVO:
            #   img = 255 - img
            img_AND= interseccaoAND(img,Kernel1,Kernel2)

            cv2.imshow("Interseccao das Erosoes",img_AND)
            cv2.imshow("Original",img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        elif op == "5":
            img = cv2.imread (IMAGEM_OBJETO,cv2.IMREAD_GRAYSCALE)
            img_color = cv2.imread (IMAGEM_OBJETO,cv2.IMREAD_COLOR) #passagem da imagem para aceitar contorno colorido
            if img is None:
                print ('Erro abrindo a imagem.\n')
                sys.exit ()
            median = cv2.medianBlur(img,19) #retirando ruídos
            
            # Segmenta a imagem, quando o fundo é branco
            #if NEGATIVO:
            #   median = 255 - median
            
            img_AND= interseccaoAND(median,Kernel1,Kernel2)    
            fechamento=fechamentoManual(img_AND,Kernel3)     
            

            conexos(fechamento,img_color)
            


        else: 
            print('Fim da Execução')
        
    if op_1 == "2":
        os.system('cls')
        print('Escolha um dos métodos de Morfologia:')
        print('Dilatação - 1')
        print('Erosão - 2')
        print('Fechamento - 3')
        print('Intersecção - 4')
        print('Contagem de Componentes Conexos - 5')
        print('Sair - 0')
        op = input("Indique a operação ")
        #tratamento de opções
        if op == "1":
            img = cv2.imread (IMAGEM_TEXTO,cv2.IMREAD_GRAYSCALE)
            if img is None:
                print ('Erro abrindo a imagem.\n')
                sys.exit () 

            # Segmenta a imagem, pois em imagens de textos o fundo geralmente é branco
            if NEGATIVO:
               img = 255 - img

            imgDilatation=dilatacao(img,Kernel4)    
            cv2.imshow("Dilatacao",imgDilatation)
            cv2.imshow("Original",img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        elif op =="2":
            img = cv2.imread (IMAGEM_TEXTO,cv2.IMREAD_GRAYSCALE)
            if img is None:
                print ('Erro abrindo a imagem.\n')
                sys.exit ()
            # Segmenta a imagem, pois em imagens de textos o fundo geralmente é branco
            if NEGATIVO:
               img = 255 - img

            imgErosion=erosao(img,Kernel4)    
            cv2.imshow("Erosao",imgErosion)
            cv2.imshow("Original",img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        elif op == "3":
            img = cv2.imread (IMAGEM_TEXTO,cv2.IMREAD_GRAYSCALE)
            if img is None:
                print ('Erro abrindo a imagem.\n')
                sys.exit ()
            # Segmenta a imagem, pois em imagens de textos o fundo geralmente é branco
            if NEGATIVO:
               img = 255 - img

            close_manual= fechamentoManual(img,Kernel4)  
            cv2.imshow("Erosao apos dilatacao (Fechamento)",close_manual)

            # O mesmo processo pode ser realizado via open cv
            closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, Kernel4)
            cv2.imshow("Resultado obtido com fechamento do OpenCV",closing)

            cv2.imshow("Original",img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


        elif op == "4":
            img = cv2.imread (IMAGEM_TEXTO,cv2.IMREAD_GRAYSCALE)
            if img is None:
                print ('Erro abrindo a imagem.\n')
                sys.exit ()

            # Segmenta a imagem, pois em imagens de textos o fundo geralmente é branco
            if NEGATIVO:
               img = 255 - img
            img_AND= interseccaoAND(img,Kernel1,Kernel4)

            cv2.imshow("Interseccao das Erosoes",img_AND)
            cv2.imshow("Original",img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        elif op == "5":
            img = cv2.imread (IMAGEM_TEXTO,cv2.IMREAD_GRAYSCALE)
            img_color = cv2.imread (IMAGEM_TEXTO,cv2.IMREAD_COLOR) #passagem da imagem para aceitar contorno colorido
            if img is None:
                print ('Erro abrindo a imagem.\n')
                sys.exit ()
            
            median = cv2.medianBlur(img,3) #retirando ruídos
             
            # Segmenta a imagem, pois em imagens de textos o fundo geralmente é branco
            if NEGATIVO:
               median = 255 - median

            #conexos(median,img_color)
            extraiTexto(median,img_color)

        else: 
            print('Fim da Execução')
    else: 
            print('Fim da Execução')


if __name__ == '__main__':
    main()

