#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 22:10:54 2019

@author: Nan
"""
import pandas as pd
from collections import defaultdict

import matplotlib.pyplot as plt
import seaborn as sns

import nltk
from nltk.cluster.kmeans import KMeansClusterer

from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
	
#import pyLDAvis.sklearn

class BellaUtils(object):
    """All parse, clean and preprocess
    """
    def __init__(self):
        """
        """
        pass
        
    def Kmeans(self, volcabulary, vectors, n_cluster):
        """K-means clustering based on cosine similarity of word2vec.
        """
        kclusterer = KMeansClusterer(n_cluster, 
                                     distance=nltk.cluster.util.cosine_distance, 
                                     repeats=10,
                                     avoid_empty_clusters=True)
        assigned_clusters = kclusterer.cluster(vectors, assign_clusters=True)
        dic = defaultdict(list)
        for c, w in zip(assigned_clusters, volcabulary):
            dic[c].append(w)
        return assigned_clusters, dic
    
    def TSNE_clustering(self, f_name, vectors, volcabulary):
        """Creates and TSNE model and plots it
        """
        tsne_model = TSNE(perplexity=40, n_components=8, init='pca', 
                          n_iter=2500, random_state=23)
        new_values = tsne_model.fit_transform(vectors)

        x = []
        y = []
        for value in new_values:
            x.append(value[0])
            y.append(value[1])
        
        plt.figure(figsize=(16, 16)) 
        for i in range(len(x)):
            plt.scatter(x[i],y[i])
            plt.annotate(volcabulary[i],
                     xy=(x[i], y[i]),
                     xytext=(5, 2),
                     textcoords='offset points',
                     ha='right',
                     va='bottom')
        plt.show()
        plt.savefig(f_name + '.' + x + '-' + y + '.png')
        #TSNE(replace kmeans check duplicates and )
        #glove fasttext bert
        
    def PCA_plot(self, vectors, color_cat, f_name, n_components=3):
        """Generate PCA plot from word2vec or GloVe vectors.
        vectors: a list of vectors representing different words.
        color_cat: assigned clusters or other info to color data points.
        """
        pca = PCA(n_components=n_components)
        pca_v = pca.fit_transform(vectors)
        pca_v = pd.DataFrame(pca_v, columns=['PC1', 'PC2', 'PC3'])
        pca_v['color'] = color_cat
    
        for x, y in [('PC1', 'PC2'), ('PC1', 'PC3')]:
            plt.figure()
            sns.set()
            sns.lmplot(x=x, y=y, data=pca_v, 
                       hue='color', fit_reg=False, scatter_kws={'s': 10})
            plt.savefig(f_name + '.' + x + '-' + y + '.png')
            
    
    def log_likelyhood_plot(self, grid_model, params, fname):
        """Plot log likelyhood change as params change.
        grid_model: gird search model
        params: grid search parameters, include learning decay and topic numbers.
         e.g. {'n_components': [10, 15, 20, 25, 30], 
         'learning_decay': [.5, .7, .9]}
        """
        cv_results = grid_model.cv_results_
        params_n = cv_results['param_n_components'].data
        params_decay = cv_results['param_learning_decay'].data
        score = cv_results['mean_test_score']
        data = pd.DataFrame({'log_likelyhood':score, 
                             'n_topics':params_n, 
                             'learning_decay':params_decay})
        plt.figure()
        sns.set_color_codes('pastel')
        sns.catplot(x='n_topics', y='log_likelyhood', hue='learning_decay',
                    data=data, kind='point', palette='pastel')
        plt.savefig(fname + '.jpg')    
            
