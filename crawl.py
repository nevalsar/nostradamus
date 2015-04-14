__author__ = 'arkanath'
import requests
import re
import xml.etree.ElementTree as ET


def getpidinfo(pid):
    inp = ','.join(pid)
    # print inp
    products = []
    mppid = {}
    for prod in pid:
        product = {}
        product['pid'] = prod
        product['pname'] = prod
        mppid[product['pid']] = product
        product['plink'] = "http://www.boschtools.com/Products/Tools/Pages/BoschProductDetail.aspx?pid="+prod
        r = requests.get(product['plink'])
        if(r.status_code!=200):
            print 'Load in 1st:',r.reason
        # print r.text
        m = re.findall(r'product_name:\["(.*)"\], product_sku', r.text)
        if(len(m)>0):
            product['description'] = m[0].replace('\\"','&quot;')
        else:
            print 'No Description Found for',prod
            product['description'] = 'Unknown'
        # print m

        m = re.findall(r'product_category:\["(.*)"\], product_id', r.text)
        if(len(m)>0):
            product['category'] = m[0].replace('\\"','&quot;')
        else:
            print 'No Category Found for pid',prod
            product['category'] = 'Unknown'

        product['rating'] = '-1'
        product['reviews'] = []
        products.append(product)

    r = requests.get("http://boschtools.ugc.bazaarvoice.com/data/reviews.xml", params={'apiversion': '5.4', 'passKey': 'hse2uvr3q27287ht1ou694cat', 'include': 'products','stats':'reviews','Filter':'ProductId:'+inp})
    if(r.status_code!=200):
        print 'Load in 2nd:',r.reason

    root = ET.fromstring(r.text.encode('ascii', 'ignore'))

    ns = "{http://www.bazaarvoice.com/xs/DataApiQuery/5.4}"

    for prod in root.iter(ns+'Product'):
        product = mppid[prod.attrib['id']]
        if(len(prod.findall('.//'+ns+'AverageOverallRating'))>0):
            product['rating'] = prod.findall('.//'+ns+'AverageOverallRating')[0].text

    for rev in root.iter(ns+'Review'):
        review = {}
        type = rev.findall(ns+'IsRatingsOnly')[0].text
        if(type=='true'):
            continue
        review['rid'] = rev.attrib['id']
        review['pid'] = rev.findall(ns+'ProductId')[0].text
        review['title'] = rev.findall(ns+'Title')[0].text.replace('"','&quot;')
        review['text'] = rev.findall(ns+'ReviewText')[0].text.replace('"','&quot;')
        try:
            review['nick'] = rev.findall(ns+'UserNickname')[0].text
        except:
            review['nick'] = 'Unknown'
            pass
        review['date'] = rev.findall(ns+'SubmissionTime')[0].text[:10]
        mppid[review['pid']]['reviews'].append(review)
        # print 'New Review:',review
    #
    return products

# x =  getpidinfo(['VAC120BN','AG40-11P'])
# for z in x:
#     print z