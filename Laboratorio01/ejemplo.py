import pygame
from pygame.locals import *


from gl import Renderer


widht = 960
height = 540

screen = pygame.display.set_mode((widht,height))
clock = pygame.time.Clock()

poligono_1 = [(165, 380) ,(185, 360), (180, 330), (207, 345), (233, 330), (230, 360), (250, 380) ,(220, 385), (205, 410) ,(193, 383)]
poligono_2 = [(321, 335), (288, 286), (339, 251), (374, 302)]

# Polígono 3
poligono_3 = [(377, 249), (411, 197) ,(436, 249)]


# Polígono 4
poligono_4 = [(413, 177), (448, 159), (502, 88), (553, 53), (535, 36), 
              (676, 37), (660, 52), (750, 145), (761, 179), (672, 192), 
              (659, 214), (615, 214), (632, 230), (580, 230), (597, 215), 
              (552, 214), (517, 144), (466, 180)]

# Polígono 5
poligono_5 = [(682, 175), (708, 120), (735, 148), (739, 170)]
def poligono(listaPuntos, color =None):
    for i in range(len(listaPuntos)):
        rend.glLine(listaPuntos[i], listaPuntos[(i + 1) % len(listaPuntos)],color)


rend = Renderer(screen)
isRunning = True




while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

    rend.glClear()
    # Aqui dibujo una y otra vez 
    poligono(poligono_1,(1,0,1))
    poligono(poligono_2,(1,0,0))
    poligono(poligono_3,(1,1,0))
    poligono(poligono_4,(0,0,1))
    poligono(poligono_5,(0.75,1,0))
    rend.glFillPolygon(poligono_1,(1,0,1))
    rend.glFillPolygon(poligono_2,(1,0,0))
    rend.glFillPolygon(poligono_3,(1,1,0))
    rend.glFillPolygon(poligono_4,(0,0,1))
    rend.glFillPolygon(poligono_5,(0.75,1,0))
    
    


    #for x in range(0, widht, 20):
     #   rend.glLine((0,0), (x,height))
      #  rend.glLine((0,height-1), (x,0))
       # rend.glLine((widht-1,0), (x,height))
        #rend.glLine((widht-1,height-1), (x,0))
        
    ########################################################

    pygame.display.flip()
    clock.tick(60)
rend.glGenerateFrameBuffer("output.bmp")
pygame.quit()