#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 20 22:25:39 2019

@author: Nan
"""
import pandas as pd
import re
import string

from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer

class BellaParse(object):
    """All parse, clean and preprocess
    """
    def __init__(self):
        """
        """
        self.exclude = set(string.punctuation) 
        self.stop = list(self.exclude) + stopwords.words('english')
        self.snowball = SnowballStemmer('english')
        self.lemma = WordNetLemmatizer()
        self.tokenizer = RegexpTokenizer(r'\w+')
        self.regex = re.compile('[^a-zA-Z ]')
        self.printable = set(string.printable)
        self.nonsense_samples = ('i have', 'i also have', 'i\'m', 'i had',
                            'i\'ve been', 'i thought', 'i was ', 'i use ',
                            'i used to', 'if you have', 'i suffer')
        
    def parse_reviewTable(self, fp, short_sentence=True, products='all'):
        """Load all reviews of give list or all products in data. Remove
        diplicates.
        fp: file path of scraped reviews.
        products: 'all' to include all products or a list of product ID. e.g.
          producst = ['P67898', 'P89098']
        """
        tb = pd.read_table(fp)
        tb['r_time'] = pd.to_datetime(tb['r_time'], format='%Y-%m-%dT%H:%M:%S', 
                     errors='coerce')
        tb['r_content'] = tb['r_title'] + '. ' + tb['r_text']
        tb = tb.dropna(subset=['r_content'])
        #remove non-ascii signs
        tb['r_content'] = tb['r_content'] \
                          .map(lambda s: ''.join(filter(lambda x: x in self.printable, s)))
        if short_sentence == True:
            tb['r_parts'] = tb['r_content'].map(self.split_sentence)
        else:
            tb['r_parts'] = tb['r_content']
        #transform table to put each part of review into one row
        review_parts = tb.r_parts.apply(pd.Series) \
                         .merge(tb, right_index = True, left_index = True) \
                         .drop(['r_text', 'r_title', 'r_content', 'r_parts'], axis = 1) \
                         .melt(id_vars = ['r_product', 'r_reviewer', 
                                          'r_time', 'r_star'], 
                               value_name = 'review') \
                         .drop('variable', axis = 1) \
                         .dropna(subset=['review'])
        return review_parts
    
    def sentenceToken(self, text):
        """Split review context into a list of sentences.
        Text: a sentence.
        """
        punkt_param = PunktParameters()
        punkt_param.abbrev_types = set(['dr', 'vs', 'mr', 'mrs'])
        tokenizer = PunktSentenceTokenizer(punkt_param)
        return tokenizer.tokenize(text)
    
    def split_sentence(self, text, long_threshold=50):
        """Split one review into sentences and then split each sentence 
        with more than one topics to parts.
        text: one review.
        """
        sentences = self.sentenceToken(text)
        short = []
        for sentence in sentences:
            if len(sentence) >= long_threshold:
                parts = re.split('&|!|;|and|,|~|but|\.|so i|\s-\s|\(|\)', 
                                 sentence.lower())
                parts = filter(lambda w: len(w) > 0, 
                               map(lambda w: w.strip(), parts))
                short += parts
            else:
                short.append(sentence.lower())
        return list(short)
    
    def remove_nonsense(self, reviews, nonsense_sample):
        """Remove some review parts do not carry much information.
        reviews: series of short sentences of reviews
        nonsense_sample: a tuple of nonsense review examples
        """
        sense_reviews = filter(lambda s: len(s) > 13 
                               and not s.startswith(nonsense_sample)
                               and not ('i do have' in s)
                               and not ('looking for' in s)
                               and not ('i purchase' in s)
                               and not ('i bought' in s), 
                               reviews)
        return list(sense_reviews)
        
    def clean(self, text):
        """ remove stop words, lemmatized and stemming given text.
        """
        clean_text = self.regex.sub('', text)
        #correct_text = TextBlob(clean_text).correct()
        no_stop = ' '.join(filter(lambda w: w not in self.stop, clean_text.split()))
        lemmatized = self.lemma.lemmatize(no_stop, pos='v')
        normalized = ' '.join(map(self.snowball.stem, lemmatized.split(' ')))
        return normalized
    
    def wordToken(self, text):
        """Tokenize given text
         lemmatized: words in third person are changed to first person and 
         verbs in past and future tenses are changed into present.
        text: string.
        """
        tokenizer_regex = re.compile(r'[\s]')
        tokens = [tok.strip().lower() for tok in tokenizer_regex.split(text)]
        return tokens
     
    def parse_product(self, df):
        """Parse product information file, return product link, image, and skin
        concerns it solves.
        fp: file path of product file.
        """
        #df = pd.read_table(fp)
        functions = []
        for i in range(df.shape[0]):
            des = df['p_description'].iloc[i]
            try:
                func = re.findall('Solutions for:([\S\s]+.)'\
                                       'If you want to know more', des)[0]
                functions.append(func.split('.')[0])
            except:
                try:
                    func = re.findall('Skincare Concerns:([\S\s]+.)'
                                           'Formulation:', des)[0]
                    functions.append(func.split('.')[0])
                except:
                    try:
                        func = re.findall('What it is:([\S\s]+.)', des)[0]
                        functions.append(func.split('.')[0])
                    except:
                        functions.append('NA')
        df['p_function'] = functions
        return df
            
