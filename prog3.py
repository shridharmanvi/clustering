import re
import sys
reload(sys)
import math as m
import random

from nltk.stem import PorterStemmer

sys.setdefaultencoding("utf-8")
wordfreq=[]
d_count=2000

#---------------------------------DATA Import-------------------------------------
#Import files 
job=open('/Users/shridharmanvi/Desktop/Projects/dm3/data/jobstry.tsv','rw')

jobs={}

for row in job.readlines():
    row= row.split('\t')
    try:
        row[0]=int(row[0])
        jobs[int(row[0])]=row
    except ValueError:
        x=1

print len(jobs.keys())


#---------------------------------DATA CLEANSING-------------------------------------
#1.Stopword removal
#2.Word stemming

tags=re.compile(r'<[^>]+>')#<tags>
backslash=re.compile(r'\\\w')
utfremove=re.compile(r'[^\x00-\x7F]+')
periodremove=re.compile(r'[\.|\$|\!|\@|\#|\$|\(|\)|\\|\/|\-|\_|\[|\]|\{|\}|\&nbsp;]')
digitsremove=re.compile(r'[0-9]')
stemmer = PorterStemmer()

stop=['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your',
      'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her',
      'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
      'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was',
      'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing',
      'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at',
      'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before',
      'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over',
      'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how',
      'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
      'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don',
      'should', 'now']



#the following loop removes html tags and stop words from 'Description' attribute from the data
for k in jobs.keys():
    rep=jobs[k][1] + ' ' + str(jobs[k][2])
    rep=tags.sub(' ',rep).lower()
    rep=backslash.sub(' ',rep)
    rep=utfremove.sub(' ',rep)
    rep=periodremove.sub('',rep)
    rep=digitsremove.sub('',rep)
    rep = ' '.join([word for word in rep.split() if word not in stop]) #and ord(word)<128])
    rep = [stemmer.stem(word) for word in rep.split()]
    jobs[k][1]= rep


#print jobs[393096][1]

#The below loop constructs the bag of words for every single job description
bag={}

for k in jobs.keys():
    sample= jobs[k][1]
    d={}
    for word in sample:
        try:
            d[word]=1+(m.log(sample.count(word)))
        except KeyError:
            x=1
        bag[k]=d
            



#building tf-idf dictionary
def buildndf():
    #D= document count
    distinct_words={}

    for k in bag.keys():
        words=bag[k]
        assign={}
        for wo in words.keys():
            assign[wo]=1
        distinct_words[k]=assign
        
        
    for k in distinct_words.keys():
        document=distinct_words[k]
        li=document.keys()
        wordfreq.extend(li)
    
buildndf()

final={}

#below loop calculates the idf of every unique word in the dataset. Multiply this value with bag[key][word]
for k in bag.keys():
    words=bag[k]
    for w1 in words.keys():
        if(w1 not in final.keys()):
            x=m.log(d_count/wordfreq.count(w1))
            final[w1]=x

            
clusters={}
final_clusters={}

#choose random clusters
for k in range(3):
    x=random.choice(bag.keys())
    clusters[k]=bag[x]



#k-means clustering
for k in bag.keys():
    bag_words=bag[k]
    for c in clusters.keys():
        cluster_words=clusters[c]
        d=0
        for ck in cluster_words.keys():
            try:
                d=(bag_words[ck]*final[ck])
                d=d*d
            except KeyError:w=1
        if (c==0):d1=d
        elif(c==1):d2=d
        elif(c==2):d3=d
    score_list=[d1,d2,d3]
    max_score_index=score_list.index(max(score_list))
    final_clusters[k]=max_score_index           

"""
def recompute_centroid():
    count0=0
    count1=0
    count2=0
    for w in final_clusters.keys():
        if(final_clusters[wo]==0):
            count0+=1
        elif(final_clusters[wo]==1):
            count1+=1
        elif(final_clusters[wo]==2):
            count2+=1
            
    for wo in final_clusters.keys():
        zero=clusters[0]
        one=clusters[1]
        two=clusters[2]
        if(final_clusters[wo]==0):
            for w in bag[wo].keys():
                try:
                    zero[w]+=bag[wo][w]
                except KeyError:
                    try:
                        zero[w]=bag[wo][w]
                    except KeyError:
                        zero[w]=0
        elif(final_clusters[wo]==1):
            for w in bag[wo].keys():
                try:
                    one[w]+=bag[wo][w]
                except KeyError:
                    try:
                        one[w]=bag[wo][w]
                    except KeyError:
                        one[w]=0
        elif(final_clusters[wo]==2):
            for w in bag[wo].keys():
                try:
                    two[w]+=bag[wo][w]
                except KeyError:
                    try:
                        two[w]=bag[wo][w]
                    except KeyError:
                        two[w]=0        
    zero=([word for word in rep.split() if word not in stop])
        
"""
print final_clusters
