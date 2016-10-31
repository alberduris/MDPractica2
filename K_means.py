#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@authors: Julen, Alberto, Till



        

"""
import matplotlib.pyplot as plt
import time
import sys 
import numpy as np
import numpy.random as random
import Preprocesado as Preprocesado

class K_means:
    
    def __init__(self, numClusters, opcIni, distMink, distInt, crit, cte ):
        self.numClusters = numClusters
        self.opcIni = opcIni
        self.distMink = distMink
        self.distInt = distInt
        self.crit = crit
        self.cte = cte
        
        
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
        clustersMatrix,membershipMatrix = self.initializeClustersAndMembership(instancesMatrix,numFileRows,numFileColumns)
        print 'Matriz de clusters inicializada'
        print 'Matriz de pertenencia inicializada\n\n'

        
        tInicializacion = time.clock() - t0
        print 'INICIALIZACIÓN TERMINADA'
        print 'Instancias procesadas: ',;print numFileRows
        print 'Atributos por instancia: ',;print numFileColumns 
        print 'Elementos procesados: ',;print numFileColumns*numFileRows 
        print 'Tiempo total inicialización: ',;print tInicializacion,;print ' segundos.'
        print 'Tiempo/elemento: ',;print (tInicializacion/(numFileColumns*numFileRows)),;print '\n\n'
        
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
        
        return instancesMatrix,wordList
        
    '''
    @post: Inicializa la matriz de clusters y la matriz de pertenencia
    '''
    def initializeClustersAndMembership(self,instancesMatrix,numFileRows,numFileColumns):
        
        if(self.opcIni == 'a'):
            #Inicializar matriz de clusters con ceros
            clustersMatrix = self.setRandomCentroids(numFileColumns-1,instancesMatrix)
            self.plotInstancesAndCentroids(instancesMatrix,clustersMatrix)
            
        elif(self.opcIni == 'b'):
            raise Exception('Not implemented yet')
            
        elif(self.opcIni == 'c'):
            clustersMatrix = self.plusPlusInit(numFileColumns-1,instancesMatrix)
            self.plotInstancesAndCentroids(instancesMatrix,clustersMatrix)
            
        #Crear matriz de pertenencia
        membershipMatrix = self.createMembershipMatrix(numFileRows,int(self.numClusters))
        
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
                    centroidsDistances[i] += self.getDistance(self.distMink,self.getVector(j,clustMatrix),self.getVector(i,clustMatrix))
        # self.getVector(i,clustersMatrix) == clustersMatrix[i] == clustersMatrix[i,:]
        print str(clustMatrix.shape[0]) + "un valor"
        while clustMatrix.shape[0]>int(self.numClusters):
            ind = centroidsDistances.tolist().index(min(centroidsDistances))
            instanceToEliminate = clustMatrix[ind,:]
            clustMatrix = np.delete(clustMatrix,ind)
            centroidsDistances = np.delete(centroidsDistances,ind)
            for i in range(0,clustMatrix.shape[0]): #actualizamos las distancias entre instancias
                print str(clustMatrix.shape[0]) + "valor diferente"
                print clustMatrix.shape[0]
                print instanceToEliminate.shape[0]
                print self.getVector(i,clustMatrix).shape[0] #el indice i es mayor que el tamano del vector.
                centroidsDistances[i] -= self.getDistance(self.distMink,self.getVector(i,clustMatrix),instanceToEliminate)
                
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
    @pre: dos conjuntos de vectores del tipo np.array() 
    @note: (extension de pre) estos dos conjuntos seran del tipo np.array(). (hay otra forma de establecerlos mas eficiente?)
    @post: la distancia (float number) entre ambos conjuntos determinada por la distancia menor entre dos vectores de conjuntos diferentes.
    '''
    def singleLink(self,alfa,conjunto1,conjunto2):
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
        for instance1 in conjunto1:
            for instance2 in conjunto2:
                dist = self.getDistance(alfa,instance1,instance2)
                if dist > distMax:
                    distMax = dist
        return distMax
        
    
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
                aux = self.getDistance(int(self.distMink),instance,cluster)
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
        
        #print 'Pertenencias iniciales: '
        self.printClusterAssingments(membershipMatrix,wordList,f)
        
        if(self.crit == 'n'):#Num.Iteraciones fijo
            for i in range (0,int(self.cte)):
                print 'Iteración ',;print i
                clustersMatrix = self.setUpdatedCentroids(instancesMatrix,clustersMatrix,membershipMatrix)
                membershipMatrix = self.closestCentroid(instancesMatrix,clustersMatrix,membershipMatrix)            
                
                #print 'Matriz pertenencia en la iteración ' + str(i+1)
                f.write('Iteracion : '+str(i+1)+'\n')
                self.printClusterAssingments(membershipMatrix,wordList,f)
            
            f.close()
        else:#Umbral
            cont = -1
            variation = float('inf')
            clustersMatrixBefore = clustersMatrix.copy()
            while(variation > int(self.cte)):
                cont += 1
                print 'Iteración ',;print cont
                clustersMatrix = self.setUpdatedCentroids(instancesMatrix,clustersMatrix,membershipMatrix)
                

                membershipMatrix = self.closestCentroid(instancesMatrix,clustersMatrix,membershipMatrix)            
                
                #print 'Matriz pertenencia en la iteración ' + str(i+1)
                f.write('Iteracion : '+str(cont+1)+'\n')
                self.printClusterAssingments(membershipMatrix,wordList,f)

                if(cont > 0):#Calcular la variacion despues de la 1era it.
                    variation = self.getVariation(clustersMatrixBefore,clustersMatrix)
                clustersMatrixBefore = clustersMatrix.copy()
                
                
            
            print 'Bucle finalizado'
            print 'Variación: ',;print variation
                 
                
            
        
        tClustering = time.clock() - t0
        print 'CLUSTERING FINALIZADO'
        print 'Tiempo total clustering: ',;print tClustering,;print ' segundos.'
        print 'KMeans - End'
        

    '''
    @post: Devuelve la variación de la posición, en valor absoluto, entre los
    centroides actuales y los de la iteración anterior.
    @params: La matriz de clusters actual y la anterior
    '''
    def getVariation(self,clustersMatrixBefore,clustersMatrix):
        vari = 0
        
        for i in range (0,int(self.numClusters)):
            #vari = vari + abs(self.getDistance(int(self.distMink),clustersMatrix[i,:],clustersMatrixBefore[i,:]))
            vari = vari + abs(self.getDistance(int(self.distMink),self.getVector(i,clustersMatrix),self.getVector(i,clustersMatrixBefore)))            
            
        return vari
    
    '''
    @post: Calcula la matriz de distancias, eficientemente (diagonal superior),
    siendo cada distancia la distancia entre los centroides de los clusters
    @note: Creo que no sirve para nada, lo he hecho por error
    '''
    def getCentroidsDistance(self,clustersMatrix):

        distancesMatrix = self.initializeMatrix(int(self.numClusters),int(self.numClusters))
        
        for i in range (0,int(self.numClusters)):
            for j in range(i+1,int(self.numClusters)):
                distancesMatrix[i][j] = self.getDistance(int(self.distMink),
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
    la lista de palabras wordList, imprime por pantalla y
    en fichero las pertenencias de los clusters
    '''
    def printClusterAssingments(self,membershipMatrix,wordList,out_file):
        
        rows = self.getNumMatrixRows(membershipMatrix)
        cols = self.getNumMatrixColumns(membershipMatrix)
        
        listaClusters = []        
        
        for j in range (0, cols):
            lista = []
            lista.append('Cluster '+str(j+1))
            for i in range (0,rows):
                if(membershipMatrix[i,j] == 1):
                    lista.append(self.getWord(i,wordList))
            listaClusters.append(lista)
               

        for i in range (0,len(listaClusters)):
                #print listaClusters[i]
                out_file.write(str(listaClusters[i])+'\n')
                
    def plotInstancesAndCentroids(self,instancesMatrix,clustersMatrix):
        
        #Define los limites en x
        plt.xlim(instancesMatrix.min(),instancesMatrix.max())
        #Define los limites en y
        plt.ylim(instancesMatrix.min(),instancesMatrix.max())

        #Dibuja las instancias        
        plt.plot(zip(*instancesMatrix)[0], zip(*instancesMatrix)[1], '.', alpha=0.5)
        
        #Dibuja los centroides        
        plt.plot(zip(*clustersMatrix)[0], zip(*clustersMatrix)[1], 'ro')
        
        plt.savefig('plots/kpp_init_%s_N%s_K%s.png' % (str(self.opcIni),str(self.getNumMatrixRows(instancesMatrix)),str(self.numClusters)), \
                    bbox_inches='tight', dpi=200)
        
        
            
        
        
       
            


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
   
    k = K_means(5,'c',2,'s','a',300)
    instancesMatrix,clustersMatrix,membershipMatrix,wordList = k.initializeMatrixes("vectors_peque.txt")
    centroides = k.set2KCentroids(k.getNumMatrixColumns(instancesMatrix),instancesMatrix)
    for centroide in centroides:
        print centroide[2:4]
       

def extraerFragmentoFichero():
    
    f = open('GoogleNews-vectors-negative300.txt','r')
    f_out = open('GoogleNews10000.txt','w')
    
    for i in range (0,100000):
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


#para pruebas
if __name__=="__main__":
    print 'K_means : main'
    
    #extraerFragmentoFichero()
    
    
    if (Preprocesado.preMain()):
        print 'Parámetros correctos'
        
        k = sys.argv[1]
        ini = sys.argv[2]
        minkwsk = sys.argv[3]
        inter = sys.argv[4]
        crit = sys.argv[5]
        terminacion = sys.argv[6]
        
        

        
        kmeans = K_means(k,ini,minkwsk,inter,crit,terminacion)
        instancesMatrix,clustersMatrix,membershipMatrix,wordList = kmeans.initializeMatrixes("vectors_peque.txt")
        
        kmeans.clustering(instancesMatrix,clustersMatrix,membershipMatrix,wordList)
        

        
        
        
    
    else: #Parámetros incorrectos
        
        print 'parametros incorrectos'

        '''
        esto lo quitaremos:
        '''
        print 'pruebas:'
        test6()