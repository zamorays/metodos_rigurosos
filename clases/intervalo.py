# -*- coding: utf-8 -*- 

# from sympy import mpmath as mp
# import numpy as np

import numpy
math = numpy    # NB!

class Intervalo(object):
    """
    Se define la clase 'Intervalo', y los métodos para la aritmética básica de intervalos,
    es decir, suma, resta, multiplicación y división. Se incluyen otras funciones
    que serán útiles.
    """
    def __init__(self, lo, hi=None):
        """
        Definimos las propiedades del objeto Intervalo a partir de sus bordes,
        lo y hi, donde lo <= hi. En el caso en que el intervalo sólo tenga
        un número, éste se interpreta como un intervalo 'delgado' o 'degenerado'.
        """
        if hi is None:
            hi = lo
        elif (hi < lo):
            lo, hi = hi, lo
        
        self.lo = lo
        self.hi = hi
        
    def __repr__(self):
        return "Intervalo [{},{}]".format(self.lo,self.hi)
    
    def __str__(self):
        # Esta función sirve con 'print'
        return "[{},{}]".format(self.lo,self.hi)

    # def _repr_html_(self):
    #     return "[{}, {}]".format(self.lo, self.hi)

    def _repr_html_(self):
        reprn = "[{}, {}]".format(self.lo, self.hi)
        reprn = reprn.replace("inf", r"&infin;")
        return reprn
    
    def _repr_latex_(self):
        return "$[{}, {}]$".format(self.lo, self.hi)

    # Aquí vienen las operaciones aritméticas
    def __add__(self, otro):
        """
        Suma de intervalos
        """
        try:
            return Intervalo(self.lo + otro.lo, self.hi + otro.hi)
        except:
            return self + Intervalo(otro)

    def __radd__(self, otro):
        return self + otro
        

        
    def __mul__(self, otro):
      
        return self._mul2(otro)
      
      
      
    def _mul1(self, otro):
        try:
            S=[self.lo*otro.lo , self.lo * otro.hi , self.hi * otro.lo , self.hi * otro.hi ]
            return Intervalo( min(S), max(S) )
        except:
            return self * Intervalo(otro)

            
    def _mul2(self, otro):
        """Multiplicacion de intervalos, evaluando todos los casos posibles """
        try:
            if self.lo >= 0 :
                if otro.lo >= 0:
                    return Intervalo(self.lo * otro.lo , self.hi * otro.hi)
                elif otro.hi <= 0 :
                    return Intervalo(self.hi * otro.lo , self.lo * otro.hi)
                elif otro.lo <= 0 and otro.hi >= 0:
                    return Intervalo(self.hi * otro.lo , self.hi * otro.hi)
                
            elif self.hi <= 0:
                if otro.hi <= 0:
                    return Intervalo(self.hi * otro.hi , self.lo * otro.lo)
                elif otro.lo >= 0:
                    return Intervalo(self.lo * otro.hi , self.hi * otro.lo)
                elif otro.lo <= 0 and otro.hi >= 0:
                    return Intervalo(self.lo * otro.hi , self.lo * otro.lo) 
                     
            elif self.lo <= 0 and self.hi >= 0:
                if otro.lo >= 0:
                    return Intervalo(self.lo * otro.hi , self.hi * otro.hi)
                elif otro.hi <= 0:
                    return Intervalo(self.hi * otro.lo , self.lo * otro.lo)         
                elif otro.lo <= 0 and otro.hi >= 0:   
                    return Intervalo(min(self.hi * otro.lo , self.lo * otro.hi) , max(self.hi * otro.hi , self.lo * otro.lo))
                    
        except:
            return self * Intervalo(otro)

     
    def __rmul__(self, otro):
        return self * otro

    # Esta es la funcion igualdad para intervalos
    def __eq__(self, otro):
        """
        función igualdad para intervalos 

        """
        try:
            if self.lo == otro.lo and self.hi == otro.hi:
                return True
            else:
                return False
        except:
            if self.lo == Intervalo(otro).lo and self.hi == Intervalo(otro).hi:
                return True
            else:
                return False
  

    #interseccion
    def __and__(self, otro):
        """
        Intersección de intervalos
        Funciona con la sintaxis & (como el AND bitwise)
        """
        if not isinstance(otro,Intervalo):
            otro = Intervalo(otro)

        if (self.lo > otro.hi) | (self.hi < otro.lo):
            return None

        else:
            a = max( self.lo, otro.lo )
            b = min( self.hi, otro.hi )
            return Intervalo(a,b)
    
    #interseccion por la izquierda
    def __rand__(self, otro):
        """
        Interseccion de intervalos (por la izquierda)
        """
        return self & otro
    
    #negativo del intervalo
    def __neg__(self):
        """
        Devuelve el valor negativo del intervalo
        """
        return Intervalo(-self.hi, -self.lo)

    #Resta
    def __sub__(self, otro):
        """
        Resta de Intervalos
        """
        if not isinstance(otro, Intervalo):
            otro = Intervalo(otro)
        
        return Intervalo(self.lo - otro.hi, self.hi - otro.lo)                
        
    #Resta reversa para poder hacer (float) - Intervalo
    def __rsub__(self, otro):
        
        if not isinstance(otro, Intervalo):
            otro = Intervalo(otro)
            
        return Intervalo.__sub__(otro, self)
            
    #Funcion reciproco
    def reciprocal(self):
        """
        Devuelve un intervalo con los valores recíprocos
        """
        if self.lo <= 0 <= self.hi:
            #si el intervalo contiene el cero debe de aparecer un error
            raise ZeroDivisionError
        else:
            return Intervalo(1.0/self.hi,1.0/self.lo)

    #division con denominadores que no contienen al cero    
    def __div__(self, otro):
    	"""
        División
    	"""
        if not isinstance(otro, Intervalo):
            otro = Intervalo(otro)

        if otro.lo <= 0 <= otro.hi:
            raise ZeroDivisionError

        else:
            return self * otro.reciprocal()
    
    #división reversa
    def __rdiv__(self, otro):
        """
    	División revrsa para poder usar floats en el numerador
        """
        if not isinstance(otro, Intervalo):
            otro = Intervalo(otro)

        return Intervalo.__div__(otro, self)

    def middle(self):
        """
        Calcula el punto medio del intervalo
        """
        return (self.lo+self.hi)/2
        
    def radio(self):
        """
        Calcula el radio del intervalo
        """
        return (self.hi-self.lo)/2
        
    def width(self):
        """
        Cacula la anchura
        """

        return abs(self.hi-self.lo)
        
    def abs(self):
        
        return max([abs(self.lo),abs(self.hi)])

    
    #Relación < de intervalos.
    def __lt__(self,otro):
        """Relación < de intervalos."""
        
        try:
            return self.hi < otro.lo
        except:
            return self < Intervalo(otro)

    #Relación > de intervalos.
    def __gt__(self,otro):
        """Relación > de intervalos."""
        
        try:
            return self.lo > otro.hi
        except:
            return self > Intervalo(otro)

    #Relación <= de intervalos.
    def __le__(self,otro):
    	"""Relación <= de intervalos"""
	
        try: 
            return (self.lo <= otro.lo) and self.hi <= otro.hi	
        except: 
            return self <= Intervalo(otro)

    #Relación >= de intervalos.
    def __ge__(self,otro):
    	"""Relación >= de intervalos"""
	
        try:
            return (self.lo >= otro.lo) and self.hi >= otro.hi
        except: 
            return self >= Intervalo(otro)
    
    def hull(self, otro):
        return Intervalo(min(self.lo,otro.lo),max(self.hi,otro.hi))

        # Aquí se definirán funciones sobre intervalos        
        
    def cos(self):

        pi = math.pi

        if self.width() >= 2*pi:
            return Intervalo(-1, 1)
                        
        num, num2 = math.mod(self.lo, 2*pi), math.mod(self.hi, 2*pi)
    
        if num2 < num:
            if num >= pi:
                return Intervalo(min(math.cos(num), math.cos(num2)), 1.0)
            
            else: 
                return Intervalo(-1.0, 1.0)

        if num2>pi and num<pi:
            return Intervalo(-1, max(math.cos(num), math.cos(num2)))
    

        num = math.cos(num)
        num2 = math.cos(num2)

        if num2 < num:
            num, num2 = num2, num

        return Intervalo(num, num2)

                        
    def sin(self):
        return self.cos(self-math.pi/2)
        
        
       
    def restringir_dominio(self, dominio=None):
        """
        Función que restringe el dominio de un intervalo a valores no negativos.
        Levanta un error si el intervalo es completamente negativo.
        """

        if dominio is None:
            dominio = Intervalo(0, math.inf)

        restringido = self & dominio

        if restringido is None:
            print """Advertencia: el intervalo {} tiene interseccion vacia 
            con el dominio {}.""".format(self, dominio)

            raise ArithmeticError
            return None

        if restringido != self:
            print """Advertencia: el intervalo {} tiene interseccion no-vacia 
            con el dominio {}; restringiendo""".format(self, dominio)

        return restringido


    def log(self):
        """
        Calcula el logaritmo de un intervalo.
        """
        #try:
        #   return Intervalo(math.log(self.lo), math.log(self.hi))

        #except:

        restringido = self.restringir_dominio()

        return Intervalo(math.log(restringido.lo), math.log(restringido.hi))


    def exp(self):
        """
        Calcula la exponencial de un intervalo.
        """
    
        return Intervalo(math.exp(self.lo), math.exp(self.hi))



        
    def sqrt(self):

        restringido = self.restringir_dominio()
        return Intervalo(math.sqrt(restringido.lo),math.sqrt(restringido.hi))
            
    def arctan(self):
        return Intervalo(math.arctan(self.lo),math.arctan(self.hi))

    def tan(self):
        
        if self.width() < 2*(pi) and math.tan(self.lo) <= math.tan(self.hi):
            return Intervalo(math.tan(self.lo), math.tan(self.hi))
        else:
            print 'Advertencia: El intervalo contiene una singularidad'
            return Intervalo(float("-inf"), float("inf"))

        #funciones elementales para intervalos
      

def cos(x):
    try:
        return x.cos()
    except:
        return math.cos(x)
        
def sin(x):
    try:
        return x.sin()
    except:
        return math.sin(x)

def tan(x):
    try:
        return x.tan()
    except:
        return math.tan(x)

def exp(x):
    try:
        return x.exp()
    except:
        return math.exp(x)
        
def log(x):
    try:
        return x.log()
    except:
        return math.log(x)

def sqrt(x):
    try:
        return x.sqrt()
    except:
        return math.sqrt(x)