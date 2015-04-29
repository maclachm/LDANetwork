__author__ = 'maclachm'
import numpy as np
import nltk
import textmining
import lda
import os
from nltk.stem.wordnet import WordNetLemmatizer

#This document makes use of a precomputed complete wordlist with the name 'wordlist.txt',
# this word list is used to compute the frequency distance for words in the vocabulary.
#Documents to be used in the LDA should be under the ./wikipedia directory with the extension '.abc.txt'
#Stop Word list should be in the main directory with the filename 'stoplist.txt'
#This process outputs a file of the JSON format with the name 'out.json'

files = []
for file in os.listdir("./wikipedia/"):
    if file.endswith("abc.txt"):
        files.append(file)

tdm = textmining.TermDocumentMatrix()
lmtzr = WordNetLemmatizer()

stop = nltk.word_tokenize(open('stoplist.txt').read())

os.chdir("./wikipedia/")
allWords =  nltk.word_tokenize(open('wordlist.txt').read())

fd = nltk.FreqDist(allWords)

for i in range(0, len(files)):
    with open(files[i]) as f:
        r = f.read()
        text = ' '
        rTok = nltk.word_tokenize(r)
        for word in rTok:
            if word in stop:
                continue
            else:
                if len(word) < 3 or '/' in word:
                    continue
                else:
                    if fd[word] < 2000 and fd[word] > 5:
                        v = lmtzr.lemmatize(word, 'v')
                        text += ' '+word

        tdm.add_doc(text)

f = []
for row in tdm.rows():
        f.append(row)
        #print row

nArr = np.array(f)
vocab = nArr[0] #vocab list
X = nArr[1:].astype(np.int) #matrix, entry[i,j] is count for word j in doc i


model = lda.LDA(n_topics=40, n_iter=1500, random_state=None)
model.fit(X)

topic_word = model.topic_word_

n = 20 #number of words to get for each topic
for i, topic_dist in enumerate(topic_word):
    topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n+1):-1]

doc_topic = model.doc_topic_

for n in range(50):
    sum_pr = sum(doc_topic[n,:])

os.chdir('..') #back to main directory
with open('out.json', 'w') as f: #tedious json writing
    s = '{ "nodes": [ '
    f.write(s)


for n in range(len(files)):
    topic_prob = doc_topic[n]
    topic_most_pr = doc_topic[n].argmax()
    name = files[n][:-8]

    s = '{{ "name" : "{}", "topic": {} }}'.format(name,topic_most_pr)

    if n != len(files)-1:
        s += ','
    else:
        s += '], "links": ['

    with open('out.json', 'a') as f:
        f.write(s)

for n in range(len(files)):
    topic_prob = doc_topic[n]

    for o in range(len(files)):
        topic2_prob = doc_topic[o]
        #get probability value
        value = 0
        for i in range(len(topic2_prob)):
            value += topic2_prob[i]*topic_prob[i]

        s = '{{ "source" : {}, "target": {}, "value": {} }}'.format(n, o, value)

        if o == len(files)-1 and n == len(files)-1:
            s += '] }'
        else:
            s += ','

        with open('out.json', 'a') as f:
            f.write(s)

import rpy2.robjects as robjects
r=robjects.r
prob_threshold = 0.25
#open R connection
r.source("graph-processing.R")
r('createGraph('+str(prob_threshold)+')') #create HTML file 'network.html'
