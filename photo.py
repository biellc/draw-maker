import cv2
import time
from PIL import Image as img

def capture_photo():
    camera_port = 0
    nFrames = 30
    camera = cv2.VideoCapture(camera_port)
    file = 'image.jpeg'
        
    print("Aperte < ESC > para sair ou < s > para Salvar")

    while True:
        retval, imagem = camera.read()
        cv2.imshow('Foto', imagem)

        k = cv2.waitKey(100)

        if k == 27:
            print('Saindo...')
            break
        if k == ord('s'):
            print('Foto salva')
            cv2.imwrite(file, imagem)
            break

    cv2.destroyAllWindows()

def rgb(imageX, imageY, convertionType, colors, grayOrRGB):
    if grayOrRGB == 0:
        im = img.open('imageGray.jpeg')
        try:
            im.thumbnail((imageX,imageY), img.ANTIALIAS)
        except:
            print("Erro na imagem copiada, tente copiar e dar CTRL + B novamente")
        return im.convert(convertionType, palette=img.WEB, colors=colors)
    else:
        im = img.open('image.jpeg')
        try:
            im.thumbnail((imageX,imageY), img.ANTIALIAS)
        except:
            print("Erro na imagem copiada, tente copiar e dar CTRL + B novamente")
        return im.convert(convertionType, palette=img.WEB, colors=colors)

def gray(imageX, imageY, convertionType, colors):
    im_gray = cv2.imread('image.jpeg', 0)
    cv2.imwrite('imageGray.jpeg', im_gray) 

    rgb(imageX, imageY, convertionType, colors, 0)
