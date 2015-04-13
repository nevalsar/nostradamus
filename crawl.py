__author__ = 'arkanath'

import requests
import xml.etree.ElementTree as ET


def getpidinfo(pid):
    inp = ','.join(pid)
    # print inp
    r = requests.get("http://boschtools.ugc.bazaarvoice.com/data/reviews.xml", params={'apiversion': '5.4', 'passKey': 'hse2uvr3q27287ht1ou694cat', 'include': 'products','stats':'reviews','Filter':'ProductId:'+inp})
    if(r.status_code!=200):
        print 'Load:',r.reason
    root = ET.fromstring(r.text.encode('ascii', 'ignore'))
    # for child in root:
    #     print child.tag,child.text
    # print root.text
    products = []
    ns = "{http://www.bazaarvoice.com/xs/DataApiQuery/5.4}"
    # for neighbor in root.iter('Products'):
    #     print neighbor.attrib
    mppid = {}
    for prod in root.iter(ns+'Product'):
        product = {}
        product['pid'] = prod.attrib['id']
        mppid[product['pid']] = product
        product['pname'] = prod.findall(ns+'Name')[0].text
        product['category'] = prod.findall(ns+'CategoryId')[0].text
        product['description'] = prod.findall(ns+'Description')[0].text
        product['plink'] = prod.findall(ns+'ProductPageUrl')[0].text
        product['rating'] = prod.findall('.//'+ns+'AverageOverallRating')[0].text
        product['reviews'] = []
        # print 'New Product:',product
        products.append(product)
    for rev in root.iter(ns+'Review'):
        review = {}
        type = rev.findall(ns+'IsRatingsOnly')[0].text
        if(type=='true'):
            continue
        review['rid'] = rev.attrib['id']
        review['pid'] = rev.findall(ns+'ProductId')[0].text
        review['title'] = rev.findall(ns+'Title')[0].text
        review['text'] = rev.findall(ns+'ReviewText')[0].text
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

# print getpidinfo(['2605411035'])