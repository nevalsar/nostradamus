import MySQLdb as db
import json
import requests
import solr

s = solr.SolrConnection('http://10.139.243.107:8983/solr')

def main():
    response = s.query('id:*BoschProductDetail.aspx?pid=*', rows=2)
#     print response.len
    for hit in response.results:
        pid =  hit['id'].split('=')[1]
        details = get_details(pid)
        details['category'] = getCategory(details['category'])
      	insertProduct(details)
    return

def getCategory(catid):
	response = s.query('id:*catid='+ str(catid)+'*', rows=1)
#     print response.len
	for hit in response.results:
		category =  hit['title'].split('|')[0]
	return category
    
def insertReview(review):
	con = db.connect('10.5.18.67','12CS30026','dual12','12CS30026');

	with con:
	    cur = con.cursor()
	    query = "INSERT INTO Review(pid,title, text, rating, nick, date, sentiment_score) VALUES("\
	    		+ "'" + review['pid']	+ "', "\
	    		+ "'" + review['title'] 		+ "', "\
	    		+ "'" + review['text'] 		+ "', "\
	    		+ "'" + review['rating'] 	+ "', "\
	    		+ "'" + review['nick'] 		+ "'"\
	    		+ "'" + review['date'] 		+ "'"\
	    		+ "'" + review['sentiment_score'] 		+ "'"\
	    		+ ")";\
		print query
	    cur.execute(query)
	return

def insertProduct(product):
	con = db.connect('10.5.18.67', '12CS30026','dual12','12CS30026');

	with con:
	    cur = con.cursor()
	    query = "INSERT INTO Product(pid,pname ,plink ,rating ,description ,category) VALUES("\
	    		+ "'" + product['pid'] 			+ "', "\
	    		+ "'" + product['pname'] 		+ "', "\
	    		+ "'" + product['plink'] 		+ "', "\
	    		+ "'" + product['rating'] 	+ "', "\
	    		+ "'" + product['description'] 		+ "'"\
	    		+ "'" + product['category'] 		+ "'"\
	    		+ ")";\
		print query
	    cur.execute(query)

	for review in product['reviews']:
		insertReview(review)
	return


if __name__=='__main__':
    main()