#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 15:40:07 2019

@author: Nan
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
#from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.colors import ListedColormap
from io import BytesIO
import base64
import sys

import dill as pickle

class BellaModel(object):
    """Prediction model from reviews to rating. Give feature importance ranking.
    """
    def __init__(self):
        """
        """
        self.db_fp = '/Users/Nan/Documents/insight/bella/bella/bellaflask/tmp/'
        #self.db_fp = '/home/ubuntu/bellaflask/tmp/'
    
    def PredictRating(self, category, text):
        """
        """
        #document to count vector
        doc_vectorizer_fp =  self.db_fp + 'cnt_vectorizer.pk'
        with open(doc_vectorizer_fp,'rb') as f:
             doc_vectorizer = pickle.load(f)
        text_vec = doc_vectorizer.transform([text])
        #document to topic vector
        topic_model_fp = self.db_fp + 'lda_topic_model.pk'
        with open(topic_model_fp,'rb') as f:
             topic_model = pickle.load(f)
        topic_vec = topic_model.transform(text_vec)
        #predict rating
        predict_model_fp = self.db_fp + 'lda_GB.model.pk'
        with open(predict_model_fp,'rb') as f:
             predict_model = pickle.load(f)
        rate = predict_model.predict(topic_vec)
        if rate == True:
            rating = 'love it!'
        else:
            rating = 'meh...'
        #show feature importance plot
        #self.PlotFeatureImportance(model)
        return rating
            
    
    def PlotFeatureImportance(self):
        """Plot ranked importance of features
        """
        predict_model_fp = self.db_fp + 'lda_GB.model.pk'
        with open(predict_model_fp,'rb') as f:
             model = pickle.load(f)
        importances = model.feature_importances_
        feature_importances = pd.DataFrame({'feature': np.argsort(importances)[::-1], 
                                            'importance':importances})
        feature_importances = feature_importances.sort_values(by='importance', 
                                                              ascending=False)
        topic_order = feature_importances.feature

        # Plot the feature importances of the forest
        # Initialize the matplotlib figure
        fig = Figure()
        ax = fig.add_subplot(1, 1, 1)
        img = StringIO.StringIO()
        sns.set_color_codes('pastel')
        ax = sns.barplot(x='importance', y='feature', data=feature_importances,
                    label='importance', orient='h', order=topic_order)
        #ax.barh(feature_importances['feature'], 
        #        feature_importances['importance'], align='center')
        # Add a legend and informative axis label
        ax.set(ylabel='Topics', xlabel='Topic importance')
        #canvas = FigureCanvas(fig)
        #output = StringIO.StringIO()
        #canvas.print_png(output)
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        return plot_url
    
    def topic_summary(self, topic, category, random=False, n=5):
        """
        """
        topic_num = int(topic)
        fp = self.db_fp + 'lda_vectors.tsv'
        #with open(fp,'rb') as f:
        #     topics = pickle.load(f)
        topics = pd.read_table(fp)
        topic_df = topics[topics['dominant_topic'] == topic_num]
        #less document than requested number
        n = min(n, topic_df.shape[0])
        if random:
            reviews = self.PullReviews(topic_df, n=n)
        else:
            topic_df = topic_df.sort_values(topic, ascending=False)
            reviews = topic_df['review'].head(n)
        plot_url =  self.PlotReviewerDistribution(topic_df, category)
        return reviews, plot_url
        
    def PullReviews(self, topic_df, n=5):
        """Pull representative reviews for specific topic
        topic: a topic in reviews, request from drop down menu
        """
        texts = topic_df['review'].sample(n=n)   
        return texts
        
    def PlotReviewerDistribution(self, topic_df, category):
        """Plot a stacked area bar plot of reviewers make reviews in one topic.
        X is ratings, stacked by selected reviewer category, such as skin 
        concerns, skin types and age.
        topic: a topic in reviews, request from drop down menu 
        category: category to stratify reviewers, e.g. skin 
        concerns, skin types and age
        """
        df = pd.DataFrame(topic_df.groupby(['r_star', category]).count()['0'])
        df.reset_index(inplace=True)  
        df = df.pivot(index='r_star', columns=category, values='0')
        fig = Figure()
        ax = fig.add_subplot(1, 1, 1)
        img = BytesIO()
        df.plot.bar(stacked=True, 
                    colormap=ListedColormap(sns.color_palette('pastel')))
        ax.set(ylabel='Counts', xlabel='Stars')
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        return plot_url
        
        
            
    