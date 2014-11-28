import re
import sys
reload(sys)

from nltk.corpus import stopwords #download nltk module by running the command 'sudo pip install -U nltk'
from nltk.stem.lancaster import LancasterStemmer

sys.setdefaultencoding("utf-8")

#---------------------------------DATA Import-------------------------------------
#Import files 
job=open('/Users/shridharmanvi/Desktop/Projects/dm3/data/jobs.tsv','rw')

jobs={}

for row in job.readlines():
    row= row.split('\t')
    try:
        row[0]=int(row[0])
        jobs[int(row[0])]=row
    except ValueError:
        x=1

#---------------------------------DATA CLEANSING-------------------------------------
#1.Stopword removal
#2.Word stemming

cachedStopWords = stopwords.words('english') #caching stop words to speeden the process of removing them
tags=re.compile(r'<[^>]+>')#<tags>
backslash=re.compile(r'\\\w')
utfremove=re.compile(r'[^\x00-\x7F]+')
stemmer = LancasterStemmer()

#the following loop removes html tags and stop words from 'Description' attribute from the data
for k in jobs.keys():
    rep=jobs[k][1] + ' ' + str(jobs[k][2])
    rep=tags.sub(' ',rep)
    rep=backslash.sub(' ',rep)
    rep=utfremove.sub(' ',rep)
    rep = ' '.join([word for word in rep.split() if word not in cachedStopWords]) #and ord(word)<128])
    rep = [stemmer.stem(word) for word in rep.split()]
    jobs[k][1]= rep

#The below loop constructs the bag of words for every single job description
bag={}

for k in jobs.keys():
    sample= jobs[k][1]
    d={}
    for word in sample:
        try:
            d[word]=sample.count(word)
        except KeyError:
            x=1
        bag[k]=d
            


#print jobs[741623][1]
#print len(jobs.keys())