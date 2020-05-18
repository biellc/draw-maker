# Libraries
from PIL import Image as img
from pynput.mouse import Controller
from datetime import datetime
from PIL import ImageGrab

import colorsys
import keyboard
import os.path
import uuid
import winsound
import colorsys
import pyautogui
import sys
import pyfiglet
import cv2
import time

from photo import capture_photo, gray, rgb

# Variables
definition = "SD"
globalConfig = []
p = ""
op = ""
grayOrRGB = ""

space = 0
convertionType = ''
colors = 0
imageX = 0
imageY = 0
skipWhite = False
pyautogui.PAUSE = 1/100

# Help Functions
def beep(freq):
    return winsound.Beep(freq, 1000)

def stopApp():
    exit()

def ler_file(file):
    with open(file) as f:
        return list(map(int,(str(f.read()).split(','))))

def write_file(name, array):
    f= open(name,"w")
    f.write(','.join((str(v) for v in array)))
    f.close()

# Main Functions

def configurarBOT():
    global globalConfig, p
    (x,y) = Controller().position
    globalConfig.append(x)
    globalConfig.append(y)
    beep(500)
    if(len(globalConfig) == 2):
        print ("2: Posicione o cursor em cima do icone de PALETA e dê ALT+X")
    if(len(globalConfig) == 4):
        print ("3: Posicione o cursor no canto inferior esquerdo do seletor de CORES e dê ALT+X")
    if(len(globalConfig) == 6):
        print ("4: Posicione o cursor na parte inferior da BARRA da PALETA e dê ALT+X")
    if(len(globalConfig) == 8):
        print("5: Posicione o cursor no local onde o desenho será iniciado")
    if (len(globalConfig) == 10):
        write_file("configs.log", globalConfig)
        print ("Sucesso: Seu bot está pronto! Caso haja algum erro deleta o arquivo config.logs para refazer o procedimento!")
        print ("Lembre-se de não alterar o zoom do navegador ou diminuir o tamanho da tela!\n")
        stopApp()
    return triggerAltX()

lastRGB = "255,255,255"
def pixelar(R,G,B, canvas, ax, ay):
    global lastRGB, globalConfig, p
    pyautogui.click(globalConfig[0], globalConfig[1])
    if lastRGB != ("{0},{1},{2}".format(R,G,B)):
        lastRGB =  ("{0},{1},{2}".format(R,G,B))
        Hue, Saturation, Value = colorsys.rgb_to_hsv(R,G,B)
        pyautogui.click(globalConfig[2],globalConfig[3])
        pyautogui.click(globalConfig[4] + (Hue*180), globalConfig[5] - (Saturation*100))
        pyautogui.click(globalConfig[6], globalConfig[7] - (Value/2.55))
        time.sleep(0.005)
    pyautogui.click(canvas[0]+(ax*space),canvas[1]+(ay*space))
    time.sleep(0.005)

def image():
    global op, grayOrRGB
    if op == 1:
        im = ImageGrab.grabclipboard()
        try:
            im.thumbnail((imageX,imageY), img.ANTIALIAS)
        except:
            print("Erro na imagem copiada, tente copiar e dar CTRL + B novamente")
            stopApp()
        beep(1000)
        return im.convert(convertionType, palette=img.WEB, colors=colors).convert('RGB')
    elif op == 2:
        capture_photo()
        beep(2500)
        time.sleep(2)
        if grayOrRGB == 2:
            return gray (imageX, imageY, convertionType, colors)
        else:
            return rgb (imageX, imageY, convertionType, colors, 1)

def checkPixel(imageMapPixels, x,y, tox, toy):
    if "{0}_{1}".format(x+tox, y+toy) not in imageMapPixels or  "{0}_{1}".format(x, y) not in imageMapPixels:
        return False
    return imageMapPixels["{0}_{1}".format(x, y)] != imageMapPixels["{0}_{1}".format(x+tox, y+toy)]

def mapImageToDictionary(imagem):
    imageMapPixels = {}
    imageMapColor = {}
    largura, altura = imagem.size
    for y in range(altura):
        for x in range(largura):
            pixel = imagem.getpixel((x, y))
            rgb = "%d,%d,%d" % ((pixel[0]), (pixel[1]), (pixel[2]))
            pixel = "%d_%d" % (x,y)
            if rgb not in imageMapColor.keys():
                imageMapColor[rgb] = []
            imageMapColor[rgb].append([x,y])
            imageMapPixels[pixel] = rgb
    return [imageMapPixels, imageMapColor]

def receberImagem():
    global globalConfig
    imagem = image()
    print ('Carregando imagem ...')
    canvas = list(Controller().position)
    pyautogui.click(globalConfig[0], globalConfig[1])
    pyautogui.move(globalConfig[8], globalConfig[9])
    print ('Mapeando imagem ...')
    (imageMapPixels, imageMapColor) = mapImageToDictionary(imagem)
    print("Cores contabilizadas: ", len(imageMapColor), "\n\nImagem processada com sucesso!")
    print("Para desligar o bot, use: CTRL+I")
    winsound.Beep(1500, 100)
    for rgb in imageMapColor.keys():
        R, G, B = (map(int,(rgb.split(','))))
        if R > 200 and G > 200 and B > 200 and skipWhite:
            continue
        conta = -1
        while(conta < len(imageMapColor[rgb]) - 1):
            if keyboard.is_pressed("ctrl+i"):
                break
            conta += 1
            if not checkPixel(imageMapPixels, imageMapColor[rgb][conta][0], imageMapColor[rgb][conta][1], -1, -1):
                continue
            if not checkPixel(imageMapPixels, imageMapColor[rgb][conta][0], imageMapColor[rgb][conta][1], 1, 1):
                continue
            if not checkPixel(imageMapPixels, imageMapColor[rgb][conta][0], imageMapColor[rgb][conta][1], -1, 0):
                continue
            if not checkPixel(imageMapPixels, imageMapColor[rgb][conta][0], imageMapColor[rgb][conta][1], 0, -1):
                continue
            if not checkPixel(imageMapPixels, imageMapColor[rgb][conta][0], imageMapColor[rgb][conta][1], 1, 0):
                continue
            if not checkPixel(imageMapPixels, imageMapColor[rgb][conta][0], imageMapColor[rgb][conta][1], 0, 1):
                continue
            pixelar(R,G,B, canvas, imageMapColor[rgb][conta][0], imageMapColor[rgb][conta][1])
            del imageMapPixels["{0}_{1}" .format( imageMapColor[rgb][conta][0], imageMapColor[rgb][conta][1])]

    for rgb in imageMapColor.keys():
        R, G, B = (map(int,(rgb.split(','))))
        if R > 200 and G > 200 and B > 200 and skipWhite:
            continue
        conta = -1
        while(conta < len(imageMapColor[rgb]) - 1):
            if keyboard.is_pressed("ctrl+i"):
                stopApp()
            conta += 1
            if  "{0}_{1}" .format( imageMapColor[rgb][conta][0], imageMapColor[rgb][conta][1]) not in imageMapPixels:
                continue
            pixelar(R,G,B, canvas, imageMapColor[rgb][conta][0], imageMapColor[rgb][conta][1])

    print('Desenho completado!')
    beep(2000)

def triggerAltX():
    while not keyboard.is_pressed("alt+x"):
        pass
    configurarBOT()

def options():
    global op, grayOrRGB, definition, space, convertionType, colors, imageX, imageY, skipWhite
    definition = str(input('Você quer que o desenho seja feito em Alta Resolução (HD) ou baixa (SD)? '))
    if definition.lower() == "hd":
        space = 1
        convertionType = 'RGB' 
        colors = 256 
        imageX = 350 
        imageY = 350  
        skipWhite = False
        pyautogui.PAUSE = 1/1000
    else:
        if definition.lower() == "sd":
            print('Definição escolhida: SD')
        else:
            print('Definição não reconhecida... por padrão irei desenhar utilizando a definição SD')
        space = 2.5
        convertionType = 'P'
        colors = 32
        imageX = 100
        imageY = 100
        skipWhite = True
        pyautogui.PAUSE = 1/100
    print('Usar uma imagem que foi copiada - 1')
    print('Tirar uma foto - 2')
    op = int(input('Você prefere tirar uma foto ou usar uma imagem que foi copiada? '))
    if op == 1:
        print('Pressione CTRL + B para fazer upload da imagem')
    else:
        print('Colorida - 1')
        print('Preto e branco - 2')
        grayOrRGB = int(input('Você quer sua foto colorida ou preto e branco? '))
        print('Pressione CTRL + B para tirar uma foto')

def iniciarPrograma():
    global globalConfig
    if os.path.exists('configs.log'):
        options()
        globalConfig = ler_file('configs.log')
        beep(3000)

        while not keyboard.is_pressed("ctrl+b") and not keyboard.is_pressed("ctrl+i"):
            pass
        if keyboard.is_pressed("ctrl+b"):
            receberImagem()
        if keyboard.is_pressed("ctrl+i"):
            stopApp()
    else:
        global p
        beep(500)
        print("\n\n\n=========== PRIMEIRA EXECUCAO DO BOT, VAMOS CONFIGURAR ELE===============\n")
        print('Meus testes foram realizados neste site: https://gartic.com.br/praticar/ \nRecomendo que você também use ele')
        print("1: Posicione o cursor em CIMA do ícone do LÁPIS e dê ALT+X")
        triggerAltX()

iniciarPrograma()
