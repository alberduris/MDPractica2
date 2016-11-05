#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@authors: Julen, Alberto, Till



        

"""

from sklearn import decomposition
import matplotlib.cm as cm
from scipy import spatial
import matplotlib.pyplot as plt
import time
import sys 
import os
import numpy as np
import numpy.random as random
import Preprocesado as Preprocesado

class K_means:
    
    def __init__(self, numClusters, opcIni, distMink, distInt, crit, cte, pca):
        self.numClusters = numClusters
        self.opcIni = opcIni
        self.distMink = distMink
        self.distInt = distInt
        self.crit = crit
        self.cte = cte
        self.pca = pca
        
        
        print "KMeans inicializado - Trabajo por hacer D:"
        
    

    '''
    @post: Inicializa dos matrices
        -La matriz de instancias que contiene los atributos de cada instancia (vectores de las palabras)
        -La matriz de clusters que contiene los centroides (vectores de los centroides)
    '''
    def initializeMatrixes(self,instancesFileName):
        
        t0 = time.clock()
        
        print 'COMENZANDO INICIALIZACIÓN'
        
        print 'Abriendo fichero...'        
        instancesFile = open(instancesFileName,'r')
        print 'Fichero abierto'
        
        
        print 'Calculando tamaño fichero, matrices...'
        numFileRows = self.getNumFileRows(instancesFileName)
        print 'Numero de instancias: ',;print numFileRows
        numFileColumns = self.getNumFileColumns(instancesFileName)
        print 'Numero de columnas: ',;print numFileColumns       

        print 'Inicializando matriz de instancias...'
        print 'Inicializando lista de palabras...'
        #Inicializar matriz de instancias
        instancesMatrix,wordList = self.initializeInstancesMatrix(instancesFile,numFileRows,numFileColumns)
        print 'Matriz de instancias inicializada'  
        print 'Lista de palabras inicializada\n\n'
        
        print 'Inicializando matriz de clusters...'
        print 'Inicializando matriz de pertenencia...'
        clustersMatrix,membershipMatrix = self.initializeClustersAndMembership(instancesMatrix)
        print 'Matriz de clusters inicializada'
        print 'Matriz de pertenencia inicializada\n\n'

        
        tInicializacion = time.clock() - t0
        print 'INICIALIZACIÓN TERMINADA'
        print 'Instancias procesadas: ',;print numFileRows
        print 'Atributos por instancia: ',;print numFileColumns 
        print 'Elementos procesados: ',;print numFileColumns*numFileRows 
        print 'Tiempo total inicialización: ',;print tInicializacion,;print ' segundos.'
        print 'Relación: ',;print ((tInicializacion/(numFileColumns*numFileRows))*1000),;print 'ms/elemento\n\n'
        
    
        return instancesMatrix,clustersMatrix,membershipMatrix,wordList
        
        
        
        

    '''
    @post: Inicializa la matriz de las instancias y la wordList
    '''
    def initializeInstancesMatrix(self,instancesFile,numFileRows,numFileColumns):
        #El numero de columnas del fichero es el numero de componentes del vector +1, por la palabra        
        numVectorComponents = numFileColumns - 1
        
        instancesMatrix = self.initializeMatrix(numFileRows,numVectorComponents)
        
        wordList = self.initializeStringMatrix(1,numFileRows)
        wordList.fill('')
        
        #Saltar la primera linea en caso de que sea cabecera    
        pos = instancesFile.tell()
        if (len(instancesFile.readline().split())==2):
            None
        else:
            instancesFile.seek(pos)
        
            
        #BUCLE TOCHO APROVECHAR A HACER TODO!!!
        j = -1
        for line in instancesFile:
            
            j = j + 1
            #if(j % 10000 == 0):
            #        print 'Instancia numero: ',;print j;
            splittedLine = line.split()
            for i in range(0,len(splittedLine)):
                    
                if (i == 0):#Matriz palabras
                    word = splittedLine[i]
                    wordList[i,j] = str(word)                
                else:#Matriz instancias
                    column = splittedLine[i]
                    instancesMatrix[j,i-1] = float(column)
        
        if(self.pca == 'pca'):        
            instancesMatrix = self.pcaInstances(instancesMatrix)
        
        return instancesMatrix,wordList
        
    '''
    @post: Inicializa la matriz de clusters y la matriz de pertenencia
    '''
    def initializeClustersAndMembership(self,instancesMatrix):
        
        if(self.opcIni == 'a'):
            #Inicializar matriz de clusters con ceros
            clustersMatrix = self.setRandomCentroids(self.getNumMatrixColumns(instancesMatrix),instancesMatrix)
            
            
        elif(self.opcIni == 'b'):
            clustersMatrix = self.set2KCentroids(self.getNumMatrixColumns(instancesMatrix),instancesMatrix)
            
        elif(self.opcIni == 'c'):
            clustersMatrix = self.plusPlusInit(self.getNumMatrixColumns(instancesMatrix),instancesMatrix)
            
            
        #Crear matriz de pertenencia
        membershipMatrix = self.createMembershipMatrix(self.getNumMatrixRows(instancesMatrix),int(self.numClusters))
        
        return clustersMatrix,membershipMatrix
        
    '''
    @post: Asigna los centroides iniciales asignando como centroides la 
    posición de k instancias al azar
    '''
    def setRandomCentroids(self,numFileColumns,instancesMatrix):
        clustersMatrix = self.initializeMatrix(int(self.numClusters),numFileColumns)
        for i in range (0,int(self.numClusters)):
        
            instanceNum = random.randint(0,self.getNumMatrixRows(instancesMatrix))
            clustersMatrix[i,:] = self.getVector(instanceNum,instancesMatrix)
            
        
        return clustersMatrix
        
    '''
    @pre: k nunca es mayor que 300. ?
    @post: Genera 2k centroides y devuelve los k más separados entre sí. 
    @note: Muchas dudas sobre la eficiencia de este algoritmo.

    '''
    def set2KCentroids(self,numFileColumns,instancesMatrix):
        clustMatrix = self.initializeMatrix(int(self.numClusters)*2,numFileColumns)
        
        for i in range (0,int(self.numClusters)*2):
        
            instanceNum = random.randint(0,self.getNumMatrixRows(instancesMatrix))
            clustMatrix[i,:] = self.getVector(instanceNum,instancesMatrix)
       
        centroidsDistances = np.ndarray(shape=(int(self.numClusters)*2))
        for i in range (0,int(self.numClusters)*2):
            for j in range (0,int(self.numClusters)*2):
                if j!=i:
                    if self.distMink=='0':
                        centroidsDistances[i] += self.getCosineDistance(self.getVector(j,clustMatrix),self.getVector(i,clustMatrix))
                    else:    
                        centroidsDistances[i] += self.getDistance(float(self.distMink),self.getVector(j,clustMatrix),self.getVector(i,clustMatrix))
        # self.getVector(i,clustersMatrix) == clustersMatrix[i] == clustersMatrix[i,:]
        #print str(clustMatrix.shape[0]) + "un valor"
        while clustMatrix.shape[0]>int(self.numClusters):
            minimo = min(centroidsDistances)
            print minimo,; print clustMatrix.shape[0]
            ind = centroidsDistances.tolist().index(minimo)
            clustMatrix = np.delete(clustMatrix,ind, 0) 
            centroidsDistances = np.delete(centroidsDistances,ind)
                
        return clustMatrix
        
    '''
    @post: Realiza la inicialización KMeans++
    @doc: http://ilpubs.stanford.edu:8090/778/1/2006-13.pdf
    '''    
    def plusPlusInit(self,numFileColumns,instancesMatrix):
        #Inicializar matriz de clusters        
        clustersMatrix = self.initializeMatrix(int(self.numClusters),numFileColumns)
        
        #Escoger un centroide inicial c1 al azar
        instanceNum = random.randint(0,self.getNumMatrixRows(instancesMatrix))
        c1 = self.getVector(instanceNum,instancesMatrix)

        #Asignar como primer centroide c1
        clustersMatrix[0,:] = c1        
        
        for i in range (1,int(self.numClusters)):#Hasta tener k centroides 
            
            
            D2 = np.array([min([np.linalg.norm(instance-centroid)**2 for centroid in clustersMatrix]) for instance in instancesMatrix])
            prob = D2/D2.sum()
            cumprob = prob.cumsum()
            r = random.random()
            ind = np.where(cumprob >= r)[0][0]
            next_centroid = self.getVector(ind,instancesMatrix)
            clustersMatrix[i,:] = next_centroid
        
        return clustersMatrix
            
    
    '''
    @post: Inicializa una matriz de ceros con las dimensiones pasadas por params
    '''
    def initializeMatrix(self,rows,columns):
        matrix = np.ndarray(shape=(rows,columns))
        matrix.fill(0)
        return matrix
        
    '''
    @post: Inicializa una matriz de ceros con las dimensiones pasadas por params
    '''
    def initializeStringMatrix(self,rows,columns):
        matrix = np.ndarray(shape=(rows,columns),dtype=(np.dtype("a25")))
        matrix.fill(0)
        return matrix
    
    '''
    @post: Crea la matriz de pertenencia inicial, con tantas columnas como clusters y 
    tantas filas como instancias. Se rellena con ceros.
    '''
    def createMembershipMatrix(self,rows,columns):
        
        '''
        Duda eficiencia: La matriz de pertenencia debería ser de tipo int
        o boolean??
        membershipMatrix = np.ndarray(shape=(rows,columns),dtype=bool)
        (El cambio es trivial ya que el resto funciona igual)
        '''
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
        
        
        f = open(file_name,'r')
        firstLine = f.readline()
        splittedFirstLine = firstLine.split()
        
        if(len(splittedFirstLine)==2):#Si tiene cabecera
            return int(splittedFirstLine[0])
                
        #Bucle tocho
        with open(file_name) as instancesFile:
            for i,line in enumerate(instancesFile):
                pass
        return i+1
        
    '''
    @post: Devuelve en numero de columnas del fichero pasado por param
    '''  
    def getNumFileColumns(self,file_name):

        f = open(file_name,'r')
        firstLine = f.readline()
        splittedFirstLine = firstLine.split()
        
        if(len(splittedFirstLine)==2):#Si tiene cabecera
            return int(splittedFirstLine[1])+1        
        
        instancesFile = open(file_name,'r')        
        line = instancesFile.readline()
        splLine = line.split()
        return len(splLine)
        
       
    '''
    @post: Devuelve el vector de tipo np.array que esta en la fila i de la matriz matrix
    '''
    def getVector(self,i,matrix):
                
        return np.asarray(matrix[i,::])

        
            
    '''
    Quizas convendría establecer un tipo de datos propio puesto que los valores de los vectores tienen sólo 6 decimales 
    (float16 de numpy se nos queda un poco grande) // Preguntarle a Alicia si eso le va a ahorrar tiempo al algoritmo.
    https://docs.python.org/2/extending/newtypes.html
    
    Alber: Me parece interesante, pero quizás sea demasiado para esta práctica.
    '''    

    '''
    @pre: alfa numero real no negativo, vectores 1 y 2 del tipo np.array() (¿a los que previamente se les ha extraido la clase?)
    @note: interesa que este metodo sea muy eficiente, surgen muchas dudas
    @post: la distancia de minkovski (float number) entre ambos vectores segun el parametro alfa.
    '''      
    def getDistance(self,alfa,vector1,vector2):
        return np.sum(np.absolute(vector1-vector2)**alfa)**(float(1)/alfa)
        
    '''
    @post: Similaridad coseno
    @note: Usando librería Scipy
    '''
    def getCosineSimilarity(self,vector1,vector2):
        return 1 - spatial.distance.cosine(vector1,vector2)

    '''
    @post: Distancia coseno
    @note: Usando librería Scipy
    '''
    def getCosineDistance(self,vector1,vector2):
        return spatial.distance.cosine(vector1,vector2)
        
    '''
    @pre: dos conjuntos de vectores del tipo np.array() 
    @note: (extension de pre) estos dos conjuntos seran del tipo np.array(). (hay otra forma de establecerlos mas eficiente?)
    @post: la distancia (float number) entre ambos conjuntos determinada por la distancia menor entre dos vectores de conjuntos diferentes.
    '''
    def singleLink(self,alfa,conjunto1,conjunto2):

        
        if(str(self.distMink) == '0'):
            distMin = self.getCosineDistance(conjunto1[0],conjunto2[0])
            for instance1 in conjunto1:
                for instance2 in conjunto2:
                    dist = self.getCosineDistance(instance1,instance2)
                    if dist < distMin:
                        distMin = dist
            
        else:    
            distMin = self.getDistance(alfa,conjunto1[0],conjunto2[0])
            for instance1 in conjunto1:
                for instance2 in conjunto2:
                    dist = self.getDistance(alfa,instance1,instance2)
                    if dist < distMin:
                        distMin = dist
        return distMin
    '''
    @pre: dos conjuntos de vectores del tipo np.array() (¿a los que previamente se les ha extraido la clase?)
    @note: (extension de pre) estos dos conjuntos seran del tipo np.array(). (hay otra forma de establecerlos mas eficiente?)
    @post: la distancia (float number) entre ambos conjuntos determinada por la distancia mayor entre dos vectores de conjuntos diferentes.
    '''
    def completeLink(self,alfa,conjunto1,conjunto2):
        distMax = 0
        
        if (self.distMink == '0'):
            for instance1 in conjunto1:
                for instance2 in conjunto2:
                    dist = self.getCosineDistance(instance1,instance2)
                    if dist > distMax:
                        distMax = dist
        else:    
            for instance1 in conjunto1:
                for instance2 in conjunto2:
                    dist = self.getDistance(alfa,instance1,instance2)
                    if dist > distMax:
                        distMax = dist
        return distMax
        

    '''
    @post: devuelve el valor sse resultante de sumar los valores sse de todos los clusters.
    '''
    def sse(self, clustersMatrix, membershipMatrix, instancesMatrix):
        t0 = time.clock()
        sseAcum = 0
        indexCl = 0
        for cluster in clustersMatrix:
            sseCluster = 0
            indexInstance = 0
            for instancia in instancesMatrix:
                if membershipMatrix[indexInstance,indexCl] ==1:
                    sseCluster += (self.getDistance(2,cluster,instancia))**2
                indexInstance+=1
            sseAcum+=sseCluster
            indexCl+=1
        tSSE = time.clock() - t0
        print 'Tiempo total SSE: ',;print tSSE,;print ' segundos.'
        print 'Relación : ',;print tSSE/self.getNumMatrixRows(membershipMatrix)*1000,;print ' ms/instancia.'
        return sseAcum
    
    '''
    @post: Asigna el centroide más cercano para cada instancia actualizando
    la matriz de pertenencia
    '''
    def closestCentroid(self,instancesMatrix,clustersMatrix,membershipMatrix):
        
        membershipMatrix.fill(0)
        instanceIndex = -1
        for instance in instancesMatrix:
            instanceIndex += 1
            distanceToCentroid = float("inf")
            cIndex = -1
            for cluster in clustersMatrix:
                cIndex += 1
                
                if(self.distMink == '0'):
                    aux = self.getCosineDistance(instance,cluster)
                else:
                    aux = self.getDistance(float(self.distMink),instance,cluster)
                   
                
                
                if(aux < distanceToCentroid):
                    clusterIndex = cIndex
                    distanceToCentroid = aux
            
            #Actualizar matriz pertenencia
            membershipMatrix[instanceIndex][clusterIndex] = 1
        
        return membershipMatrix
        
    '''
    @post: Se actualiza la matriz de clusters con los nuevos centroides de 
    los clusters calculados a partir del promedio de la posición (vector) 
    de las instancias que pertenecen a cada cluster. 
    '''
    def setUpdatedCentroids(self,instancesMatrix,clustersMatrix,membershipMatrix):
        numRows = self.getNumMatrixRows(membershipMatrix)
        numCols = self.getNumMatrixColumns(membershipMatrix)
        numAtts = self.getNumMatrixColumns(instancesMatrix)        
        
        vectorSuma = np.ndarray(shape=(1,numAtts))
        vectorSuma.fill(0)
        
        cont = 0
        
        for j in range (0,numCols):
            for i in range (0,numRows):
                if (membershipMatrix[i,j] == 1):
                    cont += 1
                    vectorSuma = vectorSuma + self.getVector(i,instancesMatrix)
                    
            newCluster = self.getMeanVector(cont,vectorSuma,numAtts)
            clustersMatrix[j,:]=newCluster
            cont = 0
                    
        return clustersMatrix
            
            
    def getMeanVector(self,cont,vector,numAtts):
        for i in range(0,numAtts):
            vector[0,i] = vector[0,i]/cont            
            
        return vector
                    
                    
    '''
    @post: KMeans clustering
    '''
    def clustering(self,instancesMatrix,clustersMatrix,membershipMatrix,wordList):
        
       
        
        print 'COMENZANDO CLUSTERING'
        
        t0 = time.clock()
        
        f = open('cluster_assingments.txt','w')   
        
        #Asignamos las pertenencias iniciales
        f.write('Pertenencias iniciales :\n')        
        membershipMatrix = self.closestCentroid(instancesMatrix,clustersMatrix,membershipMatrix)
        
        #Imprimir/Graficar Pertenencias iniciales
        if(self.pca == 'pca'):
            self.printPlotClusterAssingments(membershipMatrix,wordList,f,instancesMatrix,clustersMatrix,0)
        else:
            self.printClusterAssingments(membershipMatrix,wordList,f)
        
        if(self.crit == 'n'):#Num.Iteraciones fijo
            for i in range (0,int(self.cte)):
                print 'Iteración ',;print i
                clustersMatrix = self.setUpdatedCentroids(instancesMatrix,clustersMatrix,membershipMatrix)
                membershipMatrix = self.closestCentroid(instancesMatrix,clustersMatrix,membershipMatrix)            
                
                f.write('Iteracion : '+str(i+1)+'\n')
                if(self.pca == 'pca'):
                    self.printPlotClusterAssingments(membershipMatrix,wordList,f,instancesMatrix,clustersMatrix,i+1)
                else:
                    self.printClusterAssingments(membershipMatrix,wordList,f)
            
            f.close()
        else:#Umbral
            cont = -1
            variation = float('inf')
            clustersMatrixBefore = clustersMatrix.copy()
            while(variation > float(self.cte)):
                cont += 1
                print 'Iteración ',;print cont
                clustersMatrix = self.setUpdatedCentroids(instancesMatrix,clustersMatrix,membershipMatrix)
                

                membershipMatrix = self.closestCentroid(instancesMatrix,clustersMatrix,membershipMatrix)            
                
                #print 'Matriz pertenencia en la iteración ' + str(i+1)
                f.write('Iteracion : '+str(cont+1)+'\n')
                if(self.pca == 'pca'):
                    self.printPlotClusterAssingments(membershipMatrix,wordList,f,instancesMatrix,clustersMatrix,cont+1)
                else:
                    self.printClusterAssingments(membershipMatrix,wordList,f)

                if(cont > 0):#Calcular la variacion despues de la 1era it.
                    variation = self.getVariation(clustersMatrixBefore,clustersMatrix)
                print 'Variación: ',;print variation
                clustersMatrixBefore = clustersMatrix.copy()
                
                
            
            print 'Bucle finalizado'
            print 'Variación: ',;print variation
                 
                
        if(self.crit == 'n'):
            iteraciones = i
        else:
            iteraciones = cont
        
        tClustering = time.clock() - t0
        print 'CLUSTERING FINALIZADO'
        print 'Tiempo total clustering: ',;print tClustering,;print ' segundos.'
        print 'Tiempo por iteración : ',;print tClustering/(iteraciones+1),;print ' segundos/iteración.'
        print 'KMeans - End'
        

    '''
    @post: Devuelve la variación de la posición, en valor absoluto, entre los
    centroides actuales y los de la iteración anterior.
    @params: La matriz de clusters actual y la anterior
    '''
    def getVariation(self,clustersMatrixBefore,clustersMatrix):
        vari = 0
        
        if(self.distMink == '0'):
            for i in range (0,int(self.numClusters)):
                vari = vari + abs(self.getCosineDistance(self.getVector(i,clustersMatrix),self.getVector(i,clustersMatrixBefore))) 
        else:
            for i in range (0,int(self.numClusters)):
                vari = vari + abs(self.getDistance(float(self.distMink),self.getVector(i,clustersMatrix),self.getVector(i,clustersMatrixBefore)))            
            
        return vari
    
    '''
    @post: Calcula la matriz de distancias, eficientemente (diagonal superior),
    siendo cada distancia la distancia entre los centroides de los clusters
    @note: Creo que no sirve para nada, lo he hecho por error
    '''
    def getCentroidsDistance(self,clustersMatrix):

        distancesMatrix = self.initializeMatrix(int(self.numClusters),int(self.numClusters))
        
        if(self.distMink == '0'):
            for i in range (0,int(self.numClusters)):
                for j in range(i+1,int(self.numClusters)):
                    distancesMatrix[i][j] = self.getCosineDistance(self.getVector(i,clustersMatrix),
                                                            self.getVector(j,clustersMatrix))
        else:
            for i in range (0,int(self.numClusters)):
                for j in range(i+1,int(self.numClusters)):
                    distancesMatrix[i][j] = self.getDistance(float(self.distMink),
                                                            self.getVector(i,clustersMatrix),
                                                            self.getVector(j,clustersMatrix))
        
        return distancesMatrix
    '''
    @post: Devuelve la palabra de índice i contenida en la
    lista wordList
    '''
    def getWord(self,index,wordList):
        
        return wordList[0,index]
    
    
    
    '''
    @post: Dada la matriz de pertenencia membershipMatrix y
    la lista de palabras wordList,genera un fichero las pertenencias de los clusters
    '''
    def printClusterAssingments(self,membershipMatrix,wordList,out_file):
        
        rows = self.getNumMatrixRows(membershipMatrix)
        cols = self.getNumMatrixColumns(membershipMatrix)
    
        listaClusters = []
        
        for j in range (0, cols):
            lista = []
            lista.append('Cluster '+str(j+1))
            for i in range (0,rows):#Por cada cluster
                if(membershipMatrix[i,j] == 1):
                    lista.append(self.getWord(i,wordList))
                    
                    
            listaClusters.append(lista)
            
        for i in range(0,len(listaClusters)):
            out_file.write(str(listaClusters[i])+'\n')
    
    
    '''
    @post: Dada la matriz de pertenencia membershipMatrix y
    la lista de palabras wordList,genera un fichero las pertenencias de los clusters
    y realiza gráficos
    '''
    def printPlotClusterAssingments(self,membershipMatrix,wordList,out_file,instancesMatrix,clustersMatrix,it):

        fig = plt.figure()
        fig.canvas.set_window_title('KMeans_K=%s_N=%s_Init=%s_Dist=%s_IG=%s_It=%s' % 
        (str(self.numClusters),str(self.getNumMatrixRows(instancesMatrix)),
         str(self.opcIni),str(self.distMink),str(self.distInt),str(it)))
                    

        
        rows = self.getNumMatrixRows(membershipMatrix)
        cols = self.getNumMatrixColumns(membershipMatrix)
    
        #Define los limites en x
        plt.xlim(instancesMatrix.min()-1,instancesMatrix.max()+1)
        #Define los limites en y
        plt.ylim(instancesMatrix.min()-1,instancesMatrix.max()+1)    
        
        listaClusters = []
        listaInstancesPrint = []
        
        for j in range (0, cols):
            lista = []
            lista.append('Cluster '+str(j+1))
            listaPrint = [] 
            for i in range (0,rows):#Por cada cluster
                if(membershipMatrix[i,j] == 1):
                    lista.append(self.getWord(i,wordList))
                    listaPrint.append(i)
                    
            listaClusters.append(lista)
            listaInstancesPrint.append(listaPrint)
        colors = cm.rainbow(np.linspace(0,1,int(self.numClusters)))
        for i in range(0,len(listaClusters)):
            col = colors[i]
            out_file.write(str(listaClusters[i])+'\n')
            clustN = listaInstancesPrint[i]
            arrayInstancias = self.initializeMatrix(len(clustN),2)
            for j in range(0,len(clustN)):
                arrayInstancias[j,:] = self.getVector(clustN[j],instancesMatrix)
                #Este array contiene las instancias pertenecientes a cada cluster
                #En cada iteracion, un cluster diferente
            plt.scatter(zip(*arrayInstancias)[0], zip(*arrayInstancias)[1],color=col)
        
        #Dibuja los centroides
        plt.scatter(zip(*clustersMatrix)[0], zip(*clustersMatrix)[1],s=80,marker='>',c=colors)
        
    '''
    @post: Devuelve la dos matrices pasadas por parámetros con PCA aplicado para 2 componentes
    @note: Utiliza la librería Scipy
    @deprecated
    '''    
    def pcaInstancesAndClusters(self,instancesMatrix,clustersMatrix):
        pca = decomposition.PCA(n_components=2)
        pca.fit(instancesMatrix)
        instPCA = pca.transform(instancesMatrix)
        
        pca2 = decomposition.PCA(n_components=2)
        pca2.fit(clustersMatrix)
        clustPCA = pca2.transform(clustersMatrix)
        
        return instPCA,clustPCA
        
    '''
    @post: Devuelve la matriz pasada por parámetro con PCA aplicado para 2 componentes
    @note: Utiliza la librería Scipy
    '''    
    def pcaInstances(self,instancesMatrix):
        pca = decomposition.PCA(n_components=2)
        pca.fit(instancesMatrix)
        instPCA = pca.transform(instancesMatrix)
        
        return instPCA
        
   
    
        
    
            
    '''
    @post: Devuelve una matriz tal que:
    Filas = k 
    Columnas = 2 --> Col1: Distancia acumulada ; Col2 = NumInstancias en ese cluster
    '''
    def getNeighboursAndForeignersDistance(self,index,instancesMatrix,membershipMatrix):
        
        distancesInstances = self.initializeMatrix(int(self.numClusters),2)
        #Col1 = DistanciaTotal : #Col2 = NumInstancias
        
        for i in range(0,self.getNumMatrixRows(membershipMatrix)):#Por cada fila
            for j in range(0,int(self.numClusters)):#Por cada columna
                
                if(membershipMatrix[i][j] == 1):
                    
                    if(self.distMink == '0'):
                        distancesInstances[j][0] += self.getCosineDistance(self.getVector(index,instancesMatrix),
                                                            self.getVector(i,instancesMatrix))
                        distancesInstances[j][1] += 1
                    else:
                        distancesInstances[j][0] += self.getDistance(float(self.distMink),self.getVector(index,instancesMatrix),
                                                            self.getVector(i,instancesMatrix))
                        distancesInstances[j][1] += 1
                
        
        return distancesInstances
    
    '''
    @post: Devuelve a(xi) y b(xi) respecto a la matriz de distancias entre instancias 
    que se le pase por parámetro.
    @note: La matriz pasada por param será la salida del método getNeighboursAndForeignersDistances 
    en el que se especificara para qué xi (instancia) se está calculando el a y b
    '''
    def getABSilhouette(self,distancesInstances):
        
        distExtranjeros = float('inf')
        aux = 0
        clusterPropio = np.amin(distancesInstances,axis=0)
        clustersExtranjeros = distancesInstances-clusterPropio
        
        for i in range(0,self.getNumMatrixRows(clustersExtranjeros)):
            aux = clustersExtranjeros[i][0]/clustersExtranjeros[i][1]
            if(aux < distExtranjeros and aux != 0):
                distExtranjeros = aux
            
            
            
        return clusterPropio[0]/clusterPropio[1],distExtranjeros
    
    '''
    @post: Calcula índice Silhouette para una instancia
    '''
    def getSilhouette(self,a,b):
        return b-a/max(a,b)

    '''
    @post: Calcula índice Silhouette para todas las instancias
    '''
    def silhouetteMain(self,instancesMatrix,membershipMatrix):
        t0 = time.clock()
        silhouetteX = 0        
        for i in range(0,self.getNumMatrixRows(membershipMatrix)):
            if(i%100==0):print 'Silhouette instancia ',;print i
            foreign = kmeans.getNeighboursAndForeignersDistance(i,instancesMatrix,membershipMatrix)
            a,b = kmeans.getABSilhouette(foreign)
            sil = kmeans.getSilhouette(a,b)            
            silhouetteX =+ sil
            #print sil
        tSilhouette = time.clock() - t0
        print 'Índice Silhouette conjunto: ',;print silhouetteX/self.getNumMatrixRows(membershipMatrix)
        print 'Tiempo total índice Silhouette: ',;print tSilhouette
        print 'Relación: ',;print tSilhouette/i,;print 'segundos/instancia'

'''
Métodos para pruebas - En realidad no son métodos
se trata de copiar el cuerpo del método al main y ejecutar
pero es una manera cómoda de poner varias lineas sin
molestar y sin hacer un comentario multilinea feo
Grande Alberto! 
:D :D
'''
def test1():
    vec1=np.array([0.423481, 0.369929, 1.111249, 0.013840, 1.331685])
    vec2=np.array([0.347326, 0.256732, 0.978557, 0.664598, 1.915115])
    k = K_means(1,2,3,4,5,6)
    dist = k.getDistance(1,vec1,vec2)
    print "distancia mink alfa=1: " + str(dist)
    dist = k.getDistance(2,vec1,vec2)
    print "distancia mink alfa=2: " + str(dist)
    
def test2():
    k = K_means(1,2,3,4,5,6)
    print k.getNumFileRows("vectors_muy_peque.txt")
    print k.getNumFileColumns("vectors_muy_peque.txt")
    
def test3():
    k = K_means(1,2,3,4,5,6)
    matrix = k.initializeInstances("vectors_muy_peque.txt")
    
    vector1 = k.getVector(matrix,3)
    print vector1

def test4():
    k = K_means(1,2,3,4,5,6)
    
   
    instancesMatrix,clustersMatrix,membershipMatrix = k.initializeMatrixes("vectors_peque.txt")
    print instancesMatrix[1][1:]
    print instancesMatrix[1:][1:2]
    
    for i in range (0,5):
      conjuntoVectores1 = instancesMatrix[i,:]  
      conjuntoVectores2 = instancesMatrix[i+10,:]    
    
    
    print 'Conjunto vectores 1: '
    print conjuntoVectores1
    
    print 'Conjunto vectores 2: '
    print conjuntoVectores2

    distanciaMin = k.singleLink(2,conjuntoVectores1,conjuntoVectores2)
    distanciaMax = k.completeLink(2,conjuntoVectores1,conjuntoVectores2)
    print "distanciaMin (singleLink): " + str(distanciaMin) #deberia dar una distancia bastante pequena porque no estoy tomando clusters reales y las instancias pueden estar muy mezcladas
    print "distanciaMax (completeLink): " + str(distanciaMax)
    #no soy capaz de interpretar si los resultados son correctos, podria hacer los calculos a mano pero da pereza.
    #entran dentro de lo razonable puesto que la min es menor que uno y la max es 2 (para la prueba que he hecho yo)
    #dado que los randoms generados estan entre 0 y 1 no me parece muy alocado que entre 2 grupos de 3 instancias las mas alejadas esten separadas por 2 unidades.
    
def test5():
    #Probar lo de la matriz de pertenencia
    print 'Matriz pertenencia DESPUES: '
    kmeans.imprimirMatriz(membershipMatrix)        
        
    kmeans.closestCentroid(instancesMatrix,clustersMatrix,membershipMatrix)
        
    print 'Matriz pertenencia DESPUES: '
    kmeans.imprimirMatriz(membershipMatrix)
    
def test6():
   
    k = K_means(5,'c',2,'s','a',300,'')
    instancesMatrix,clustersMatrix,membershipMatrix,wordList = k.initializeMatrixes("vectors_peque.txt")
    centroides = k.set2KCentroids(k.getNumMatrixColumns(instancesMatrix),instancesMatrix)
    for centroide in centroides:
        print centroide[2:4]
       
def test7():
    kmeans = K_means(5,'c',2,'s','a',300,'')
    instancesMatrix,clustersMatrix,membershipMatrix,wordList = kmeans.initializeMatrixes("vectors_peque.txt")
    kmeans.clustering(instancesMatrix,clustersMatrix,membershipMatrix,wordList)
    print kmeans.sse(clustersMatrix, membershipMatrix, instancesMatrix)

def extraerFragmentoFichero():
    
    f = open('GoogleNews-vectors-negative300.txt','r')
    f_out = open('GoogleNews10000.txt','w')
    
    for i in range (0,10000):
        line = f.readline()
        f_out.write(str(line))
        
    f.close()
    f_out.close()
                
    '''
    @post: Devuelve una lista con todas las palabras del 
    set original de datos
    @deprecated
    '''
    def getWordList(self,file_name):
        instancesFile = open(file_name,'r')
        instancesFile.next()        
        wordList = self.initializeStringMatrix(1,self.getNumFileRows(file_name))
        wordList.fill('')
        
        i = 0;
        j = -1;
        for line in instancesFile:
            j = j + 1
            splittedLine = line.split()
            word = splittedLine[i]
            wordList[i,j] = str(word)
            
        return wordList
        
def generalPerformanceTest():
    
    

    
    performance_file = open('generalPerformanceTest.csv','a') #he cambiado esto para que haga append
    
    #independientemente de los parametros que se le pasen
 
    minkwsk = '0' #cosine  MUY RICO ALBERTO TOMAS LOS NUMEROS COMO CARACTERES D:<
    inter = 's' #irrelevante
    crit = 'd' #criterio umbral
    terminacion = 0.001
    pca = ''
    
    performance_file.write('VARIANDO INICIALIZACION,Dist 0 => Cosine Distance en lugar de Minkwsk,criterio d=umbral,umbral=0.001' )
    
    

    #inicial inclusive final exclusive
    for j in range(1,4):
        if j==1:
            performance_file.write('random initialization\n')
            ini='a'
        elif j==2:
            performance_file.write('2K initialization\n')
            ini='b'
        else:
            performance_file.write('Kmeans++ initialization\n')
            ini='c'

        for i in range (20,26):
            kmeans = K_means(i,ini,minkwsk,inter,crit,terminacion,pca)
            instancesMatrix,clustersMatrix,membershipMatrix,wordList = kmeans.initializeMatrixes("GoogleNews2000.txt")
            kmeans.clustering(instancesMatrix,clustersMatrix,membershipMatrix,wordList)
            
            sse = kmeans.sse(clustersMatrix,membershipMatrix,instancesMatrix)
            performance_file.write('k,SSE\n')
            performance_file.write(str(i)+','+str(sse)+'\n')
    
    ini = 'c' 
    #ahora variaremos cosine y minks distance
    inter = 's' #irrelevante
    crit = 'd' #criterio umbral
    terminacion = 0.001
    pca = ''
    
    performance_file.write('VARIANDO DISTANCIA MINKSK (y coseno),inicializacion = k++,criterio d=umbral,umbral=0.001' )
    
    

    #inicial inclusive final exclusive
    for j in range(0,4):
        minkwsk = j
        if j==0:
            minkwsk = '0'
            performance_file.write('distancia coseno\n')
        else:
            performance_file.write('distancia minkovski =' + str(j) + ' \n')
       
        for i in range (20,26):
            kmeans = K_means(i,ini,minkwsk,inter,crit,terminacion,pca)
            instancesMatrix,clustersMatrix,membershipMatrix,wordList = kmeans.initializeMatrixes("GoogleNews2000.txt")
            kmeans.clustering(instancesMatrix,clustersMatrix,membershipMatrix,wordList)
            
            sse = kmeans.sse(clustersMatrix,membershipMatrix,instancesMatrix)
            performance_file.write('k,SSE\n')
            performance_file.write(str(i)+','+str(sse)+'\n')

    ini = 'c' 
    minkwsk = '0'
    inter = 's' #irrelevante
    pca = ''
    
    performance_file.write('VARIANDO ENTRE UMBRAL Y NUM IT FIJAS,inicializacion = k++, distancia coseno' )
    
    

    #inicial inclusive final exclusive
    for j in range(0,2):
        if j==0:
            crit = 'd' #criterio umbral
            terminacion = 0.001
            performance_file.write('umbral fijo, 0.001 \n')
        else:
            crit = 'n'
            terminacion = 7
            performance_file.write('num iteraciones fijo, 7 \n')
        for i in range (20,26):
            kmeans = K_means(i,ini,minkwsk,inter,crit,terminacion,pca)
            instancesMatrix,clustersMatrix,membershipMatrix,wordList = kmeans.initializeMatrixes("GoogleNews2000.txt")
            kmeans.clustering(instancesMatrix,clustersMatrix,membershipMatrix,wordList)
            
            sse = kmeans.sse(clustersMatrix,membershipMatrix,instancesMatrix)
            performance_file.write('k,SSE\n')
            performance_file.write(str(i)+','+str(sse)+'\n')

    performance_file.close()




def kPerformanceTest():
    
    

    
    performance_file = open('kPerformanceTest.csv','a') #he cambiado esto para que haga append
    
    
    if (Preprocesado.preMain()):
        print 'Parámetros correctos'
        
        k = sys.argv[1]
        ini = sys.argv[2]
        minkwsk = sys.argv[3]
        inter = sys.argv[4]
        crit = sys.argv[5]
        terminacion = sys.argv[6]
        if(len(sys.argv)==8):        
            pca = sys.argv[7]
        else:
            pca = ''
        
        performance_file.write('KMeans_Init=%s,Dist=%s,Crit=%s,Term=%s \n' % (str(ini),str(minkwsk),str(crit),str(terminacion)))
        performance_file.write('c= inicializacion kmeans++,Dist 0 => Cosine Distance en lugar de Minkwsk,criterio d=umbral' )
        performance_file.write('k,SSE\n')
        

        #Julen, aquí vete poniendo el inicial y el final (exclusivo el final)
        #Salva los ficheros cada vez que si no te escribe encima eh
        for i in range (1,300):
            
            print 'ITERACIÓN PARA K = ',;print i
        
            kmeans = K_means(i,ini,minkwsk,inter,crit,terminacion,pca)
            instancesMatrix,clustersMatrix,membershipMatrix,wordList = kmeans.initializeMatrixes("GoogleNews2000.txt")
            kmeans.clustering(instancesMatrix,clustersMatrix,membershipMatrix,wordList)
            
            sse = kmeans.sse(clustersMatrix,membershipMatrix,instancesMatrix)
            
            performance_file.write(str(i)+','+str(sse)+'\n')
            
        
        performance_file.close()
    
    else: #Parámetros incorrectos
        
        print 'parametros incorrectos'
   
'''
@post: Método principal 
@note: De aquí surge la magia
'''     
def tirarDelHilo():
    print 'K_means : main'

    #kPerformanceTest()    
    
    #extraerFragmentoFichero()
    
    
    if (Preprocesado.preMain()):
        print 'Parámetros correctos'
        
        k = sys.argv[1]
        ini = sys.argv[2]
        minkwsk = sys.argv[3]
        inter = sys.argv[4]
        crit = sys.argv[5]
        terminacion = sys.argv[6]
        if(len(sys.argv)==8):        
            pca = sys.argv[7]
        else:
            pca = ''
        
        

        
        kmeans = K_means(k,ini,minkwsk,inter,crit,terminacion,pca)
        instancesMatrix,clustersMatrix,membershipMatrix,wordList = kmeans.initializeMatrixes("vectors.txt")
        kmeans.clustering(instancesMatrix,clustersMatrix,membershipMatrix,wordList)
        #kmeans.silhouetteMain(instancesMatrix,membershipMatrix)
        print(kmeans.sse(clustersMatrix,membershipMatrix,instancesMatrix))
        
        
        
    
    else: #Parámetros incorrectos
        
        print 'parametros incorrectos'

#para pruebas
if __name__=="__main__":
    
    tirarDelHilo()
    #generalPerformanceTest()
    #kPerformanceTest()    
    
    #extraerFragmentoFichero()
    
    
    

