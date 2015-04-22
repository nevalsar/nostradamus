import ast
import requests
import solr
import re
import MySQLdb as mdb
import json

output = []
outputdict = {}

def getResult(query):
    query.strip()
    paramx = {"q":"+*BoschProductDetail.aspx* " + query, "rows":500, "fl":"id score", "wt":"python", "defType":"edismax", "qf":"id title^3 content^0.5"}
    r = requests.get("http://10.139.243.107:8983/solr/collection1/select", params = paramx)
    return ast.literal_eval(r.text) 

db = mdb.connect('10.5.18.67','12CS30026','dual12','12CS30026')
cursor = db.cursor()

s = solr.SolrConnection('http://10.139.243.107:8983/solr')

def main():
    query = raw_input()
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
                desc = row[4]
                category = row[5]
                solr_score = hit['score']
                avg_score = 0.7 * solr_score + 0.3 * avg_senti

                output.append({'pid': pid, 'name': pname, 'description': desc, 'category': category, 'solr_score': solr_score, 'avg_sentiment_score': avg_senti, 'avg_score': avg_score})
            
    # print output
    outputdict['results'] = output
    print json.dumps(outputdict)
    # print JSONEncoder().encode(output)
    return
    
if __name__=='__main__':
    main()
    # print getResult("router")