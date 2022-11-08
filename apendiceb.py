import math

#Dimensionamento de seções retangulares à Torção combinada com Flexão e Esforço Cortante

#Resistência característica à compressão do concreto em MPa
fck = 20

#Tensão de escoamento característica do aço em MPa
fyk = 500

#Módulo de elasticidade do aço em GPa
es = 200

#Coeficientes parciais de segurança do concreto
gamac = 1.4

#Coeficientes parciais de segurança do aço
gamas = 1.15

#Coeficientes parciais de segurança para momento fletor
gamaf = 1.4

#Coeficiente beta de redistribuição de momentos
bduct = 1.0

#Largura da seção transversal em cm
b = 25

#Altura da seção transversal em cm
h = 40

#Parâmentro d em cm
dl = 4

#Momento fletor de serviço em kKm
amk = 11.03

#Esfroço cortante em kN
vk = 17.36

#Momento torçor em kNm
tk = 9.6

#Parâmentros do diagrama retangular

if (fck<=50):
    alamb = 0.8
    alfac = 0.85
    eu = 3.5
    qlim = 0.8*bduct-0.35
else:
    alamb = 0.8 - (fck-50)/400
    alfac = 0.85*(1-(fck-50)/200)
    eu = 2.6 + 35*((90-fck/100))**4
    qlim = 0.8*bduct-0.35

#Conversão de unidades de kN e cm
amk = 100*amk
tk = 100*tk
es = 100*es

#Resistências de cálculo em kN/cm2
fcd = fck/(10*gamac)
tcd = alfac*fcd
fyd = fyk/(10*gamas)

#Esforços solicitantes de cálculo
amd = gamaf*amk
vd = gamaf*vk
td = gamaf*tk

#Altura útil
d = h-dl

#Parâmetro geométrico
delta=dl/d

#Dimensionamento ao esforço cortante e torção

#Verificação do esmagamento das bielas considerando a superposição das tensões
#Parcela devida ao esforço cortante
bw = b

#Tensão convencional de cisalhamento
twd = vd/(bw*d)
#Passando para MPa
twd = 10*twd

#Tensão de cisalhamento última

fcd = 10*fcd
av = 1-fck/250
twu = 0.27*av*fcd

#Parcela devida ao momento torçor

#Parâmetros da seção vazada equivalente
#t0 = espessura da parede da seção vazada
#ae = área limitada pela linha média
#up = perímetro da linha média
c1 = dl
t0 = b*h/(2*(b+h))
if (t0 >= 2*c1):
    t = t0
    ae = (b-t)*(h-t)
    up = 2*(b-h-2*t)
else:
    t = t0
    tmax = b - 2*c1
    if (t>tmax):
        t = tmax
    ae = (b-2*c1)*(h-2*c1)
    up = 2*(b+h-4*c1)

#Tensão convencional de cisalhamento
ttd = td/(2*ae*t)
#Passando para MPa
ttd = 10*ttd

#Tensão de cisalhamento última
ttu = 0.25*av*fcd

#Combinação das tensões e verificação
soma = ttd/ttu + twd/twu

if(soma>1):
    print("Esmagamento da biela de compressão. Aumente as dimensões da seção transversal")

#Espaçamento máximo dos estribos

if(soma<=0.67):
    smax = 0.6*d
if(smax>30):
    smax=30
else:
    smax=0.3*d
    if(smax>20):
        smax=20

#Dimensionamento das armaduras para esforço cortante
#Tensão Talc de redução da armadura
if (fck<=50):
    a= 2/3
    tc = 0.126*(fck**a)/gamac
else:
    tc=0.8904*math.log(1+0.11*fck)/gamac

#Tensão Tald para cálculo da armadura

tald = 1.11*(twd-tc)
if (tald<0):
    tald=0
#Limitação da tensão de escoamento do aço conforme a NBR-6118
if (fyd>435):
    fyd=435

#Cálculo da armadura
aswv = 100*bw*tald/fyd

#Dimensionamento das armaduras para o momento torçor
fyd = fyd/10
aswt = 100*td/(2*ae*fyd)
aslt = td*up/(2*ae*fyd)

#Cálculo da armadura mínima:
#A tensão fyd dever menor ou igual a 500MPa
fykmax = fyk
if(fykmax>500):
    fykmax = 500

#Resistência média á tração do concreto
if(fck<=50):
    a=2/3
    fctm=0.3*(fck**a)
else:
    fctm=2.12*math.log(1+0.11*fck)

#Taxa mínima de armadura
rowmin = 0.2*fctm/fykmax

#Superposição dos estribos
asw = aswv + 2*aswt
aswmin = rowmin*100*bw
if(asw<aswmin):
    asw = aswmin

#Armadura longitudinal mínima da torção
aslmin = 0.5*rowmin*up*bw
if(aslt<aslmin):
    aslt=aslmin

#Mostrando os resultados na tela
print("Estribos de dois ramos: ",)
print("Para o cortante[cm2/m] ",round(aswv/10,2))
print("Para o torçor[cm2/m]: ",round(aswt/10,2))
print("Total[cm2/m]: ", round(asw/10,2))
print("Espaçamento máximo[cm]: ",round(smax,2))
print("Armadura longitudinal para o torçor[cm2]: ", round(aslt/10,2))