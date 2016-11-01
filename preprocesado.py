#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys 
import K_means as K_means

"""
@post: Comprueba que se ha elegido una de las opciones de inicialización disponibles siendo:
a) Aleatoria
b) Por división del espacio
c) Generar 2k clusters y de sus centroides elegir los k más separados entre sí
"""
def comprobarOpcionInicializacion(opc):
    if(opc!="a" and opc!="b" and opc!="c"):
        print "Opcion incorrecta, solo (a),(b) o (c)"
        return False
    else:
        return True
"""
@post: Comprueba que el número de clusters es correcto (cualquier entero >= 1)
"""
def comprobarEntero(numClusters):
    try:
        numC = int(numClusters)
        if (numC == 0):
            print "El numero de clusters no puede ser cero, introduce un numero de clusters entero positivo mayor que cero"
            return False
        return numC
    except ValueError:
        print "No has introducido un numero entero como numero de clusters"
        return False #el numero de clusters nunca va a ser negativo.
        #esta forma de programar no es muy ortodoxa pero como solo comprobamos inputs vale.
"""
@post: Comprueba que el parámetro para calcular la distancia Minkowski es correcto (cualquier float >= 0)
"""
def comprobarFlotante(distanciaMinkowski):
    try:
        disM = float(distanciaMinkowski)
        if(disM < 0):
            print "El parámetro p de la distancia Minkowski debe ser p > 0 || p = 0 para distancia Coseno"
            return False
        return True
    except ValueError:
        print "No has introducido un numero como distancia de minkowski"
        return False #la distancia de minkowski nunca va a ser negativa.
        #esta forma de programar no es muy ortodoxa pero como solo comprobamos inputs vale.
"""
@post: Comprueba que se ha elegido una de las opciones disponibles para la distancia intergrupal siendo:
s = Single-Link
c = Complete-Link
"""
def comprobarDistanciaIntergrupal(distanciaIntergrupal):
    if(distanciaIntergrupal!="s" and distanciaIntergrupal!="c"):
        print "opcion incorrecta, solo (s) o (c)"
        return False
    else:
        return True
"""
@post: Comprueba que se ha elegido una de las opciones disponibles para el criterio de convergencia siendo:
n = Número de iteraciones fijo
d = Disimilitud
"""
def comprobarCriterioConvergencia(criterioConvergencia):
    
    if(criterioConvergencia!="n" and criterioConvergencia!="d"):
        print "opcion incorrecta, solo (n) o (d)"
        return False
    else:
        return True
"""
@post: Comprobar que se ha introducido un numero como constante para el criterio de convergencia (En caso de haber elegido "Numero de iteraciones fijo")
"""
def comprobarCte(cte):
    try:
        const = int(cte)
        if(const <= 0):
            print "El numero de iteraciones fijas debe ser > 0"
            return False
        return const
    except ValueError:
        print "No has introducido un numero como constante del criterio de convergencia"
        return False #la cte del criterio de convergencia nunca va a ser negativa.
        #esta forma de programar no es muy ortodoxa pero como solo comprobamos inputs vale.

"""
@post: Comprobar que se ha introducido un numero como constante para el criterio de convergencia (En caso de haber elegido "Numero de iteraciones fijo")
"""
def comprobarUmbral(umbral):
    try:
        umbral = float(umbral)
        if(umbral <= 0):
            print "El umbral debe ser > 0"
            return False
            
        return umbral
    except ValueError:
        print "No has introducido un numero como constante del criterio de convergencia"
        return False #la cte del criterio de convergencia nunca va a ser negativa.
        #esta forma de programar no es muy ortodoxa pero como solo comprobamos inputs vale.
        
def comprobarPrincipal(k,ini,minkwsk,inter,crit,terminacion):
    #Comprobación criterio de terminación
    #Si el criterio es n entonces comprobar numero fijo de it.
    #Si el criterio es d entonces comprobar umbral
        if (crit == "n"):#Numero de iteraciones fijo
        
            if (comprobarEntero(k) and comprobarOpcionInicializacion(ini) 
            and comprobarFlotante(minkwsk) and comprobarDistanciaIntergrupal(inter) 
            and comprobarCte(terminacion)):
                return True
            else:
                return False
                
        else:
            
            if (comprobarEntero(k) and comprobarOpcionInicializacion(ini) 
            and comprobarFlotante(minkwsk) and comprobarDistanciaIntergrupal(inter) 
            and comprobarUmbral(terminacion)):
                #importar desde otro archivo .py
                return True
            else:
                return False
                
                
def preMain():
    print '***K-means***'
    if len(sys.argv)<7:
        print "Numero de argumentos: " + str(len(sys.argv))
        print "Error en el numero de argumentos. Deben ser 7."
        print "(arg[0] -> self)"
        print "1er argumento: numero de clusters k."
        print "2do argumento: tipo de inicializacion; 'a','b' o 'c'."
        print "3er argumento: distancia de minkowski (numero real)."
        print "4to argumento: distancia intergrupal 's' o 'c'."
        print "5to argumento: criterio de convergencia 'n' o 'd'."
        print "6to argumento: Constante o umbral correspondiente al criterio de convergencia."
    
        
        

    else:
        
        if(comprobarPrincipal(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6])):  
            return True        
        
        #if(comprobarPrincipal(k,ini,minkwsk,inter,crit,terminacion)):  
            #return True
    
    

if __name__=="__main__":
    
    print 'Preprocesado main'
            
def test1():
    print '***K-means***'
    if len(sys.argv)!=7:
        print "Numero de argumentos: " + str(len(sys.argv))
        print "Error en el numero de argumentos. Deben ser 7."
        print "(arg[0] -> self)"
        print "1er argumento: numero de clusters k."
        print "2do argumento: tipo de inicializacion; 'a','b' o 'c'."
        print "3er argumento: distancia de minkowski (numero real)."
        print "4to argumento: distancia intergrupal 's' o 'c'."
        print "5to argumento: criterio de convergencia 'n' o 'd'."
        print "6to argumento: Constante o umbral correspondiente al criterio de convergencia."
    
        
        

    else:
        
        
        #asignaciones
        k = sys.argv[1]
        ini = sys.argv[2]
        minkwsk = sys.argv[3]
        inter = sys.argv[4]
        crit = sys.argv[5]
        terminacion = sys.argv[6]
        #mas las instancias!!.....
        
        if(comprobarPrincipal(k,ini,minkwsk,inter,crit,terminacion)):  
            km = K_means.K_means(k,ini,minkwsk,inter,crit,terminacion)
            km.initializeInstances('vectors_muy_peque.txt')
            
        
        
                
                
                
        
        
            
            
            

        

        

