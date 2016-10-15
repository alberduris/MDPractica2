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
        return numC
    except ValueError:
        print "No has introducido un numero entero como numero de clusters"
        return -1 #el numero de clusters nunca va a ser negativo.
        #esta forma de programar no es muy ortodoxa pero como solo comprobamos inputs vale.
"""
@post: Comprueba que el parámetro para calcular la distancia Minkowski es correcto (cualquier float >= 0)
"""
def comprobarFlotante(distanciaMinkowski):
    try:
        disM = float(distanciaMinkowski)
        return disM
    except ValueError:
        print "no has introducido un numero como distancia de minkowski"
        return -1 #la distancia de minkowski nunca va a ser negativa.
        #esta forma de programar no es muy ortodoxa pero como solo comprobamos inputs vale.
"""
@post: Comprueba que se ha elegido una de las opciones disponibles para la distancia intergrupal siendo:
s = Single-Link
c = Complete-Link
"""
def comprobarDistanciaIntergruapl(distanciaIntergrupal):
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
    #TODO: Recoger y comprobar el umbral de disimilitud
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
        return const
    except ValueError:
        print "No has introducido un numero como constante del criterio de convergencia"
        return -1 #la cte del criterio de convergencia nunca va a ser negativa.
        #esta forma de programar no es muy ortodoxa pero como solo comprobamos inputs vale.


if __name__=="__main__":
    
    
    print 'K-means'
    if len(sys.argv)!=7:
        print "Numero de argumentos: " + str(len(sys.argv))
        print "Error en el numero de argumentos. Deben ser 7."
        print "(arg[0] -> self)"
        print "1er argumento: numero de clusters k."
        print "2do argumento: tipo de inicializacion; 'a','b' o 'c'."
        print "3er argumento: distancia de minkowski (numero real)."
        print "4to argumento: distancia intergrupal 's' o 'c'."
        print "5to argumento: criterio de convergencia 'n' o 'd'."
        print "6to argumento: constante correspondiente al criterio de convergencia."
    
        print "biblia sobre cada una de las opciones..."

    else:

        #asignaciones
        k = sys.argv[1]
        ini = sys.argv[2]
        minkwsk = sys.argv[3]
        inter = sys.argv[4]
        crit = sys.argv[5]
        cte = sys.argv[6]
        #mas las instancias!!.....

    if (comprobarEntero(k) and comprobarOpcionInicializacion(ini) and comprobarFlotante(minkwsk) and comprobarDistanciaIntergruapl(inter) and comprobarCriterioConvergencia(crit) and comprobarCte(cte)):

        K_means.K_means(k,ini,minkwsk,inter,crit,cte) #importar desde otro archivo .py

