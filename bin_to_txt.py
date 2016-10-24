# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 15:40:39 2016

@author: Alber
@source: Silo (http://stackoverflow.com/users/2567696/silo) @ http://stackoverflow.com/questions/27324292/convert-word2vec-bin-file-to-text

"""
import sys
from gensim.models import word2vec

print 'Iniciando'

#esto convendría hacerlo con rutas relativas 
model = word2vec.Word2Vec.load_word2vec_format(sys.argv[1], binary=True)

print 'Modelo cargado'

#esto convendría hacerlo con rutas relativas 
model.save_word2vec_format(sys.argv[1]+'.txt', binary=False)

print 'Finalizado'
