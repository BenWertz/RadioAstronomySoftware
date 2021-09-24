import numpy as np
import matplotlib.pyplot as plt
import scipy
import scipy.special
from math import *

# s=np.arange(-pi/2,pi/2,tau/16)
# t=np.arange(0,tau,tau/16)

s=np.linspace(-2,2,200)
t=np.linspace(-2,2,200)

A=2
B=3
C=4
D=5
E=6
F=7

# x=np.cos(A*tau*s)
# y=np.cos(B*tau*s)
# z=np.cos(C*tau*s)

x=np.outer(s,np.ones(len(s)))
y=np.outer(np.ones(len(s)),t)
z=scipy.special.j0(15*np.hypot(x,y))

    #s=np.linspace(-pi/2,pi/2,100)
    #t=np.linspace(0,tau,100)

    # x=np.outer(np.cos(s),np.cos(t))
    # y=np.outer(np.cos(s),np.sin(t))
    # z=np.outer(np.sin(s),np.ones(len(t)))


    # K=0.9
    #
    # R2=0.1
    # K2=0.1
    #
    # x=np.cos(t)+np.cos(t*(1+1/K))/(1+1/K)+R2*np.cos(t*(1+1/K2))
    #
    # y=np.sin(t)+np.sin(t*(1+1/K))/(1+1/K)+R2*np.sin(t*(1+1/K2))

    # fig=plt.figure()
    # ax=fig.gca(projection='3d')
    #
    # # ax.set_facecolor('black')
    #
    # plt.plot(x,y,t,'lime',linewidth=1)

fig=plt.figure(figsize=(8,4))
ax=fig.add_subplot(121,projection='3d')
ax2=fig.add_subplot(122)

#ax.plot(x,y,z)
#ax.set_proj_type('ortho')
ax.plot_surface(x,y,z,cmap='viridis',edgecolor='none')


# ax.set_xlim3d(-2,2)
# ax.set_ylim3d(-2,2)
# ax.set_zlim3d(-2,2)
# ax.set_box_aspect([1,1,1])

ax2.imshow(z)

#fig.gca().set_aspect('equal')
# plt.xlabel("Angle")
# plt.ylabel("Sine")
# plt.title("Sine wave")
plt.show()