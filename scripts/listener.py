#!/usr/bin/env python
import pygame
import rospy
from std_msgs.msg import String
i = 0
pygame.init()
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
sky_blue = (135, 206, 250)
green = (0, 255, 0)
red = (255, 0, 0)

gameDisplay = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Kuglice')

gameExit = False


def callback(data):
    global i
    i += 1
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data[28:33])
    if i % 50 == 0:
        gameExit = False
        dubina = float(data.data[28:33])
        pozicija = int(200 - dubina * 40)
        if not gameExit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True

            gameDisplay.fill(blue)
            pygame.draw.rect(gameDisplay, sky_blue, [0, 0, 800, 200])
            pygame.draw.circle(gameDisplay, red, [400, pozicija], 20)
            pygame.display.flip()
        else:
            pygame.quit()
            quit()


def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'talker' node so that multiple talkers can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("pozicija", String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
