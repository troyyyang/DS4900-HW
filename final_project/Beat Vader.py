#!/usr/bin/env python
# coding: utf-8

# ### Importing libraries and defining utility functions

# In[1]:


import pandas as pd
import numpy as np
import re, string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import CountVectorizer  
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import confusion_matrix
import GetOldTweets3 as got
import warnings
pd.options.display.max_rows = 999
pd.options.display.max_columns = 999
pd.options.display.max_colwidth = 1000
warnings.filterwarnings('ignore')


# In[2]:


def accuracy(actual, pred):
    true = 0
    for i in range(len(pred)):
        if actual[i] == round(pred[i]):
            true +=1
    return true/len(pred)


# In[3]:


def lemmatizer(tweet):
    tweet = tweet.split()
    stemmer = WordNetLemmatizer()
    lemmed = [stemmer.lemmatize(word) for word in tweet]
    return ' '.join(lemmed)


# In[4]:


def to_label(score):
    if score > .05:
        return 1
    elif score < -.05:
        return 2
    else:
        return 0


# In[5]:


def clean_text(text):
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', '', text)
    text = re.sub('@[^\s]+', '', text)
    text = re.sub('#([^\s]+)', '', text)
    text = regex.sub('', text)
    text = text.strip()
    return text


# ### Reading in data and doing some preprocessing and cleaning

# In[6]:


train = pd.read_csv('Tweets_airline.csv',encoding = "ISO-8859-1")


# In[7]:


train['airline_sentiment'] = train['airline_sentiment'].replace('neutral', 0)


# In[8]:


train['airline_sentiment'] = train['airline_sentiment'].replace('positive', 1)


# In[9]:


train['airline_sentiment'] = train['airline_sentiment'].replace('negative', 2)


# In[10]:


train['text'] = train['text'].map(lambda x: clean_text(x))


# In[11]:


train['text'] = train['text'].map(lambda x: lemmatizer(x))


# In[12]:


text = train['text'].values


# In[13]:


text.shape


# In[14]:


label = train['airline_sentiment'].values


# In[15]:


label.shape


# In[16]:


X_train, X_test, y_train, y_test = train_test_split(text, label)


# ### Defining pipelines and parameter grids to search over for logistic regression

# Using TF-IDF

# In[17]:


parameters_lr = {
    'lr__C': (.01,0.1, 0.5,1),
    'lr__solver' : ('newton-cg', 'sag', 'saga', 'lbfgs')
}

pipeline_lr = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words = 'english')),
    ('lr', LogisticRegression(max_iter = 400))
])

grid_lr = GridSearchCV(pipeline_lr, parameters_lr, cv = 3)
grid_lr.fit(X_train, y_train)

results_lr = pd.DataFrame.from_dict(grid_lr.cv_results_)
print(results_lr)


# Using BOW

# In[18]:


parameters_lr = {
    'lr__C': (.01,0.1, 0.5,1),
    'lr__solver' : ('newton-cg', 'sag', 'saga', 'lbfgs')
}

pipeline_lr = Pipeline([
    ('bow',  CountVectorizer(max_features=5000, min_df=5, max_df=0.9, stop_words='english')  ),
    ('lr', LogisticRegression(max_iter = 400))
])

grid_lr = GridSearchCV(pipeline_lr, parameters_lr, cv = 3)
grid_lr.fit(X_train, y_train)

results_lr = pd.DataFrame.from_dict(grid_lr.cv_results_)
print(results_lr)


# #### Evaluate best LR model on test data

# In[19]:


best_pipeline_lr = Pipeline([
    ('bow',  CountVectorizer(max_features=5000, min_df=5, max_df=0.9, stop_words='english')  ),
    ('lr', LogisticRegression( C = 1, solver = 'saga',max_iter = 400))
])

best_pipeline_lr.fit(X_train, y_train)
best_lr_preds = best_pipeline_lr.predict(X_test)

cr_best_lr = classification_report(y_test,best_lr_preds,output_dict=True)
pd.DataFrame(cr_best_lr).transpose()


# ### Defining pipelines and parameter grids to search over for naive bayes

# Using TF-IDF

# In[20]:


parameters_nb = {
    'nb__alpha': (0.00001, 0.5, 1),
    'nb__fit_prior' : (True, False)
}

pipeline_nb = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words = 'english')),
    ('nb', MultinomialNB())
])


grid_nb = GridSearchCV(pipeline_nb, parameters_nb, cv = 3)
grid_nb.fit(X_train, y_train)

results_nb = pd.DataFrame.from_dict(grid_nb.cv_results_)
print(results_nb)


# Using BOW

# In[21]:


parameters_nb = {
    'nb__alpha': (0.00001, 0.5, 1),
    'nb__fit_prior' : (True, False)
}

pipeline_nb = Pipeline([
    ('bow',  CountVectorizer(max_features=5000, min_df=5, max_df=0.9, stop_words='english') ),
    ('nb', MultinomialNB())
])

grid_nb = GridSearchCV(pipeline_nb, parameters_nb, cv = 3)
grid_nb.fit(X_train, y_train)

results_nb = pd.DataFrame.from_dict(grid_nb.cv_results_)
print(results_nb)


# #### Evaluate best NB model on test data

# In[22]:


best_pipeline_nb = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words = 'english')),
    ('nb', MultinomialNB(alpha = .5, fit_prior = False))
])

best_pipeline_nb.fit(X_train, y_train)
best_nb_preds = best_pipeline_nb.predict(X_test)

cr_best_nb = classification_report(y_test,best_nb_preds,output_dict=True)
pd.DataFrame(cr_best_nb).transpose()


# ### Defining pipelines and parameter grids to search over for adaboost

# Using TF-IDF

# In[23]:


parameters_ada = {
    'ada__n_estimators': (500,1000),
}

pipeline_ada = Pipeline([
    ('bow',  CountVectorizer(max_features=5000, min_df=5, max_df=0.9, stop_words='english') ),
    ('ada', AdaBoostClassifier())
])

grid_ada = GridSearchCV(pipeline_ada, parameters_ada, cv = 3)
grid_ada.fit(X_train, y_train)

results_ada = pd.DataFrame.from_dict(grid_ada.cv_results_)
print(results_ada)


# Using BOW

# In[24]:


parameters_ada = {
    'ada__n_estimators': (500,1000),
}

pipeline_ada = Pipeline([
    ('bow', TfidfVectorizer(stop_words = 'english')) ,
    ('ada', AdaBoostClassifier())
])

grid_ada = GridSearchCV(pipeline_ada, parameters_ada, cv = 3)
grid_ada.fit(X_train, y_train)

results_ada = pd.DataFrame.from_dict(grid_ada.cv_results_)
print(results_ada)


# #### Evaluate best Adaboost model on test data

# In[25]:


best_pipeline_ada = Pipeline([
    ('bow',  CountVectorizer(max_features=5000, min_df=5, max_df=0.9, stop_words='english') ),
    ('ada', AdaBoostClassifier(n_estimators = 500))
])

best_pipeline_ada.fit(X_train, y_train)
best_ada_preds = best_pipeline_ada.predict(X_test)

cr_best_ada = classification_report(y_test,best_ada_preds,output_dict=True)
pd.DataFrame(cr_best_ada).transpose()


# ### Evaluating the pre-trained model "Vader"

# In[26]:


analyser = SentimentIntensityAnalyzer()
vader_preds_raw = train['text'].map(lambda x: analyser.polarity_scores(x)['compound'])
vader_preds = vader_preds_raw.map(lambda x: to_label(x)).tolist()
labels = train['airline_sentiment'].tolist()


# In[27]:


cr_vader = classification_report(labels,vader_preds,output_dict=True)
pd.DataFrame(cr_vader).transpose()


# ### Assessing the model on my labeled data

# In[28]:


tweets = pd.read_csv('Tweets.csv')


# In[29]:


tweets['Tweet'] = tweets['Tweet'].map(lambda x: clean_text(x))


# In[30]:


tweets['Tweet'] = tweets['Tweet'].map(lambda x: lemmatizer(x))


# In[31]:


test_x = tweets['Tweet'].values


# In[32]:


label = tweets['Sentiment']


# In[33]:


label = list(map(lambda x: 0 if x == 0.1 else 1,label))


# In[34]:


test_preds = best_pipeline_lr.predict(test_x)


# In[35]:


test_preds = list(map(lambda x: 1 if x > 0 else 0,test_preds.tolist()))


# In[36]:


accuracy(label,test_preds)


# In[37]:


results = list(zip(label,test_preds,tweets['Tweet'].tolist()))


# In[38]:


results = pd.DataFrame(results, columns = ['actual','predicted','tweet'])


# In[39]:


results.loc[results['actual']!=results['predicted']]


# In[102]:


feature_names = best_pipeline_lr.steps[0][1].get_feature_names()
for i, class_label in enumerate([0,1,2]):
    top = np.argsort(best_pipeline_lr.steps[1][1].coef_[i])[-50:]
    print("%s: %s" % (class_label," ".join(feature_names[j] for j in top)))
    print('\n')


# ### Get 2 test data sets for third party evaluators

# In[73]:


tweetCriteria = got.manager.TweetCriteria().setQuerySearch('boston bruins')                                           .setSince("2019-03-01")                                           .setUntil("2019-04-01")                                           .setMaxTweets(100)                                           .setTopTweets(True)
tweets = got.manager.TweetManager.getTweets(tweetCriteria)


# In[74]:


validation_tweets = []
for tweet in tweets:
    validation_tweets.append(tweet.text)
    


# In[75]:


validation_tweets = pd.DataFrame(validation_tweets, columns = ['tweet'])


# In[76]:


tweet_x = validation_tweets['tweet'].map(lambda x: clean_text(x))


# In[77]:


tweet_x = tweet_x.map(lambda x: lemmatizer(x))


# In[78]:


validation_x = tweet_x.values


# In[79]:


validation_preds = best_pipeline_lr.predict(validation_x)


# In[80]:


validation_preds = list(map(lambda x: 1 if x > 0 else 0,validation_preds.tolist()))


# In[81]:


validation_tweets['prediction'] = validation_preds


# In[83]:


validation_tweets.to_csv('validation.csv', index = False)


# In[84]:


validated = pd.read_csv('validation.csv')


# In[98]:


len(validated.loc[(validated['tester_one']==validated['tester_two']) & (validated['tester_one']==validated['prediction'])])


# In[99]:


len(validated.loc[(validated['tester_one']==validated['tester_two'])])


# In[ ]:





# In[ ]:




