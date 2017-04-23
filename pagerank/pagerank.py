import numpy
from pymongo import MongoClient
from pprint import pprint

global db
db = MongoClient().db.links
if not db:
	pprint('Connected to DB')

cursor = db.find()
items = []
for item in cursor:
	items.append(item)


size = len(items)
print("We have " + str(size) + " items to handle")

prematrix = [[]] * size
for i in range(size):
	print(i)
	prematrix[i]= [1/len(items[i]['refs']) if (items[j]['url'] in items[i]['refs']) else 0 for j in range(size) ]

matrix = numpy.matrix(prematrix)



