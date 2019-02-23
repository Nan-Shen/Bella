#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 22:10:54 2019

@author: Nan
"""
from collections import defaultdict

from gensim.models.coherencemodel import CoherenceModel

#from glove import Glove, Corpus

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.model_selection import GridSearchCV


class BellaTopics(object):
    """All parse, clean and preprocess
    """
    def __init__(self):
        """
        """
        pass
    
    def TF_IDF(self, reviews, max_df=0.15, min_df=2, ngram_range=(1,1), 
                               n_features=1000):
        """reweight word counts or importance in a review 
        by removing common word used in all reviews, like 'love', 'skin'.
        Term Frequency - Inverse Document Frequency (TF-IDF)
        reviews: normalized reviews
        """
        tfidf_vectorizer = TfidfVectorizer(max_df=max_df, min_df=min_df, 
                                           ngram_range=ngram_range,
                                           max_features=n_features, 
                                           stop_words='english')#or 'engilish'
        #max_features=no_features, 
        tfidf = tfidf_vectorizer.fit_transform(reviews)
        #frequencies = sum(tfidf).toarray()[0]
        #w_tfidf = pd.DataFrame(frequencies, 
        #                          index=tfidf_vectorizer.get_feature_names(), 
        #                          columns=['frequency'])
       # w_tfidf = w_tfidf.sort_values('frequency', ascending = False)
        return tfidf_vectorizer, tfidf
    
    def NMF_topic(self, vectorizer, tfidf, n_topic, n_keyword=20):
        """Fit nmf model (generalized Kullback-Leibler divergence) with
         tf-idf features.
        """
        nmf = NMF(n_components=n_topic, random_state=1, 
                  beta_loss='kullback-leibler', solver='mu', 
                  max_iter=1000, alpha=.1, l1_ratio=.5).fit(tfidf)
        tfidf_feature_names = vectorizer.get_feature_names()
        r_concerns = defaultdict(list)
        for topic_idx, topic in enumerate(nmf.components_):
            for i in topic.argsort()[:-n_keyword - 1:-1]:
                r_concerns[topic_idx].append(tfidf_feature_names[i])
        return r_concerns, nmf
                  #n_components = 8, max_df = 0.2
        #n_components = 10, max_df = 0.15
        
    def count_vec(self, tokenized_text, max_df=0.8, min_df=2, ngram_range=(1,1),
                                  n_features=1000):
        """Turn reviews to a vector of counts of each word.
        """
        cnt_vectorizer = CountVectorizer(max_df=max_df, min_df=min_df, 
                                        max_features=n_features,
                                        ngram_range=ngram_range,
                                        token_pattern='[a-zA-Z0-9]{3,}',
                                        stop_words='english')
        cnt = cnt_vectorizer.fit_transform(tokenized_text)
        return cnt_vectorizer, cnt
        
    def LDA_topic(self, cnt_vectorizer, cnt, n_topic, n_keyword=20):
        """
        """
        lda = LatentDirichletAllocation(n_topics=n_topic, 
                                        max_iter=5, learning_method='online', 
                                        learning_offset=50.,
                                        random_state=0).fit(cnt)
        lda_feature_names = cnt_vectorizer.get_feature_names()
        r_concerns = defaultdict(list)
        for topic_idx, topic in enumerate(lda.components_):
            for i in topic.argsort()[:-n_keyword - 1:-1]:
                r_concerns[topic_idx].append(lda_feature_names[i])
        return(r_concerns, lda)
    
    def Coherence_Score(model, metric='c_v'):
        """Calculate coherence score using c_v or Umass.
        """
        coherence_model_lda = CoherenceModel(model=model, 
                                             texts=docs, dictionary=dictionary, 
                                             coherence="u_mass")
        coherence_lda = coherence_model_lda.get_coherence()
        
    def Best_topic_model(self, params, model, vectors):
        """Search for the best topic model parameters. 
        params: grid search parameters. e.g. {'n_components': 
            [10, 15, 20, 25, 30], 'learning_decay': [.5, .7, .9]}
        model: topic model.
        vector: vectorized data.
        """
        grid_model = GridSearchCV(model, param_grid=params)
        grid_model.fit(vectors)
        best_model = grid_model.best_estimator_
        print("Best Model's Params: ", grid_model.best_params_)
        print("Best Log Likelihood Score: ", grid_model.best_score_)
        print("Model Perplexity: ", best_model.perplexity(vectors))
        return grid_model
        
      
        