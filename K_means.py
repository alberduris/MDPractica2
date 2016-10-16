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
        matrix = np.ndarray(shape=(100,201))    
        
        j = -1 
        for line in instancesFile:
            j = j + 1
            splittedLine = line.split()
            print str(j)+":"; print splittedLine
            for i in range(1,len(splittedLine)):
                column = splittedLine[i]
                print "i:"+str(i)+" column:"+ str(column)
                matrix[j,i] = float(column)
                print 'Matrix[j,i]:'+str(matrix[j,i])
                
        print matrix[99::]
        
        np.savetxt('output.txt',matrix,delimiter=',')
        
                
                
            
                

    


