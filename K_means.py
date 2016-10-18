#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@authors: Julen, Alberto, Till

"""

import numpy as np

class K_means:

    
    
    def __init__(self, numClusters, opcIni, distMink, distInt, crit, cte ): #instances,):
        print "trabajo por hacer D:"
        
    def initializeInstances(self):
        instancesFile = open('vectors_peque.txt','r')
        
        #todo - sacar las filas (100) con la cantidad de lineas que hay en el fichero
        #todo - sacar las columnas con splitted line o algo parecido
        matrix = self.initializeMatrix(100,200)
        self.imprimirMatriz(matrix)
        
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
        for i in range (self.getNumMatrixRows(matrix)):
            print ''
            for j in range(self.getNumMatrixColumns(matrix)):
                print matrix[i,j],
                if (j != self.getNumMatrixColumns(matrix)-1):
                    print ',',
        print ''
        
    
        
    def getNumMatrixRows(self,matrix):
        return len(matrix)
        
    def getNumMatrixColumns(self,matrix):
        return len(matrix[0])
            
        
                
                
            
                

    


