import numpy
from pymongo import MongoClient

global db
db = MongoClient().db.links
if not db:
	print('Connected to DB')

items = db.find({})

size = len(items)
prematrix = [[]] * size
for i in range(size):
	prematrix[i]= [1/len(item.refs) for j in range(size) if (items[j].url in item.refs) else 0]

print("Prematrix array:\n" +'\n'.join(prematrix))
matrix = numpy.matrix(prematrix)



