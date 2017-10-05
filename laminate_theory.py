# -*- coding: utf-8 -*-
"""
Created on Sun Jul 06 14:59:42 2014

@author: jejmule
"""
import numpy as np

class material(object):    
       
    def __init__(self,name,E,G,mu,rho,alpha):
        ##initialisation
        self.name = name
        self.E1=E         
        self.E2=E
        self.G=G
        self.mu=mu
        self.rho=rho
        self.alpha = [alpha,alpha,0]
    
    def __repr__(self):
        return self.name
        
    def __str__(self):
        return self.name
    
    def mixComposite(self,matrix,Vf):
        ## Mix a fiber materiel (self) with the matrix
        ##Vf : Fiber volume fraction
        ##Vm : Matrix volume fraction
        Vm = 1-Vf
        temp1 = self.E1*Vf+matrix.E1*Vm
        temp2 = (self.E1*matrix.E1) / (Vf*matrix.E1 + Vm*self.E1)
        self.E1 = temp1
        self.E2 = temp2
        self.G = (self.G*matrix.G) / (Vf*matrix.G + Vm*self.G)
        self.mu = Vf*self.mu + Vm*matrix.mu
        self.rho = Vf*self.rho+Vm*matrix.rho
        alpha1 = Vf*self.alpha[0]+(1-Vf)*matrix.alpha[0]
        alpha2 = 1 / ((Vf/self.alpha[0])+(Vm/matrix.alpha[0]))
        self.alpha = [alpha1,alpha2,0]
     
    
    def get_stifness(self,angle):
        #reduced stiffness matrix Qij
        mu12 = self.mu
        mu21 = self.E2*self.mu/self.E1
       
        Q=np.zeros((3,3))

        Q[0,0]=self.E1 / (1-mu12*mu21)
        Q[0,1]=mu12*self.E2 / (1-mu12*mu21)
        Q[1,0]=mu21*self.E1 / (1-mu12*mu21)
        Q[1,1]=self.E2 / (1-mu12*mu21)
        Q[2,2]=self.G
        return rotation(Q,angle)
        
    def get_alpha(self,angle):
        rad = np.radians(angle) 
        xx = self.alpha[0]*np.power(np.cos(rad),2)+self.alpha[1]*np.power(np.sin(rad),2)
        yy = self.alpha[0]*np.power(np.sin(rad),2)+self.alpha[1]*np.power(np.cos(rad),2)
        xy = 2*np.cos(rad)*np.sin(rad)*(self.alpha[0]-self.alpha[1])
        return [xx,yy,xy]
    
    
def rotation(matrix,degree) :
    rad = np.radians(degree)    
    T = np.array([[np.power(np.cos(rad),2),np.power(np.sin(rad),2),2*np.cos(rad)*np.sin(rad)]
    ,[np.power(np.sin(rad),2),np.power(np.cos(rad),2),-2*np.cos(rad)*np.sin(rad)],
      [-np.cos(rad)*np.sin(rad),np.cos(rad)*np.sin(rad),np.power(np.cos(rad),2)-np.power(np.sin(rad),2)]])
    #print(T)
    diag = []
    diag = np.zeros((3,3))
    diag[0,0] = 1
    diag[1,1] = 1
    diag[2,2] = 2
    return np.dot(np.dot(np.linalg.inv(T),matrix),np.linalg.inv(T.T))
    
class ply(object):
    #material = None
    #orientation = []
    #grammage = []
    #length = None
    thickness = []    
    def __init__(self,material,orientation,grammage):
        self.material = material
        self.orientation = orientation
        self.grammage = np.array(grammage)#*1/1000
        self.thickness = self.grammage# * self.material.toto
        if len(orientation) == len(orientation):
            self.length = len(orientation)
        else:
            print('error, orientation list and grammage are not equal in length')
    
    def __repr__(self):
        out = '\nmaterial :'+str(self.material)+'\n'
        out += 'orientaion :'
        for i, el in enumerate(self.orientation):
            out += str(el) + ' '
        out += '\n'+'grammage in mm :' 
        for i, el in enumerate(self.grammage):
            out += str(el) + ' '
        return out
    def ruban(self,ratio):
        #ratio est le rapport entre le ruban et la largeur total
        return ply(self.material,self.orientation, self.grammage * ratio)

class laminate(object):
    A = []
    B = []
    D = []
    h = []
    thickness = {0}
    def __init__(self,plylist,order):
        self.materials = []
        self.orientations = []
        self.thickness = []
        self.plylist = plylist
        self.assembly(plylist,order)
        self.compute()
        
    def assembly(self,plylist,order):
        #length = 0;
        for i, p in enumerate(plylist):
            #build material list
            self.materials += [p.material]*p.length
            #build orientation and thickness lists
            o = list(p.orientation)
            t = list(p.thickness)
            if order[i] < 0:
                o.reverse()
                t.reverse()
            self.orientations += o
            self.thickness += t
            
    def compute(self):
        #h_t is the total laminate height
        #h is the height of each ply from the geometrical plane
        h_t = 0;
        for i, t in enumerate(self.thickness):
            h_t += t
        h = [];
        h.append(h_t/2)
        
        for i, t in enumerate(self.thickness):
            h.append(h[i]-t)
            
        #compute A,B and D laminate stiffness matrix with the classical lamination theory
        self.A = np.zeros((3,3))
        self.B = np.zeros((3,3))
        self.D = np.zeros((3,3))
        for i, layer in enumerate(self.materials):
            self.A += layer.get_stifness(self.orientations[i])*(h[i]-h[i+1])
            self.B += layer.get_stifness(self.orientations[i])*(np.power(h[i],2)-np.power(h[i+1],2))
            self.D += layer.get_stifness(self.orientations[i])*(np.power(h[i],3)-np.power(h[i+1],3))
        self.B = self.B/2
        self.D = self.D/3
        self.h = h
        
    def __repr__(self):
        out = '\nlaminate description\n'
        for i, txt in enumerate(self.materials):
            out += 'layer '+str(i)+': '+str(txt)+', '+str(self.orientations[i])+'\xB0, '+str(self.thickness[i])+' mm\n'
        out += '\nmatrice A:\n'+str(self.A)+'\nmatrice B:\n'+str(self.B)+'\nmatrice D:\n'+str(self.D)
        return out
        
    def thermal_stress(self,deltaT):
        Nxx = 0
        Nyy = 0
        Nxy = 0
        Mxx = 0
        Myy = 0
        Mxy = 0
        for i, layer in enumerate(self.materials):
            Q =  layer.get_stifness(self.orientations[i])
            alpha = layer.get_alpha(self.orientations[i])
            h = self.h
            Nxx += (Q[0,0]*alpha[0]+Q[0,1]*alpha[1]+Q[0,2]*alpha[2])*(h[i]-h[i+1])
            Nyy += (Q[0,1]*alpha[0]+Q[1,1]*alpha[1]+Q[1,2]*alpha[2])*(h[i]-h[i+1])
            Nxy += (Q[0,2]*alpha[0]+Q[1,2]*alpha[1]+Q[2,2]*alpha[2])*(h[i]-h[i+1])
            Mxx += (Q[0,0]*alpha[0]+Q[0,1]*alpha[1]+Q[0,2]*alpha[2])*(np.power(h[i],2)-np.power(h[i+1],2))
            Myy += (Q[0,1]*alpha[0]+Q[1,1]*alpha[1]+Q[1,2]*alpha[2])*(np.power(h[i],2)-np.power(h[i+1],2))
            Mxy += (Q[0,2]*alpha[0]+Q[1,2]*alpha[1]+Q[2,2]*alpha[2])*(np.power(h[i],2)-np.power(h[i+1],2))
        Nxx = deltaT * Nxx
        Nyy = deltaT * Nyy
        Nxy = deltaT * Nxy
        Mxx = deltaT * Mxx / 2
        Myy = deltaT * Myy / 2
        Mxy = deltaT * Mxy / 2
        return [Nxx,Nyy,Nxy,Mxx,Myy,Mxy]
        
    def inverse(self):
        matrix = np.zeros((6,6))
        Ai = np.linalg.inv(self.A)
        Bi = np.linalg.inv(self.B)
        Di = np.linalg.inv(self.D)
        for i in range(6):
            for j in range(6):
                if i<3 and j<3:
                    matrix[i,j] = Ai[i,j]
                if i>3 and j<3:
                    matrix[i,j] = Bi[i-3,j]
                if i<3 and j>3:
                    matrix[i,j] = Bi[i,j-3]
                if i>3 and j>3:
                    matrix[i,j] = Di[i-3,j-3]
        return matrix
    
    def apply_load(self,load):
        return np.dot(self.inverse(),load)

