#!/Users/arkanath/anaconda/bin/python

import cgi, cgitb 
import json
import copy
import ast
import requests
import solr
import re
import MySQLdb as mdb
import json
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

cgitb.enable()
# form = cgi.FieldStorage()

commonwords = stopwords.words('english')
commonwords.append('.')

def tokenizeandexcludecommon(text):
    # print commonword
    l = word_tokenize(text.lower())
    l3 = ['*'+x+'*' for x in l if x not in commonwords]
    return ' '.join(l3)

output = []
outputdict = {}

def getResult(query):
    query.strip()
    # print 'Query is:',tokenizeandexcludecommon(query)
    paramx = {"q":"+*BoschProductDetail.aspx* " + tokenizeandexcludecommon(query), "rows":500, "fl":"id score", "wt":"python", "defType":"edismax", "qf":"id title^60 content^2"}
    # print paramx
    r = requests.get("http://10.139.243.107:8983/solr/collection1/select", params = paramx)
    return ast.literal_eval(r.text)

db = mdb.connect('10.5.18.67','12CS30026','dual12','12CS30026')
cursor = db.cursor()

s = solr.SolrConnection('http://10.139.243.107:8983/solr')

def main(query):
    # query = 'best router in the world'
    response = getResult(query)
    for hit in response['response']['docs']:
        avg_senti = 0
        # print hit['id']
        m = re.findall(r'http://www.boschtools.com/Products/Tools/Pages/BoschProductDetail.aspx\?pid=([^\'" >]+)', hit['id'])
        if len(m) == 1:
            # print hit['score'], m[0]
            sql = "SELECT avg(sentiment_score) FROM Review GROUP BY pid HAVING pid = '" + m[0] + "'"
            cursor.execute(sql)
            if cursor.rowcount:
                avg_senti = cursor.fetchone()[0]
                # print "avg_sentiment_score: ", avg_senti

            sql = "SELECT * FROM Product WHERE pid = '" + m[0] + "'"
            cursor.execute(sql)
            if cursor.rowcount:
                row = cursor.fetchone()
                pid = m[0]
                pname = row[1]
                desc = unicode(row[4], 'utf-8')
                category = row[5]
                solr_score = hit['score']
                # print desc
                try:
                    avg_score = 0.7 * solr_score + 0.3 * avg_senti
                except:
                    avg_score = 0.7 * solr_score
                try:
                    output.append({'pid': pid, 'name': pname, 'description': desc, 'category': category, 'solr_score': solr_score, 'avg_sentiment_score': avg_senti, 'avg_score': avg_score})
                except:
                    # print desc
                    pass

#     # print output
#     outputdict['results'] = output
#     # print JSONEncoder().encode(output)
#     return outputdict

# print "Content-type: application/javascript\r\n"
print "Content-type: application/javascript\r\n"
# query = form.getvalue('query')
query = 'aweg'
response={}
response['ii'] = 'awef'
results = []
response['results'] = results
result1 = {}
result1['pid'] = 'API-FD'
result1['name'] = query
result1['description'] = query
result1['category'] = query
result1['score'] = 4.5
result1['avg_sentiment_score'] = 4.8
result1['avg_score'] = 4.7
results.append(result1)
result2 = copy.copy(result1)
result2['category'] = 'ewagweag'
results.append(result2)
print('functionName('+json.dumps(main(query))+');')
# print('functionName('+json.dumps(response)+');')
# print(json.dumps(response))