from math import *
import numpy as np
from cmath import exp as cexp
import scipy.special as sci

import numpy as np
import matplotlib.pyplot as plt

c=3.0e8 #Speed of light

def calculatePattern(A,L1,frequency):

    theta=np.zeros([50],dtype=float)
    phi=np.zeros([3],dtype=float)

    for i in range(len(phi)):
        phi[i]=-90+i*180/(len(phi)-1)

    DATA=np.zeros([3,len(phi),len(theta)],dtype=float)
    RPcp=np.zeros([len(phi),len(theta)],dtype=float)
    RPxp=np.zeros([len(phi),len(theta)],dtype=float)

    for i in range(len(theta)):
        theta[i]=-90+i*180/(len(theta)-1)

    if A=="" or L1=="":
        print("Error: Some parameters are missing")
        return


    A=float(A)
    wavelength=c/frequency
    #Phase error
    t=A**2/(8.0*wavelength*L1)

    deltaX=wavelength/10
    deltaPolar=pi/10
    Eax2=0+0j
    Eay2=0+0j
    Eax2Eay2=0
    directivity=0

    # Check cutoff frequency

    if c/(1.706*A)>frequency: #TE11 node
        print("Error: Aperture is too small to support TE11 mode at " + (frequency*1e-9) + "GHz")
        return

    deltaX=(A/2)/round((A/2)/deltaX)
    deltaPolar=min(deltaPolar,pi/round(pi*(A/2)*10/wavelength))

    R_=np.zeros([int(round(2*pi/deltaPolar)),int(round((A/2)/deltaX+1))],dtype=float)
    A_=np.zeros([int(round(2*pi/deltaPolar)),int(round((A/2)/deltaX+1))],dtype=float)
    X_=np.zeros([int(round(2*pi/deltaPolar)),int(round((A/2)/deltaX+1))],dtype=float)
    Y_=np.zeros([int(round(2*pi/deltaPolar)),int(round((A/2)/deltaX+1))],dtype=float)
    diff=np.zeros([int(round(2*pi/deltaPolar)),int(round((A/2)/deltaX+1))],dtype=float)

    Ea_x=np.zeros([len(A_),len(R_[0])],dtype=complex)
    Ea_y=np.zeros([len(A_),len(R_[0])],dtype=complex)

    for i in range(len(A_)):
        # R_[i]=np(Math.round((A/2)/deltax+1));
        # A_[i]=new Array(Math.round((A/2)/deltax+1));
        # X_[i]=new Array(Math.round((A/2)/deltax+1));
        # Y_[i]=new Array(Math.round((A/2)/deltax+1));
        # diff[i]=new Array(Math.round((A/2)/deltax+1));
        for j in range(len(R_[i])):
            R_[i][j]=j*deltaX;
            A_[i][j]=deltaPolar+i*deltaPolar
            X_[i][j]=R_[i][j]*cos(A_[i][j])
            Y_[i][j]=R_[i][j]*sin(A_[i][j])
            diff[i][j]=deltaX*deltaPolar*R_[i][j]

            Ea_x[i][j]=complex(
                (sci.jv(2,1.841*R_[i][j]/(A/2))*sin(2*A_[i][j]))*cos(-2*pi*t*pow(R_[i][j]/(A/2),2)),
                (sci.jv(2,1.841*R_[i][j]/(A/2))*sin(2*A_[i][j]))*sin(-2*pi*t*pow(R_[i][j]/(A/2),2))
                )

            Ea_y[i][j]=complex(
                (sci.j0(1.841*R_[i][j]/(A/2))-sci.jv(2,1.841*R_[i][j]/(A/2))*cos(2*A_[i][j]))*cos(-2*pi*t*pow(R_[i][j]/(A/2),2)),
                (sci.j0(1.841*R_[i][j]/(A/2))-sci.jv(2,1.841*R_[i][j]/(A/2))*cos(2*A_[i][j]))*sin(-2*pi*t*pow(R_[i][j]/(A/2),2))
            )

            Eax2+=diff[i][j]*Ea_x[i][j]
            Eay2+=diff[i][j]*Ea_y[i][j]
            magnitudeSum=float((Ea_x[i][j]*Ea_x[i][j].conjugate()+Ea_y[i][j]*Ea_y[i][j].conjugate()).real)
            magnitudeSum2=float((Eax2*Eax2.conjugate()+Eay2*Eay2.conjugate()).real)
            Eax2Eay2+=diff[i][j]*magnitudeSum
    directivity=10*log10(4*pi/pow(wavelength,2)*magnitudeSum2/Eax2Eay2)/log10(10);
    #document.getElementById("Directivity").innerHTML=Directivity.toFixed(2);


    Px=np.zeros([len(theta)],dtype=complex)
    Py=np.zeros([len(theta)],dtype=complex)

    Ecp=np.zeros([len(theta)],dtype=complex)
    Exp=np.zeros([len(theta)],dtype=complex)

    expVar=0+0j

    for m in range(len(phi)):
        for k in range(len(theta)):
            # print(m,k)
            Px[k]=0+0j
            Py[k]=0+0j
            for i in range(len(Y_)):
                for j in range(len(X_[i])):
                    expVar=cexp(
                        2j*pi/wavelength*
                            (X_[i][j]*sin(theta[k]*pi/180)*cos(phi[m]*pi/180)+
                             Y_[i][j]*sin(theta[k]*pi/180)*sin(phi[m]*pi/180))
                    )
                    Px[k]+=diff[i][j]*(Ea_x[i][j]*expVar)
                    Py[k]+=diff[i][j]*(Ea_y[i][j]*expVar)
            # print(Ea_y[i][j],Y_[i][j],sin(theta[k]*pi/180),sin(phi[m]*pi/180),k,m)
            # print(i,j)
            # print(Px[k],Py[k])
            # quit()

            multiplierCp=(Px[k]*(cos(phi[m]*pi/180)*sin(phi[m]*pi/180)*(1-cos(theta[k]*pi/180)))+
                        Py[k]*
                        (pow(sin(phi[m]*pi/180),2)+cos(theta[k]*pi/180)*pow(cos(phi[m]*pi/180),2)))

            multiplierXp=(Py[k]*(sin(phi[m]*pi/180)*cos(phi[m]*pi/180)*(1-cos(theta[k]*pi/180)))+
                        Px[k]*
                        (pow(cos(phi[m]*pi/180),2)+cos(theta[k]*pi/180)*pow(sin(phi[m]*pi/180),2)))

            # multiplierXp=(cos(phi[m]*pi/180)*sin(phi[m]*pi/180)*(1-cos(theta[k]*pi/180))+
            #             Py[k]*
            #             (pow(sin(phi[m]*pi/180),2)+cos(theta[k]*pi/180)*pow(cos(phi[m]*pi/180),2)))

            Ecp[k]=multiplierCp
            Exp[k]=multiplierXp


            RPcp[m][k]=sqrt(Ecp[k].real**2+Ecp[k].imag**2)
            RPxp[m][k]=sqrt(Exp[k].real**2+Exp[k].imag**2)
#        quit()

    print(RPcp.shape)
    Emax=max([max(RPcp[n]) for n in range(len(RPcp))])

    for k in range(len(theta)):
        for m in range(len(phi)):
            # Circular polarization (HI isn't circularly polarized on average, so not important)
            DATA[0][m][k]=10*(log(RPcp[len(phi)-m-1][k]/Emax)/log(10))
            # Linear polarization (the one we're using)
            DATA[1][m][k]=10*(log(RPxp[len(phi)-m-1][k]/Emax)/log(10))

            DATA[2][m][k]=10*(log((RPcp[len(phi)-m-1][k]+RPxp[len(phi)-m-1][k])/Emax)/log(10))

#            DATA[0][m][k]=(RPcp[len(phi)-m-1][k]/Emax)#(log(RPxp[len(phi)-m-1][k]/Emax)/log(10))
 #           DATA[1][m][k]=(RPxp[len(phi)-m-1][k]/Emax)#(log(RPxp[len(phi)-m-1][k]/Emax)/log(10))
    return [directivity,theta,phi,DATA]

output=calculatePattern(0.280,0.587,1.420405e9)

# plt.axes(xlim=(min(output[1]),max(output[1])),ylim=(-80,0))

drawMode=0
if drawMode==0:
    plt.axes(ylim=(-80,0))

    for i in range(1):
        for j in range(len(output[3][1])):
            plt.plot(output[1],output[3][2][j])
    plt.plot(output[1],[-3 for i in output[1]])

    print(output[1].shape,output[2].shape,output[3].shape)
elif drawMode==1:
    K=180
    ax=plt.axes(xlim=[-K,K],ylim=[-K,K])
    theta, phi = output[1]*pi/180,output[2]*pi/180
    THETA,PHI=np.meshgrid(theta,phi)
    R=output[3][2]#np.maximum(50+output[3][2],0)
    X=180/pi*np.sin(THETA)*np.cos(PHI)
    Y=180/pi*np.sin(THETA)*np.sin(PHI)
    #print(X.shape,Y.shape,output[3][0].shape)
    ax.pcolormesh(THETA*180/pi,PHI*180/pi,R,shading="gouraud")
    CS=ax.contour(THETA*180/pi,PHI*180/pi,R,levels=[-20,-3],colors='k')
    ax.clabel(CS,inline=True,fontsize=10)
    # ax.pcolormesh(X,Y,R,
    #     cmap='jet')
else:
    K=60
    ax=plt.axes(projection='3d',xlim=[-K,K],ylim=[-K,K],zlim=[-K*.7,K*.7])
    theta, phi = output[1]*pi/180,output[2]*pi/180
    THETA,PHI=np.meshgrid(theta,phi)
    for i in range(1):
        R=80+4*output[3][2]
        X=R*np.sin(THETA)*np.cos(PHI)
        Y=R*np.sin(THETA)*np.sin(PHI)
        Z=R*np.cos(THETA)
        print(X.shape,Y.shape,Z.shape)
        #print(X.shape,Y.shape,output[3][0].shape)
        plot=ax.plot_surface(
            X,Y,Z,rstride=1,cstride=1,cmap=plt.get_cmap('jet'),
            linewidth=0,antialiased=False,alpha=1)
print(output[0])
plt.show()
