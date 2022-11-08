from sympy import *
from sympy.physics.continuum_mechanics.beam import Beam
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from matplotlib import style

style.use('ggplot')
init_printing()


#Determina o poligno
P = Polygon([[0, 0], [1, 0], [1, 1], [0, 1]])
C= P.centroid

print(C)

# Determina as reações R1, R2
R1, R2 = symbols('R1 R2')

# Propriedade da viga [cm]
bw = 14
h = 50
d = 46

#Inércia [cm4]
I = (1/12) * bw * h**3
#Módulo de elasticidade [kN/cm²]
E = 2500
#Resistência característica do concreto a compressão [MPa]
fck = 25
#Resistência de cáldulo do concreto a compressão [MPa]
fcd = fck/1.4/10
#Resistência média do concreto á tração direta[MPa]
fctm = 0.3 * ((fck)**(2/3))
#Resistência do concreto á tração direta [MPa]
fctd = 0.7 * fctm / 1.4

#Tensão na armadura transversal caracteristica
fywk = 50

#Carga [kN/m]
load = 43.7

# Comprimento da viga [m], módulo de elasticidade [kN/cm²], inércia [cm4]
b = Beam(5, E, I)

#Função aplica carga na viga
#Primeiro argumento é a carga
#Segundo argumento é o ponto de início(x=0)
#Terceiro argumento é o grau da carga
#Quarto argumento é o ponto final (x=5)
b.apply_load(load, 0, 0, end=5)

#Aplica uma reação desconhecida em R1 na posição x=0.
#O terceiro argumento indica que a carga é um ponto (valor = -1)
b.apply_load(R1, 0, -1)

#Aplica uma reação desconhecida em R1 na posição x=5.
#O terceiro argumento indica que a carga é um ponto (valor = -1)

b.apply_load(R2, 5, -1)

#Adiciona um suporte fixo para as seguintes cordenadas x=0 e x=5, dizendo que a deflexão será 0
b.bc_deflection = [(0, 0), (5, 0)]

#Cálcula a reação nos apoios 
b.solve_for_reaction_loads(R1, R2)

#Máximo cortante
vk = b.max_shear_force()
vk = float(vk[1])
print("Vk: " + str(round(vk,2)) + "kN")

#Esforço cortante solicitante de cálculo
vsd = 1.4*vk
print("Vsd: " + str(round(vsd,2)) + "kN")

#Modelo de cálculo I
vrd2 = 0.27 * (1-fck/250) * fcd * bw * d
print("Vrd2: " + str(round(vrd2,2)) + "kN")

#Cálculo da armadura transversal
aswmin = 20 * fctm/10 * bw / fywk
print("Asw,min: " + str(round(aswmin,2)) + "cm2/m")

#Parcela cortante
vc = 0.6 * fctd/10 * bw * d
print("Vc: " + str(round(vc,2)) + "kN")

#Parcela força cortante solicitante a ser resistida pelos estribos
vsw = vsd - vc
print ("Vsw: " + str(round(vsw,2)) + "kN")

asw90 = 100 * vsw / (39.2 * d)
print("Asw,90: " + str(round(asw90,2)) + "cm2/m")

#Plota os resultados
b.plot_loading_results()