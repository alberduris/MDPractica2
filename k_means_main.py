#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys 
import k_means as K_means

def comprobarOpcionInicializacion(opc):
	if(opc!="a" and opc!="b" and opc!="c"):
		print "opcion incorrecta, solo (a),(b) o (c)"
		return False
	else:
		return True

def comprobarEntero(numClusters):
	try:
		numC = int(numClusters)
		return numC
	except ValueError:
		print "no has introducido un numero entero como numero de clusters"
		return -1 #el numero de clusters nunca va a ser negativo.
		#esta forma de programar no es muy ortodoxa pero como solo comprobamos inputs vale.

def comprobarFlotante(distanciaMinkowski):
	try:
		disM = float(distanciaMinkowski)
		return disM
	except ValueError:
		print "no has introducido un numero como distancia de minkowski"
		return -1 #la distancia de minkowski nunca va a ser negativa.
		#esta forma de programar no es muy ortodoxa pero como solo comprobamos inputs vale.

def comprobarArg4(distanciaIntergrupal):
	if(distanciaIntergrupal!="s" and distanciaIntergrupal!="c"):
		print "opcion incorrecta, solo (s) o (c)"
		return False
	else:
		return True

def comprobarArg5(criterioConvergencia):
	if(criterioConvergencia!="n" and criterioConvergencia!="d"):
		print "opcion incorrecta, solo (n) o (d)"
		return False
	else:
		return True

def comprobarCte(cte):
	try:
		const = int(cte)
		return const
	except ValueError:
		print "no has introducido un numero como constante del criterio de convergencia"
		return -1 #la cte del criterio de convergencia nunca va a ser negativa.
		#esta forma de programar no es muy ortodoxa pero como solo comprobamos inputs vale.


if __name__=="__main__":
	
	
	
	if len(sys.argv)!=7:
		print len(sys.argv)
		print "Error en el numero de argumentos."
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

		if (comprobarEntero(k) and comprobarOpcionInicializacion(ini) and comprobarFlotante(minkwsk) and comprobarArg4(inter) and comprobarArg5(crit) and comprobarCte(cte) ):

			K_means.k_means(k,ini,minkwsk,inter,crit,cte) #importar desde otro archivo .py

