#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@authors: Julen, Alberto, Till

"""

import numpy as np

class K_means:

    
    
    def __init__(self, numClusters, opcIni, distMink, distInt, crit, cte ): #instances,):
        print "trabajo por hacer D:"
        
    def initializeInstances(self,instancesFileName):
        instancesFile = open(instancesFileName,'r')
        
        
        matrix = self.initializeMatrix(self.getNumFileRows(instancesFileName),
                                       self.getNumFileColumns(instancesFileName))
        
        j = -1
        for line in instancesFile:
            j = j + 1
            splittedLine = line.split()
            for i in range(1,len(splittedLine)):
                column = splittedLine[i]
                matrix[j,i-1] = float(column)
                
        self.imprimirMatriz(matrix)
        np.savetxt('output.txt',matrix,delimiter=',')
        

    '''
    @post: Inicializa una matriz de ceros
    @note: Por el momento la dimension se indica 'hardcoded'
    '''
    def initializeMatrix(self,columns,rows):
        matrix = np.ndarray(shape=(columns,rows))
        matrix.fill(0)
        return matrix        
    
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
    
    k = K_means(1,2,3,4,5,6)
    print k.getNumFileRows("vectors_peque.txt")
    print k.getNumFileColumns("vectors_peque.txt")




#Métodos para pruebas - En realidad no son métodos
#se trata de copiar el cuerpo del método al main y ejecutar
#pero es una manera cómoda de poner varias lineas sin
#molestar y sin hacer un comentario multilinea feo
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
    

