import urlparse
import requests 
import lxml.html 
import urllib
from joblib import Parallel, delayed
# def parse_page(reponse):
# 	hxs = HtmlXPathSelector(response)
# 	content = hxs.select('//*[@id="imagecontainer"]')
# 	for res in content:
# 		#item ["Image"]= map(unicode.strip, res.select('//div[@class="pro_detail_tit"]//div[@class="pro_titre"]/h1/text()').extract())
# 		item['image_urls'] = map(lambda src: urlparse.urljoin(response.url, src), res.select('./img/@src').extract())
# 		items.append(item)
# 	return items

# def main():
# 	response = requests.get("http://www.boschtools.com/Products/Tools/Pages/BoschProductDetail.aspx?pid=3931B-SPB")
# 	print parse_page(response)


# dicto = {}

def func(pid):
	global dicto
	print "crawling "+pid+" ..."
	try:
		hxs = lxml.html.document_fromstring(requests.get("http://www.boschtools.com/Products/Tools/Pages/BoschProductDetail.aspx?pid="+pid).content)
		arr = hxs.xpath('//*[@id="imagecontainter"]/img/@src')
		# dicto[pid] = arr[0]
		with open("srcs","a") as f:
			f.write(pid+"===>>>"+arr[0]+"\n")
	except:
		pass
	print "crawled "+pid+" ==> ",arr[0]
	# urllib.urlretrieve(arr[0], "./pics/"+pid+".png")
# func("3931B-SPB")

def main():
	with open("pid.txt") as f:
		lines = f.readlines()
	for line in lines:
		func(line.strip())
	# Parallel(n_jobs=-1)( delayed(func)(line.strip()) for line in lines )
	# with open("srcs","w") as f:
	# 	for key in dicto:
	# 		f.write(key+"===>>>"+dicto[key])

main()