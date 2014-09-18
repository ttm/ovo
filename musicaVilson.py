#-*- coding: utf-8 -*-
import numpy as n
from scipy.io import wavfile as w

f_a = 44100  # Hz, frequência de amostragem

############## 2.2.1 Tabela de busca (LUT)
# tamanho da tabela: use par para não conflitar abaixo
# e ao menos 1024
Lambda_tilde = Lt = 1024

# Senoide
foo = n.linspace(0, 2*n.pi, Lt, endpoint=False)
S_i = n.sin(foo)  # um período da senoide com T amostras

# Quadrada:
Q_i = n.hstack((n.ones(Lt/2)*-1, n.ones(Lt/2)))

# Triangular:
foo = n.linspace(-1, 1, Lt/2, endpoint=False)
Tr_i = n.hstack((foo, foo*-1))

# Dente de Serra:
D_i = n.linspace(-1, 1, Lt)

# som real, importar período e
# usar T correto: o número de amostras do período

f = 110.  # Hz
Delta = 3.4  # segundos
Lambda = int(Delta*f_a)

# Amostras:
ii = n.arange(Lambda)


############## 2.2.5 Tremolo e vibrato, AM e FM
# VEJA: vibrato.py e tremolo.py para as figuras 2.19 e 2.20
f = 220.
Lv = 2048  # tamanho da tabela do vibrato
fv = 1.5  # frequência do vibrato
nu = 1.6  # desvio maximo em semitons do vibrato (profundidade)
Delta = 5.2  # duração do som
Lambda = int(Delta*f_a)

# tabela do vibrato
x = n.linspace(0, 2*n.pi, Lv, endpoint=False)
tabv = n.sin(x)  # o vibrato será senoidal

ii = n.arange(Lambda)  # índices
### 2.56 índices da LUT para o vibrato
Gammav_i = n.array(ii*fv*float(Lv)/f_a, n.int)  # índices para a LUT
### 2.57 padrão de oscilação do vibrato para cada amostra
Tv_i = tabv[Gammav_i % Lv]
### 2.58 frequência em cada amostra
F_i = f*(2.**(Tv_i*nu/12.))
### 2.59 índices para LUT do som
D_gamma_i = F_i*(Lt/float(f_a))  # movimentação na tabela por amostra
Gamma_i = n.cumsum(D_gamma_i)  # a movimentação na tabela total
Gamma_i = n.array(Gamma_i, dtype=n.int)  # já os índices
### 2.60 som em si
T_i = Tr_i[Gamma_i % Lt]  # busca dos índices na tabela

T_i = n.int16(T_i * float(2**15-1))
w.write("vibrato.wav", f_a, T_i)  # escrita do som

ff=open("output.txt","rb")
aa=ff.readlines()
aa_=[]
for medida in aa:
    medidas=[float(i) for i in medida[1:-2].split(",")]
    aa_.append(medidas)
aa__=n.array(aa_)
for i in xrange(aa__.shape[1]):
    aa__[:,i]=(aa__[:,i]-aa__[:,i].mean())/(aa__[:,i].std())
# 20 medidas por segundo
# uma medida a cada 50ms
# 0.005*44100 amostras
# total de 44100*0.005*len(aa)
contador=0
passo=0.05*44100
amostras=passo*len(aa)
T_i=n.array([])
for medida in aa__:
    #medidas=[float(i) for i in medida[1:-2].split(",")]
    ainicial=int(passo*contador)
    afinal=int(passo*(contador+1))
    #tamostras = n.arange(ainicial,afinal):
    tamostras = n.arange(passo)
    
    ### 2.56 índices da LUT para o vibrato
    # fazer fv depender de parametro
    fv=5+medida[1]
    Gammav_i = n.array(tamostras*fv*float(Lv)/f_a , n.int)+Gammav_i[-1]  # índices para a LUT
    ### 2.57 padrão de oscilação do vibrato para cada amostra
    Tv_i = tabv[Gammav_i % Lv]
    ### 2.58 frequência em cada amostra
    # fazer nu depender de parametro
    nu=4+medida[2]
    # f depender de parametro
    F_i = f*(2.**(Tv_i*nu/12.))
    ### 2.59 índices para LUT do som
    D_gamma_i = F_i*(Lt/float(f_a))  # movimentação na tabela por amostra
    Gamma_i_ = n.cumsum(D_gamma_i)  # a movimentação na tabela total
    Gamma_i = n.array(Gamma_i_, dtype=n.int)+Gamma_i[-1]  # já os índices
    ### 2.60 som em si
    T_i_ = Tr_i[Gamma_i % Lt]  # busca dos índices na tabela
    # fazer amplitude depender de parametro

    T_i = n.hstack(( T_i, n.int16(T_i_ * float(2**15-1)) ))
    contador+=1
T_i = n.int16(T_i * float(2**15-1))
w.write("vibrato2.wav", f_a, T_i)  # escrita do som



