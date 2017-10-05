# -*- coding: utf-8 -*-
"""
Created on Sun Jul 06 19:04:07 2014

@author: jejmule
"""
#definition des materiaux de base
glass = material('glass',73,23,0.2,2.55,5e-6)
carbon = material('carbon',260,93,0.33,1.78,8e-6)
flax = material ('flax',60,6.4,0.35,1.35,1e-10)  #mixed properties
epoxy = material('epoxy',3.3,1.33,0.33,1.2,55e-6)
glass.mixComposite(epoxy,0.43)
carbon.mixComposite(epoxy,0.43)
flax.mixComposite(epoxy,0.43)
titanal = material('titanal',70,26,0.35,1,22.2e-6)
mdf = material('MDF',4,1.6,0.25,1,3e-6)

triax_V_1100 = ply(glass,[0,-45,45],[.561,.221,.221])
triax_V_1100i = ply(glass,[0,45,-45],[.561,.221,.221])

triax_V_860 = ply(glass,[0,-45,45],[.288,.284,.284])
triax_V_860i = ply(glass,[0,45,-45],[.288,.284,.284])

triax_V_560 = ply(glass,[0,-45,45],[.288,.136,.136])
triax_V_560i = ply(glass,[0,45,-45],[.288,.136,.136])

biax_V_312 = ply(glass,[45,-45],[0.156,0.156])
biax_V_400 = ply(glass,[45,-45],[0.2,0.2])

serge_C_200 = ply(carbon,[0,90],[.100,.100])
serge_C_400 = ply(carbon,[0,90],[.200,.200])
biax_C_200 = ply(carbon,[-45,45],[.100,.100])
UD_C_140 = ply(carbon,[0],[0.140])
UD_C_170 = ply(carbon,[0],[0.170])
UD_C_200 = ply(carbon,[0],[0.200])
UD_C_300 = ply(carbon,[0],[0.300])
UD_V_300 = ply(glass,[0],[0.300])
UD_V_600 = ply(glass,[0],[0.600])
alu_02 = ply(titanal,[0],[0.2])
alu_04 = ply(titanal,[0],[0.4])
alu_06 = ply(titanal,[0],[0.6])
alu_08 = ply(titanal,[0],[0.8])
mdf_3 = ply(mdf,[0],[3])
mdf_8 = ply(mdf,[0],[10])
mdf_10 = ply(mdf,[0],[10])

UD_C = ply(carbon,[0],[0.174*25/90])

LinBi = ply(flax,[-45,45],[.150,.150])
LinUD = ply(flax,[0],[.300])
UD_C_full = ply(carbon,[0],[0.1])

UD_C_test = ply(carbon,[0],[0.1])

#compo_0 = laminate([triax_V_1100,mdf_3,triax_V_1100],[1,1,-1])
#compo_1 = laminate([UD_C,triax_V_860,mdf_3,triax_V_860,UD_C],[1,1,1,-1,1])
#compo_2 = laminate([lin30,mdf_3,lin30],[1,1,-1])

AntiConfFlax = laminate([LinUD,LinBi,mdf_8,LinBi,LinUD],[1,1,1,-1,1])
print(AntiConfFlax)
AntiConfFlaxC200 = laminate([UD_C_test,LinBi,mdf_8,LinBi,UD_C_test],[1,1,1,-1,1])
print(AntiConfFlaxC200)

#compo_1 = laminate([alu_04,mdf_3,alu_04],[1,1,1])
#compo_2 = laminate([UD_C_200,biax_C_200,mdf_3,biax_C_200,UD_C_200],[1,1,1,1,1])
#compo_3 = laminate([UD_C_200,serge_C_200,mdf_3,serge_C_200,UD_C_200],[1,1,1,-1,1])
#compo_4 = laminate([UD_C_200,serge_C_400,mdf_3,serge_C_400,UD_C_200],[1,1,1,-1,1])
#compo_5 = laminate([UD_C_200,biax_V_312,mdf_3,biax_V_312,UD_C_200],[1,1,1,-1,1])
#compo_6 = laminate([UD_C_200,biax_V_400,mdf_3,biax_V_400,UD_C_200],[1,1,1,-1,1])

#compo_1 = laminate([UD_V_600,alu_04,mdf_3,alu_04,UD_V_600],[1,1,1,1,1])
#compo_1i = laminate([alu_04,UD_V_600,mdf_3,UD_V_600,alu_04],[1,1,1,1,1])
#compo_2 = laminate([UD_V_288,alu_06,alu_06,UD_V_288],[1,1,1,1])
#compo_3 = laminate([UD_C_140,alu_04,mdf_2,alu_04,UD_C_140],[1,1,1,1,1])
#compo_3i = laminate([alu_04,UD_C_140,mdf_2,UD_C_140,alu_04],[1,1,1,1,1])
#compo_4 = laminate([UD_C_144,alu_06,alu_06,UD_C_144],[1,1,1,1])



#print(compo_0)
#print(compo_1)
#print(compo_2)
"""
print compo_2
print compo_3
print compo_4
print compo_5
"""
