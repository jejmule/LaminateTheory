# -*- coding: utf-8 -*-
"""
Created on Sun Jul 20 20:24:43 2014

@author: jejmule
"""

mat1 = material('mat1',0,0,0,1,0)
mat1.E1 = double(230e9)
mat1.E2 = double(6.6e9)
mat1.G = double(4.8e9)
mat1.mu = double(0.25)

test = ply(mat1,[90,0],[.5,.5])
C = mat1.get_stifness(0)
C90 =mat1.get_stifness(90)
print C[0,2], C90[0,2]
a=laminate([test],[1])
print a

m = cos(radians(90))
n = sin(radians(90))
Q16 = (C[0,0]-C[0,1]-2*C[2,2])*np.power(m,3)*n+(C[0,1]-C[1,1]+2*C[2,2])*m*np.power(n,3)
print Q16



empa = material('empa',0,0,0,1,0)
empa.E1 = 181000
empa.E2 = 10300
empa.G = 7170
empa.mu = 0.28

la = ply(empa,[0,90],[1,1])
print laminate([la],[1])


nasa = material('nasa',0,0,0,1,0)
nasa.E1 = 20010000
nasa.E2 = 1301000
nasa.G = 1001000
nasa.mu = 0.3
print nasa.get_stifness(45)
ply0 = ply(nasa,[0,45],[0.005,0.005])
L =laminate([ply0,ply0],[1,1])
print L
