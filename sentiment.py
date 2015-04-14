from __future__ import print_function
import semantria
import uuid
import time



# Global support
serializer = semantria.JsonSerializer()
session = semantria.Session("0346ac1a-a224-4c2c-95b7-0d1eba990bdd", "d2a68640-215c-4957-908b-e55a86a4520b", serializer, use_compression=True)




def fetcher():
	i_content = []
	with open("reviews") as f:
		i_content = f.readlines()
	tot = ""
	for line in i_content:
		tot += line
	content = tot.split("||||||||")
	ret = []
	for line in content:
		line = line.strip()
		line = line.split("====>>>>")
		if len(line)==2:
			ret.append(line)
	return ret

def writer(score,rid):
	with open("scores","a") as f:
		f.write(rid+" "+str(score)+"\n")


def sentiment(reviews):
	for rid in reviews:
		doc = {"id": rid, "text": reviews[rid]}
		status = session.queueDocument(doc)
		if status == 202:
			print("\"", doc["id"], "\" document queued successfully.", "\r\n")
	length = len(reviews)
	results = []
	while len(results) < length:
		print("Retrieving your processed results...", "\r\n")
		# time.sleep(2)
		# get processed documents
		status = session.getProcessedDocuments()
		results.extend(status)
		for data in status:
			print("Document ", data["id"], "\n", "Text => ",reviews[data["id"]], " Sentiment score: ", data["sentiment_score"], "\n")
			# executer("update review set sentiment_score = {0} where rid = {1}".format(data["sentiment_score"],data["id"]))
			writer(data["sentiment_score"],data["id"])

def main():
	results = fetcher()
	reviews = {}
	for result in results:
		print("doing",result)
		reviews[str(result[0])] = result[1]
	sentiment(reviews)


main()

# for text in initialTexts:
#    doc = {"id": str(uuid.uuid4()).replace("-", ""), "text": text}
#    status = session.queueDocument(doc)
#    if status == 202:
#      print("\"", doc["id"], "\" document queued successfully.", "\r\n")


# length = len(initialTexts)
# results = []

# while len(results) < length:
#    print("Retrieving your processed results...", "\r\n")
#    time.sleep(2)
#    # get processed documents
#    status = session.getProcessedDocuments()
#    results.extend(status)


# for data in results:
#    # print document sentiment score
#    print("Document ", data["id"], " Sentiment score: ", data["sentiment_score"], "\r\n")

#    # print document themes
#    if "themes" in data:
#       print("Document themes:", "\r\n")
#       for theme in data["themes"]:
#          print("     ", theme["title"], " (sentiment: ", theme["sentiment_score"], ")", "\r\n")

#    # print document entities
#    if "entities" in data:
#       print("Entities:", "\r\n")
#       for entity in data["entities"]:
#          print("\t", entity["title"], " : ", entity["entity_type"]," (sentiment: ", entity["sentiment_score"], ")", "\r\n")

