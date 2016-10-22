#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@authors: Julen, Alberto, Till

TODO: ASIGNAR CENTROIDE MÁS CERCANO MODIFICANDO LA MATRIZ DE PERTENENCIA
TODO: DISTANCIAS INTERGRUPALES
TODO: K-MEANS JAJA
"""
import sys 
import numpy as np
import numpy.random as random
import Preprocesado as Preprocesado

class K_means:
    
   
            
    def __init__(self, numClusters, opcIni, distMink, distInt, crit, cte ):
        print "trabajo por hacer D:"
        
    

    '''
    @post: Inicializa dos matrices
        -La matriz de instancias que contiene los atributos de cada instancia (vectores de las palabras)
        -La matriz de clusters que contiene los centroides (vectores de los centroides)
    '''
    def initializeMatrixes(self,instancesFileName):
        instancesFile = open(instancesFileName,'r')
        
        numFileRows = self.getNumFileRows(instancesFileName)
        numFileColumns = self.getNumFileColumns(instancesFileName)
        
        #Inicializar matriz de instancias
        instancesMatrix = self.initializeInstancesMatrix(instancesFile,numFileRows,numFileColumns-1)
        
                
        #Inicializar matriz de clusters con ceros
        clustersMatrix = self.setRandomCentroids(numFileColumns-1,instancesMatrix)        
        
        #Crear matriz de pertenencia
        membershipMatrix = self.createMembershipMatrix(numFileRows,int(sys.argv[1]))
        self.imprimirMatriz(membershipMatrix)        
        
        return instancesMatrix,clustersMatrix
        
        
        

    '''
    @post: Inicializa la matriz de las instancias
    '''
    def initializeInstancesMatrix(self,instancesFile,numFileRows,numFileColumns):
        instancesMatrix = self.initializeMatrix(numFileRows,numFileColumns)
            
        j = -1
        for line in instancesFile:
            j = j + 1
            splittedLine = line.split()
            for i in range(1,len(splittedLine)):
                column = splittedLine[i]
                instancesMatrix[j,i-1] = float(column)
        
        return instancesMatrix
        
    '''
    @post: Asigna los centroides iniciales asignando como centroides la 
    posición de k instancias al azar
    '''
    def setRandomCentroids(self,numFileColumns,instancesMatrix):
        clustersMatrix = self.initializeMatrix(int(sys.argv[1]),numFileColumns)
        
        for i in range (0,int(sys.argv[1])):
        
            instanceNum = random.randint(0,self.getNumMatrixRows(instancesMatrix))
            clustersMatrix[i,:] = self.getVector(instanceNum,instancesMatrix)
            
        return clustersMatrix
        
    '''
    @post: Inicializa una matriz de ceros con las dimensiones pasadas por params
    '''
    def initializeMatrix(self,rows,columns):
        matrix = np.ndarray(shape=(rows,columns))
        matrix.fill(0)
        return matrix
    
    '''
    @post: Crea la matriz de pertenencia inicial, con tantas columnas como clusters y 
    tantas filas como instancias. Se rellena con ceros.
    '''
    def createMembershipMatrix(self,rows,columns):
        membershipMatrix = np.ndarray(shape=(rows,columns),dtype=int)
        membershipMatrix.fill(0)
        return membershipMatrix

     
    '''
    @post: Imprime el shape, el size y el contenido de una matriz
    '''
    def imprimirMatriz(self,matrix):
        print 'Printing matrix'        
        print 'Matrix shape: ',
        print matrix.shape
        print 'Matrix size: ',
        print matrix.size
        
        numMatrixRows = self.getNumMatrixRows(matrix)
        numMatrixColumns = self.getNumMatrixColumns(matrix)      
        
        for i in range (numMatrixRows):
            print ''
            for j in range(numMatrixColumns):
                if(i == 0 and j == 0):
                    print '{',
                print matrix[i,j],
                if(i == numMatrixRows-1 and j == numMatrixColumns-1):
                    print '}',
                if (j != numMatrixColumns-1):
                    print ',',
        print ''
        
    
     
    '''
    @post: Devuelve en numero de filas de la matriz pasada por param
    '''
    def getNumMatrixRows(self,matrix):
        return len(matrix)
    '''
    @post: Devuelve en numero de columnas de la matriz pasada por param
    ''' 
    def getNumMatrixColumns(self,matrix):
        return len(matrix[0])

    '''
    @post: Devuelve en numero de lineas del fichero pasado por param
    '''  
    def getNumFileRows(self,file_name):
        with open(file_name) as instancesFile:
            for i,line in enumerate(instancesFile):
                pass
        return i+1
        
    '''
    @post: Devuelve en numero de columnas del fichero pasado por param
    '''  
    def getNumFileColumns(self,file_name):
        instancesFile = open(file_name,'r')        
        line = instancesFile.readline()
        splLine = line.split()
        return len(splLine)
        
       
    '''
    @post: Devuelve el vector de tipo np.array que esta en la fila i de la matriz matrix
    '''
    def getVector(self,i,matrix):
        return matrix[i,::] 

        
            
    '''
    Quizas convendría establecer un tipo de datos propio puesto que los valores de los vectores tienen sólo 6 decimales 
    (float16 de numpy se nos queda un poco grande) // Preguntarle a Alicia si eso le va a ahorrar tiempo al algoritmo.
    https://docs.python.org/2/extending/newtypes.html
    
    Alber: Me parece interesante, pero quizás sea demasiado para esta práctica.
    '''    

    '''
    @pre: alfa numero real no negativo, vectores 1 y 2 del tipo np.array() (¿a los que previamente se les ha extraido la clase?)
    @note: interesa que este metodo sea muy eficiente, surgen muchas dudas
    @post: 
    '''      
    def getDistance(self,alfa,vector1,vector2):
        return np.sum(np.absolute(vector1-vector2)**alfa)**(float(1)/alfa)
        

#para pruebas
if __name__=="__main__":
    print 'K_means : main'
    
    if (Preprocesado.preMain()):
        print 'Parámetros correctos'
        
        k = sys.argv[1]
        ini = sys.argv[2]
        minkwsk = sys.argv[3]
        inter = sys.argv[4]
        crit = sys.argv[5]
        terminacion = sys.argv[6]

        kmeans = K_means(k,ini,minkwsk,inter,crit,terminacion)
        instancesMatrix,clustersMatrix = kmeans.initializeMatrixes("vectors_peque.txt")
        
        #kmeans.imprimirMatriz(instancesMatrix)
        #print 'Imprimir Matriz Clusters'
        #kmeans.imprimirMatriz(clustersMatrix)
        
        
        
        
    
    else: #Parámetros incorrectos
        
        print ''
        
        
    
    
    
    
    




'''
Métodos para pruebas - En realidad no son métodos
se trata de copiar el cuerpo del método al main y ejecutar
pero es una manera cómoda de poner varias lineas sin
molestar y sin hacer un comentario multilinea feo
'''
def test1():
    vec1=np.array([0.423481, 0.369929, 1.111249, 0.013840, 1.331685])
    vec2=np.array([0.347326, 0.256732, 0.978557, 0.664598, 1.915115])
    k = K_means(1,2,3,4,5,6)
    dist = K_means.getDistance(k,1,vec1,vec2)
    print "distancia: " + str(dist)
    dist = K_means.getDistance(k,2,vec1,vec2)
    print "distancia: " + str(dist)
    
def test2():
    k = K_means(1,2,3,4,5,6)
    print k.getNumFileRows("vectors_muy_peque.txt")
    print k.getNumFileColumns("vectors_muy_peque.txt")
    
def test3():
    k = K_means(1,2,3,4,5,6)
    matrix = k.initializeInstances("vectors_muy_peque.txt")
    
    vector1 = k.getVector(matrix,3)
    print vector1
    

