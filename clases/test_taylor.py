# -*- coding: utf-8 -*- 

from taylor import *
from sympy import series, symbols,simplify,factorial

x = symbols('x')

fx = 1. + 2.*x**2 + 3.*x**3 + 4.*x**4 + 5.*x**5 + 9.*x**9
gx = 6. + x**3 + 6.*x**7
hx = 5.*x**4
mx = 3.*x**8
sx = 1.+x
orden = 35
a = 1.*taylorDiff([1.,0.,2.,3.,4.,5.,0,0,0,9.],orden)
b = 1.*taylorDiff([6.,0,0,1.,0,0,0,6.,0],orden)
c = 1.*taylorDiff([0,0,0,0,5.,0,0,0],orden)
d = 1.*taylorDiff([0,0,0,0,0,0,0,0,3.],orden)
e = 1.*taylorDiff([1,2,3,4,5,6,7,8],7)
f = 1.*taylorDiff([9,10,11,12,13,14,15,16],7)
s = 1.*taylorDiff([1,1,0,0,0,0,0,0],7)
ss= 1.*taylorDiff([0,1,0,0,0,0,0,0],7)

##################################
#ERROR EN EL ORDEN 0 
##################################

def test_sum():
  aux=[]
  for i in range(orden):
    if (fx+gx).coeff(x**i) == None:
        aux.append(0.0)
    else:
        aux.append((fx+gx).coeff(x**i))

  #print aux
  assert (a+b).jet.all() == np.array(aux).all()
  #ans = np.array(range(apx1)).resize(apx2) + np.array(range(apx2))
  #assert (a+b).jet.all() == np.array(ans).all()
  

def test_dif():
  aux=[]
  for i in range(orden):
    if (fx-hx).coeff(x**i) == None:
        aux.append(0.0)
    else:
        aux.append((fx-hx).coeff(x**i))
        
  #print aux
  assert ((a-c).jet).all() == (np.array(aux)).all()
  #ans = np.array(range(apx1)).resize(apx2) + np.array(range(apx2))
  #assert (a+b).jet.all() == np.array(ans).all()
  
def test_mul():
  
  aux=[]
  for i in range(orden):
    if (fx*gx).coeff(x**i) == None:
        aux.append(0.0)
    else:
        aux.append((fx*gx).coeff(x**i))

  #print aux
  assert (a*b).jet.all() == (np.array(aux)).all()
  
def test_div():
  
  # t/c
  aux=[]
  for i in range(orden):
    if (fx/5.).coeff(x**i) == None:
        aux.append(0.0)
    else:
        aux.append((fx/5.).coeff(x**i))
        
  assert (a/5.).jet.all() == np.array(aux).all()
  ## c/t
  #invfx = series(5./gx,x,n=orden).expand()
  #for i in np.arange(orden):
    #if invfx.coeff(x**i) == None:
        #aux.append(0.0)
    #else:
        #aux.append(invfx.coeff(x**i))
        
  #print aux
  
  # t/t
  
  fgx = series(fx/gx,x,n=orden)
  #ERROR
  aux = [1/6.]
  for i in range(1,orden+1):
    if fgx.coeff(x**i) == None:
        aux.append(0.0)
    else:
        aux.append(fgx.coeff(x**i))
        
  ab = a/b
  assert ab.jet[0:20].all() == np.array(aux)[0:20].all()
  print ab.jet[0:20].all() == np.array(aux)[0:20].all()

def test_pow():
  power = 5.3
  pwsx = series(sx**power,x,n=orden)
  aux = [1**power]
  for i in range(1,orden+1):
    if pwsx.coeff(x**i) == None:
      aux.append(0.0)
    else:
      aux.append(pwsx.coeff(x**i))
  
  #print aux
  s.extendOrd(orden)
  assert (s**5.3).jet[1:orden].all() == np.array(aux)[1:orden].all()