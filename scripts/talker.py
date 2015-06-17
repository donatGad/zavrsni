#!/usr/bin/env python

## Simple talker demo that published std_msgs/Strings messages
## to the 'chatter' topic

import rospy
from std_msgs.msg import String

m=0.5
r=0.15
pi=3.14
rv=1000
rz=1.225
g=9.81
d=0.47
h0=-10
T=0.001
Tend=10

def predz(x):
    if x< 0:
        return -1
    else:
        return 1

def uzgon(h,r,pi,rv,rz,g):
    Vu = pi * (r+h)**2 * (2*r-h) / 3
    V = 4 * r**3 * pi / 3
    if h < -r: 
        y = rv * g * V
    elif h > r:
        y = rz * g * V
    else:
        y = rz * g * Vu + rv * g * (V - Vu)
    return y

def otpor(h,v,r,rv,rz,d):
    
    A=2*r**2*pi 
    a=2*r*pi*(r-abs(h))

    if v>0:
        if h < -r:
            y=0.5*rv*d*A*v**2*predz(v)
        elif h > 0:
            y=0.5*rz*d*A*v**2*predz(v)
        else:
            y=0.5*rz*d*a*v**2*predz(v) + 0.5*rv*d*(A-a)*v**2*predz(v)
    elif h>r:
        y=0.5*rz*d*A*v**2*predz(v)
    elif h<0:
        y=0.5*rv*d*A*v**2*predz(v)
    else:
        y=0.5*rv*d*a*v**2*predz(v) + 0.5*rz*d*(A-a)*v**2*predz(v)
    return y

def simulator(m,h0,pi,rv,rz,g,T,d): 
	v=[]
	h=[]
	v.append(0)
	v.append(0)
	h.append(h0)
	h.append(h0)
	i=2
	ch=0
	temp=0
	pub = rospy.Publisher('pozicija', String, queue_size=10)
	rospy.init_node('talker', anonymous=True)
	rate = rospy.Rate(1/T) # 10hz
	while not rospy.is_shutdown():
		hi=(T**2/m)*(uzgon(h[i-1], r, pi, rv, rz, g) - otpor(h[i-1], v[i-1], r, rv, rz, d) - m*g) + 2*h[i-1] - h[i-2]
		h.append(hi)
		vi=1/T*(h[i]-h[i-1])
		v.append(vi)
		poruka = "Trenutna dubina: %.2f" %h[i]
		rospy.loginfo(poruka)
		pub.publish(poruka)
		i=i+1
		if vi<0 and ch == 0:
			temp=m
			ch=1	
			m = 3*4188.79*r**3
		if hi< h0 and ch==1:
			m = temp
			ch=0
		rate.sleep()
				

	
if __name__ == '__main__':
	try:
		simulator(m,h0,pi,rv,rz,g,T,d)
	except rospy.ROSInterruptException:
		pass
