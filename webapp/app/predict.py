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
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import StringIO
import base64

import dill as pickle

class BellaModel(object):
    """Prediction model from reviews to rating. Give feature importance ranking.
    """
    def __init__(self):
        """
        """
        pass
    
    def PredictRating(self, category, text):
        """
        """
        #document to count vector
        doc_vectorizer_fp = '/Users/Nan/Documents/insight/bella/bella/bellaflask/tmp/cnt_vectorizer.pk'
        with open(doc_vectorizer_fp,'rb') as f:
             doc_vectorizer = pickle.load(f)
        text_vec = doc_vectorizer.transform([text])
        #document to topic vector
        topic_model_fp = '/Users/Nan/Documents/insight/bella/bella/bellaflask/tmp/lda_topic_model.pk'
        with open(topic_model_fp,'rb') as f:
             topic_model = pickle.load(f)
        topic_vec = topic_model.transform(text_vec)
        #predict rating
        predict_model_fp = '/Users/Nan/Documents/insight/bella/bella/bellaflask/tmp/lda_GB.model.pk'
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
        predict_model_fp = '/Users/Nan/Documents/insight/bella/bella/bellaflask/tmp/lda_GB.model.pk'
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
                    label='importance', color='b', orient='h', order=topic_order)
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
        
    def PullReviews(self, topic):
        """Pull representative reviews for specific topic
        topic: a topic in reviews, request from drop down menu
        """
        topic_dic_fp = ''
        with open(topic_dic_fp,'rb') as f:
             topic_dic = pickle.load(f)
        return topic_dic[topic]
        
    def PlotReviewerDistribution(self, topic, category):
        """Plot a stacked area bar plot of reviewers make reviews in one topic.
        X is ratings, stacked by selected reviewer category, such as skin 
        concerns, skin types and age.
        topic: a topic in reviews, request from drop down menu 
        category: category to stratify reviewers, e.g. skin 
        concerns, skin types and age
        """
        reviewer_dic_fp = ''
        with open(topic_dic_fp,'rb') as f:
             reviewer_dic = pickle.load(f)
        from matplotlib.colors import ListedColormap
        df.set_index(category)\
          .reindex(df.set_index(category).sum().sort_values().index, axis=1)\
          .T.plot(kind='bar', stacked=True,
              colormap=ListedColormap(sns.color_palette("GnBu", 10)), 
              figsize=(12,6))
        columns=["App","Feature1", "Feature2","Feature3",
                           "Feature4","Feature5",
                           "Feature6","Feature7","Feature8"], 
        return topic_dic[topic]
        
        
            
    