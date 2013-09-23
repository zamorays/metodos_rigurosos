# -*- coding: utf-8 -*- 

# Escribimos funciones con el nombre test_ALGO
from sympy import mpmath as mp
from intervalo import sin, cos, sqrt, Intervalo
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def partIntervalo(intervalo, n):
  nInterv    = np.linspace(intervalo.lo,intervalo.hi, n+1)
  listInterv = [Intervalo(nInterv[i],nInterv[i+1]) for i in range(n)]
  return listInterv
  
def plotFIntevalo(listInterv,Fx=None):
  rnd = np.random.uniform(0.,1.,3)
  nlen = len(listInterv)
  if Fx != None:
    listFx=Fx(listInterv)
    plotF = plt.figure()
    ax = plotF.add_subplot(111)
    plt.plot(np.linspace(listInterv[0].lo,listInterv[-1].hi,100),Fx(np.linspace(listInterv[0].lo,listInterv[-1].hi,100)),color=(rnd[0],rnd[1],rnd[2]))
    #rect=matplotlib.patches.Rectangle((listInterv[0].lo,listFx[0].lo),listInterv[0].width(),listFx[0].width(),color=(rnd[2],rnd[0],rnd[1]),alpha=0.2)
    #ax.add_patch(rect)
    pltrec = [matplotlib.patches.Rectangle((listInterv[i].lo,listFx[i].lo),listInterv[i].width(),listFx[i].width(),color=(rnd[2],rnd[0],rnd[1]),alpha=0.2) for i in range(nlen)]
    recs   = [ax.add_patch(rec) for rec in pltrec]
    plt.ylim(min(listFx).lo,max(listFx).hi)
    return plotF,listFx
  
  else:
    plotF = plt.figure(1)
    #plt.Rectangle((,))
    plt.plot(np.linspace(listInterv[0].lo,listInterv[-1].hi,100),np.cos(np.linspace(listInterv[0].lo,listInterv[-1].hi,100)),color=(0,0,0))
    return plotF