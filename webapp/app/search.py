#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 21:58:18 2019

@author: Nan
"""

import pandas as pd
import numpy as np

import dill as pickle

class BellaSearch(object):
    """Semantic search models, sentiment analysis and search for top products
    """
    def __init__(self):
        """
        """
        pass
    
    def test(self):
        return 'You did it!'
    
    def CustomizedSearch(self, concerns, category,
                         model_type='fasttext', n_similar_words=10, n_product=3):
        """Search for reviews containing words semantically similar to keywords
        and sum up sentiment score by products. Return products with highest 
        score.
        concerns: string seperated by comma, e.g. wrinkle,pore
        ft: fast text word embedding model trained on reviews
        w2v: word2vec embedding model trained on reviews
        product_fp: product information file path.
        review_fp: review information file path, containing sentiment scores.
        model: word embedding models, fasttext or word2vec
        """
        review_fp = '/Users/Nan/Documents/insight/bella/bella/bellaflask/tmp/review_sentiment.df.pk'
        with open(review_fp,'rb') as f:
            reviews = pickle.load(f)
        #reviews = reviews[reviews['r_category'] == category, ]
        
        model_fp = '/Users/Nan/Documents/insight/bella/bella/bellaflask/tmp/word2vec.pk'
        if model_type == 'fasttext':
            model_fp = '/Users/Nan/Documents/insight/bella/bella/bellaflask/tmp/fasttext.pk'
        with open(model_fp,'rb') as f:
            embedding_model = pickle.load(f)
        print('Word embedding model loaded')
            
        topn = self.concern_score(reviews, concerns, embedding_model, 
                                      n_similar_words, n_product)
        product_fp = '/Users/Nan/Documents/insight/bella/bella/bellaflask/tmp/product_info.df.pk'
        with open(product_fp,'rb') as f:
            product_df = pickle.load(f)
        product_df = product_df[product_df['p_category'] == category]
        print('Product file loaded')

        products = self.search_product(product_df, topn)
        return products
    
    def feature_score(self, df, key_words, review_column='reviews'):
        """Calculate scores based on one concern related reviews' sentiment score.
        df: dataframe, review file parsed by parse_reviewTable(), with 'review'
        column containing title and text of reviews and 'r_product' containing
        product ID.
        key_words: results of semantic search, or words similar to one feature
        word. This will be a list of tuple, e.g. [('w1', 0.3), ('w2', 0.2)]
        """
        #fastext missspelling
        feature_score = df.apply(lambda row: \
                                           sum(np.multiply([w in row['review'] \
                                                      for w in key_words.keys()], 
                                                      key_words.values())) * \
                                           row['senti_score'], 
                                 axis=1)
        return feature_score
    
    def concern_score(self, df, concerns, embedding_model, n_similar_words=10, n_product=5):
        """Sum up scores based on every concern.
        df: dataframe, review file parsed by parse_reviewTable(), with 'review'
        column containing title and text of reviews and 'r_product' containing
        product ID.
        concerns:a string from request, concerns seperated by comma.
        embedding_model: word embedding model trained on reviews, can be 
                         fasttext or word2vec.
        n_similiar_words: number of similar words to be considered.
        n_product: number of products to recommend.
        """
        concerns = map(lambda w: w.strip(), concerns.split(','))
        key_words = {}
        for concern in concerns:
            words = embedding_model.wv.most_similar(positive=concern, 
                                                  topn=n_similar_words)
            for w, v in words:
                key_words[w] = key_words.get(w, 0) + v
        c_score = self.feature_score(df, key_words, review_column='reviews')
        df['concern_score'] = c_score
        product_score = df.groupby(['r_product'])[['concern_score']].sum()
        #product_score = product_score.sort_values(by='concern_score', 
         #                                         ascending=False)
        #top_products = product_score[:n_product].index.values
        top_products = product_score.nlargest(n_product, 'concern_score').index.values
        return top_products
    
    def search_product(self, df, top_product_id, 
                       columns=['p_Brand', 'p_Name', 'p_function', 'p_link', 'p_image']):
        """Look for product based on product id, return brand brand, 
        product name, functions, shopping link, image link.
        fp: file path of product information file.
        top_product_id: a list of top n product IDs used by sephora, e.g. P404010
        columns: product dataframe columns to be retained as necessary 
                 infoemation present to users
        """
        tops = df[df['p_ID'].isin(top_product_id)]
        tops = tops[columns]
        return tops.to_dict('records')
