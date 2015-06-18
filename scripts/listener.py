#!/usr/bin/env python
import pygame
import rospy

from std_msgs.msg import String, Float32MultiArray


n = 0
pygame.init()
disp_sirina = 800
disp_visina = 600
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
sky_blue = (135, 206, 250)
green = (0, 255, 0)
red = (255, 0, 0)

gameDisplay = pygame.display.set_mode((disp_sirina, disp_visina))
pygame.display.set_caption('Kuglice')

gameExit = False


def callback(data):
    global n
    n += 1
    br_kug = len(data.data)
    dubina = [0 for x in range(br_kug)]
    pozicija_x = [0 for x in range(br_kug)]
    pozicija_y = [0 for x in range(br_kug)]
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data[28:33])

    if n % 1 == 0:
        gameExit = False
        gameDisplay.fill(blue)
        pygame.draw.rect(gameDisplay, sky_blue, [0, 0, disp_sirina, disp_visina / 4])

        for i in range(br_kug):
            dubina[i] = data.data[i]
            pozicija_y[i] = int(disp_visina/4 - dubina[i] * 40)
            pozicija_x[i] = int(disp_sirina / (br_kug + 1) * (i + 1))
            if not gameExit:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameExit = True

                pygame.draw.circle(gameDisplay, red, [pozicija_x[i], pozicija_y[i]], 20)
            else:
                pygame.quit()
                quit()
        pygame.display.flip()


def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'talker' node so that multiple talkers can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("pozicija", Float32MultiArray, callback, queue_size = 1)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
