# Bella Tella

## What is Bella?
Bella is a web app with two functions: 
1. To customers: provide personalized beauty products recommendations.
2. To Business: offer insights of customer segmentation.

You may check Bella_Tella.pdf for pipeline and summary report.

## How to use?
1. Open http://23552.club (B-E-L-L-A on cell phone keypad is 23552.)
2. For product recommendations, select Beauty Advisor button. Then, put in product type (currently only serum data has been collected) and type in features you want (e.g. good scent) or skin issues you have (e.g. acne) separated by comma. As long as there are reviews mentioning the same word, Bella will find all related reviews and give you products that people most satisfied with considering the input features.
3. For business insights, select Business Analyst button. Choose a topic and a feature of customers (e.g. skin type, age). Bella will give two reviews mainly talking about selected topic and a plot telling you how satisfying different customer subgroups feel about this topic.

## Script and models
1. Customer_semanticSearch_sentimentAnalysis.ipynb
This note covers preprocessing and training of word embedding models and contextual sentiment analysis. In the end, I compared ratings from reviewers worried about aging (information from Sephora customer data) of Bella and Sephora (built-in skin quiz: https://www.sephora.com/beauty/skin-care-quiz) recommended anti-aging products.
GloVe word embeddings example is in GloVE_wordEmbedding.ipynb.

2. Business_topicModeling.ipynb
This note contains scripts I used to generate topics used in Business Analyst page.

3. predictionModel.iphynb
I tried to build a prediction model with topic distribution in reviews. But topics alone cannot determine ratings (customer attitude). Then, I used topics in another way explained above.

## Dependency
You can copy and paste the text bellow, save it as bella_environment.yml. Then you can recreate my environment with "conda env create -f environment.yml".

name: bella
channels:
  - anaconda-fusion
  - defaults
  - conda-forge
dependencies:
  - python=3.7.2=haf84260_0
  - textblob=0.15.2=py_0
  - gensim=3.4.0=py37h1de35cc_0
  - nltk=3.4=py37_1
  - numpy=1.15.4=py37hacdab7b_0
  - numpy-base=1.15.4=py37h6575580_0
  - pandas=0.24.1=py37h0a44026_0
  - scikit-learn=0.20.2=py37h27c97d8_0
  - scipy=1.2.1=py37h1410ff5_0
  - seaborn=0.9.0=py37_0
  - snowballstemmer=1.2.1=py37_0
  - spacy=2.0.16=py37h6440ff4_0
  
prefix: ~/anaconda3/envs/bella

