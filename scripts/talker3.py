#!/usr/bin/env python
import rospy
from std_msgs.msg import String

m = 0.5
r = 0.15
pi = 3.14
rv = 1000
rz = 1.225
g = 9.81
d = 0.47
h0 = -10
T = 0.001
Tend = 10


def predz(x):
    if x < 0:
        return -1
    else:
        return 1


def uzgon(h, r, pi, rv, rz, g):
    Vu = pi * (r+h)**2 * (2*r-h) / 3
    V = 4 * r**3 * pi / 3
    if h < -r:
        y = rv * g * V
    elif h > r:
        y = rz * g * V
    else:
        y = rz * g * Vu + rv * g * (V - Vu)
    return y


def otpor(h, v, r, rv, rz, d):

    A = 2 * r ** 2 * pi
    a = 2 * r * pi * (r - abs(h))

    if v > 0:
        if h < -r:
            y = 0.5 * rv * d * A * v ** 2 * predz(v)
        elif h > 0:
            y = 0.5 * rz * d * A * v ** 2 * predz(v)
        else:
            y1 = 0.5 * rz * d * a * v ** 2 * predz(v)
            y2 = 0.5 * rv * d * (A-a) * v ** 2 * predz(v)
            y = y1 + y2
    elif h > r:
        y = 0.5 * rz * d * A * v ** 2 * predz(v)
    elif h < 0:
        y = 0.5 * rv * d * A * v ** 2 * predz(v)
    else:
        y1 = 0.5 * rv * d * a * v ** 2 * predz(v)
        y2 = 0.5 * rz * d * (A-a) * v ** 2 * predz(v)
        y = y1 + y2

    return y


def pozicija(m, h0, h1, v0, v1, T, r, pi, rv, rz, g, d):
    h2 = (T ** 2 / m) * (uzgon(h1, r, pi, rv, rz, g) - otpor(h1, v1, r, rv, rz, d) - m * g) + (2 * h1) - h0
    v2 = 1 / T * (h2 - h1)
    return (h2, v2)


def simulator(br_kug, m, h0, pi, rv, rz, g, T, d):
    h = [[0 for x in range(3)] for x in range(br_kug)]
    v = [[0 for x in range(3)] for x in range(br_kug)]
    ch = [0 for x in range(br_kug)]
    temp = [0 for x in range(br_kug)]

    for i in range(br_kug):

        h[i][0] = h0
        h[i][1] = h0
        temp[i] = 0

    pub = rospy.Publisher('pozicija', String, queue_size=10)
    rospy.init_node('simulator', anonymous=True)
    rate = rospy.Rate(1/T)   # 10hz
    while not rospy.is_shutdown():
        for i in range(br_kug):
            (h[i][2], v[i][2]) = pozicija(m, h[i][0], h[i][1], v[i][0], v[i][1], T, r, pi, rv, rz, g, d)
        poruka = "Trenutna dubina %.0f. kuglice: %.2f" % (i+1, h[i][2])
        rospy.loginfo(poruka)
        pub.publish(poruka)
        h[i][0] = h[i][1]
        h[i][1] = h[i][2]
        v[i][0] = v[i][1]
        v[i][1] = v[i][2]
        if v[i][2] < 0 and ch[i] == 0:
            temp[i] = m
            ch[i] = 1
            m = 3 * 4188.79 * r ** 3
        if h[i][2] < h0 and ch[i] == 1:
            m = temp[i]
            ch[i]= 0
        rate.sleep()


if __name__ == '__main__':
    try:
        simulator(1, m, h0, pi, rv, rz, g, T, d)
    except rospy.ROSInterruptException:
            pass
