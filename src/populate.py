import MySQLdb as db
import json
import requests
import solr
import crawl

s = solr.SolrConnection('http://10.139.243.107:8983/solr')

def main():
    response = s.query('id:*BoschProductDetail.aspx?pid=*', rows=300)
#     print response.len
    pid = []
    count  =0
    jjj = 0
    for hit in response.results:
        con = db.connect('10.5.18.67','12CS30026','dual12','12CS30026');
        cur = con.cursor()
        query = "select * from Product where pid = '"+hit['id'].split('=')[1]+"'"
        cur.execute(query)
        res = cur.fetchall()
        if(len(res)>0):
            print 'Already there,continuing,',hit['id'].split('=')[1]
            continue
        pid = []
        pid.append(hit['id'].split('=')[1])
        print pid
        details=crawl.getpidinfo(pid)
        if len(details) == 0:
            count += 1
            continue
        jjj += 1
        details = details[0]
        # details['category'] = getCategory(details['category'])
        insertProduct(details)
        # pid = []
        # pid.append(hit['id'].split('=')[1])

        # print pid
        # details=crawl.getpidinfo(pid)
    print count,jjj
    return

def getCategory(catid):
    response = s.query('id:*catid='+ str(catid)+'*', rows=1)
#     print response.len
    for hit in response.results:
        category =  hit['title'].split('|')[0]
        print category
        return category

def insertReview(review):
    con = db.connect('10.5.18.67','12CS30026','dual12','12CS30026');

    for key in review:
        if review[key] is None:
            review[key] = 'Unknown'


    with con:
        cur = con.cursor()
        query = "INSERT INTO Review(pid,title, text, nick, date, sentiment_score) VALUES("\
                + '"' + review['pid'].replace('"',"&quot;").encode('ascii', 'ignore')    + '", '\
                + '"' + review['title'].replace('"',"&quot;").encode('ascii', 'ignore')         + '", '\
                + '"' + review['text'].replace('"',"&quot;").encode('ascii', 'ignore')         + '", '\
                + '"' + review['nick'].replace('"',"&quot;").encode('ascii', 'ignore')         + '", '\
                + '"' + review['date'].replace('"',"&quot;").encode('ascii', 'ignore')         + '", '\
                + " NULL "\
                + ")";\
        print query
        cur.execute(query)
    return

def insertProduct(product):
    con = db.connect('10.5.18.67', '12CS30026','dual12','12CS30026');


    for key in product:
        if product[key] is None:
            product[key] = 'Unknown'

    with con:
        cur = con.cursor()
        query = "INSERT INTO Product(pid,pname ,plink ,rating ,description ,category) VALUES("\
                +'"'+ product['pid'].replace('"',"&quot;").encode('ascii', 'ignore')           + '", '\
                +'"'+ product['pname'].replace('"',"&quot;").encode('ascii', 'ignore')             + '", '\
                +'"'+ product['plink'].replace('"',"&quot;").encode('ascii', 'ignore')             + '", '\
                +'"'+ product['rating'].replace('"',"&quot;").encode('ascii', 'ignore')         + '", '\
                +'"'+ product['description'].replace('"',"&quot;").encode('ascii', 'ignore') + '", '\
                +'"'+ product['category'].replace('"',"&quot;").encode('ascii', 'ignore')         + '"'\
                + ")";\
        print query
        cur.execute(query)

    for review in product['reviews']:
        insertReview(review)
    return


if __name__=='__main__':
    main()