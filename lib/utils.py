#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 22:12:43 2019

@author: Nan
"""

#!/usr/bin/env python2
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
from sklearn.decomposition import PCA, 
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
        tsne_model = TSNE(perplexity=40, n_components=2, init='pca', 
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
            
            
    """ review_parts = parse_reviewTable(fp, products='all')
    #drop cuplicates in tokenized text first, otherwise there will be error
    #in k means
    reviews = review_parts['review'].drop_duplicates()
    sense_reviews = remove_nonsense(reviews, nonsense_sample=nonsense_samples)
    clean_reviews = reviews.map(clean)
    
    tokenized_text = reviews.map(wordToken)
    volcabulary, vectors = w2v_model(tokenized_text)
    assigned_clusters, dic = Kmeans(volcabulary, vectors, n_cluster=10)
    TSNE_clustering(vectors, volcabulary, 3)
    
    #reviews.map(lambda s:len(s.split())).mean()
    cnt_vectorizer, cnt = count_vec(clean_reviews, 
                                    max_df=0.3, 
                                    min_df=2,
                                    ngram_range=(3,3),
                                    n_features=1000)
    lda_topics = LDA_topic(cnt_vectorizer, cnt, n_topic=20)
    
    
    tfidf_vectorizer, tfidf = TF_IDF(reviews, 
                                     max_df=0.15, 
                                     min_df=2, 
                                     ngram_range=(8,10), 
                                     n_features=1000)
    
    nmf_topics = NMF_topic(tfidf_vectorizer, tfidf, n_topic=8, n_keyword=20)
    review_vector = tfidf_vectorizer.transform(tokenized_text).toarray()
    
    
        
        w2v = models.KeyedVectors \
                    .load_word2vec_format("../GoogleNews-vectors-negative300.bin",
                                          binary=True)
    """
    