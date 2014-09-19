#-*- coding: utf-8 -*-
import numpy as n, networkx as x
from scipy.io import wavfile as w
g1=x.random_graphs.erdos_renyi_graph(20,.3)
g2=x.random_graphs.barabasi_albert_graph(20,6)
g1_=g1.degree()
g2_=g2.degree()
g1__=g1_.values(); g1__.sort()
g2__=g2_.values(); g2__.sort()
Lambda_tilde=Lt=(2.**5)*1024.
# Senoide
foo=n.linspace(0,2*n.pi,Lt,endpoint=False)
S_i=n.sin(foo) # um período da senóide com T amostras
D_i=n.linspace(-1,1,Lt)
Q_i=n.hstack(  ( n.ones(Lt/2)*-1 , n.ones(Lt/2) )  )
f_a=44100

def v(f=200,d=2.,tab=S_i,fv=2.,nu=2.,tabv=S_i):
    Lambda=n.floor(f_a*d)
    ii=n.arange(Lambda)
    Lv=float(len(tabv))

    Gammav_i=n.floor(ii*fv*Lv/f_a) # índices para a LUT
    Gammav_i=n.array(Gammav_i,n.int)
    # padrão de variação do vibrato para cada amostra
    Tv_i=tabv[Gammav_i%int(Lv)] 

    # frequência em Hz em cada amostra
    F_i=f*(   2.**(  Tv_i*nu/12.  )   ) 
    # a movimentação na tabela por amostra
    D_gamma_i=F_i*(Lt/float(f_a))
    Gamma_i=n.cumsum(D_gamma_i) # a movimentação na tabela total
    Gamma_i=n.floor( Gamma_i) # já os índices
    Gamma_i=n.array( Gamma_i, dtype=n.int) # já os índices
    return tab[Gamma_i%int(Lt)] # busca dos índices na tabela

f=200
f_=1.1
som=n.array([])
for gg in g1__:
    dd7=v(f=f*(f_**gg),tab=D_i,tabv=Q_i ,d=.2,fv=0.,nu=.0)
    som=n.hstack(( som, dd7))
# most music players read only 16-bit wav files, so let's convert the array
aa = n.int16(som* float(2**15-1))
w.write("musicaGrafo.wav", f_a, aa)
f=200
f_=1.1
som=n.array([])
for gg in g2__:
    dd7=v(f=f*(f_**gg),tab=D_i,tabv=Q_i ,d=.2,fv=0.,nu=.0)
    som=n.hstack(( som, dd7))
# most music players read only 16-bit wav files, so let's convert the array
aa = n.int16(som* float(2**15-1))
w.write("musicaGrafo2.wav", f_a, aa)

