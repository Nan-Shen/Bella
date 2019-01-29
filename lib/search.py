
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 21:58:18 2019

@author: Nan
"""

import pandas as pd
import re

from gensim.models import Word2Vec, FastText

from textblob import TextBlob

class BellaSearch(object):
    """Semantic search models, sentiment analysis and search for top products
    """
    def __init__(self):
        """
        """
        pass
    
    def CustomizedSearch(self, concerns, ft, w2v, product_fp, review_fp,
                         model='fasttext', n_similar_words=10, n_product=3):
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
        df = pd.read_table(review_fp)
        if model == 'fasttext':
            topn = self.concern_score(df, concerns, ft, n_similar_words, n_product)
        elif model == 'word2vec':
            topn = self.concern_score(df, concerns, w2v, n_similar_words, n_product)
        
        brands = []
        names = []
        functions = []
        links = []
        images = []
        for product_id in topn:
            p_Brand, p_Name, p_function, \
                     p_link, p_image =  self.search_product(product_fp, 
                                                            product_id)
            brands.append(p_Brand)
            names.append(p_Name)
            functions.append(p_function)
            linksa.append(p_link)
            images.append(p_image)
            
        
    def w2v_model(self, tokenized_text, size=150, window=10):
        """Train a word2vec model, get embeddings for semantic search of query.
        docs: tf-idf vectors or tokenized documents.
        """
        model = Word2Vec(tokenized_text, size=size, window=window, min_count=1)
        #model.save('word2vec.model')
        #model.train(tokenized_text, total_examples=len(tokenized_text), 
        #            epochs=10)
        volcabulary = model.wv.vocab.keys()
        vectors = model[model.wv.vocab]
        return model, volcabulary, vectors
    
    def fasttext_model(self, tokenized_text, size=150, window=10):
        """Train a word2vec model, get embeddings for semantic search of query.
        docs: tf-idf vectors or tokenized documents.
        """
        model = FastText(tokenized_text, size=size, window=window, 
                         min_count=1, iter=10)
        volcabulary = model.wv.vocab.keys()
        vectors = model[model.wv.vocab]
        return model, volcabulary, vectors
    
    def sentiment(self, text):
        """Get sentiment score of tweet content
        """
        sentiScore = TextBlob(text).sentiment.polarity
        return sentiScore
    
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
                                        sum([int(w[0] in row['review'])* w[1] \
                                             for w in key_words]), \
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
        c_score = [0] * df.shape[0]
        concerns = concerns.split(',')
        for concern in concerns:
            key_words = embedding_model.wv.most_similar(positive=concern, 
                                                  topn=n_similar_words)
            f_score = self.feature_score(df, key_words, review_column='reviews')
            c_score = map(sum, zip(c_score, f_score))
        df['concern_score'] = c_score
        product_score = df.groupby(['r_product'])[['concern_score']].sum()
        product_score = product_score.sort_values(by='concern_score', 
                                                  ascending=False)
        top_products = product_score['r_product'].head(n_product).values
        return top_products
    
    def parse_product(self, fp):
        """Parse product information file, return product link, image, and skin
        concerns it solves.
        fp: file path of product file.
        """
        df = pd.read_table(fp)
        functions = []
        for i in range(df.shape[0]):
            des = df['p_description'].iloc[i]
            try:
                functions.append(re.findall('Solutions for:([\S\s]+)'\
                                       'If you want to know more', des)[0])
            except:
                try:
                    functions.append(re.findall('Skincare Concerns:([\S\s]+)'
                                           'Formulation:', des)[0])
                except:
                    try:
                        functions.append(re.findall('What it is:([\S\s]+)'\
                                               'What it', des)[0])
                    except:
                        functions.append('NA')
        df['p_function'] = functions
        return df
    
    def search_product(self, fp, product_id):
        """Look for product based on product id, return brand brand, 
        product name, functions, shopping link, image link.
        fp: file path of product information file.
        product_id: product ID used by sephora, e.g. P404010
        """
        df = pd.read_table(fp)
        product = df[df['p_ID'] == product_id]
        return product[['p_Brand', 'p_Name', 'p_function', 
                             'p_link', 'p_image']].values[0]
        