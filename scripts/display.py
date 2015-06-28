#!/usr/bin/env python
import pygame
import rospy

from std_msgs.msg import Float32MultiArray


pygame.init()
disp_sirina = 800
disp_visina = 600
white = (220, 220, 220)
black = (50, 50, 50)
grey = (120, 120, 120)
blue = (0, 0, 255)
sky_blue = (135, 206, 250)
green = (0, 255, 0)
red = (255, 0, 0)

gameDisplay = pygame.display.set_mode((disp_sirina, disp_visina))  #definiranje prozora
pygame.display.set_caption('Kuglice')

gameExit = False


def callback(data):
    h0 = rospy.get_param('zad_dub', -10)  #citanje ros parametara
    r = rospy.get_param('radius', 0.15)

    velicina = 20      #postavljanje parametara simulacije
    br_kug = len(data.data)
    dubina = [0 for x in range(br_kug)]
    pozicija_x = [0 for x in range(br_kug)]
    pozicija_y = [0 for x in range(br_kug)]
        
    gameExit = False
    gameDisplay.fill(blue)  #crtanje podloge
    pygame.draw.rect(gameDisplay, sky_blue, [0, 0, disp_sirina, disp_visina / 5])

    for i in range(br_kug):
        dubina[i] = data.data[i]   #citanje dubine
        pozicija_y[i] = int(disp_visina / 5 + (14 * dubina[i] * disp_visina / (20 * h0)))  #racunanje pozicije na ekranu
        pozicija_x[i] = int(disp_sirina / (br_kug + 1) * (i + 1))
        if not gameExit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True

            pygame.draw.circle(gameDisplay, red, [pozicija_x[i], pozicija_y[i]], velicina)   #crtanje kuglice
        else:  #gasenje simulacije na gumb, ne radi dobro
            pygame.quit()
            quit()
    pygame.display.flip()  #prikaz novih kuglica i podloge


def listener():

    rospy.init_node('listener', anonymous=True)  #registracija noda

    rospy.Subscriber("pozicija", Float32MultiArray, callback, queue_size = 1)  #pretplata na topic

    rospy.spin()

if __name__ == '__main__':
    listener()
