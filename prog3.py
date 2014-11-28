import re
from nltk.corpus import stopwords #download nltk module by running the command 'sudo pip install -U nltk'
#Import files 
job=open('jobs.tsv','rw')

#cachedStopWords = stopwords.words('english') #caching stop words to speeden the process of removing stop words

jobs={}

for row in job.readlines():
    row= row.split('\t')
    try:
        row[0]=int(row[0])
        jobs[int(row[0])]=row
    except ValueError:
        x=1

tags=re.compile(r'<[^>]+>')#<tags>
backslash=re.compile(r'\\\w')

for k in jobs.keys():
    rep=jobs[k][1]
    rep=tags.sub(' ',rep)
    rep=backslash.sub(' ',rep)
    rep = ' '.join([word for word in rep.split() if word not in stopwords.words("english")])
    jobs[k][1]= rep
    

print jobs[965577][1]
print len(jobs.keys())