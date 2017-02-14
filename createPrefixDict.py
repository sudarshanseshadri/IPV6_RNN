import sys, csv, pickle

inputFileName = sys.argv[1]
prefixDict = {}
with open(inputFileName, 'rb') as csvFile:
	addresses = csv.reader(csvFile, delimiter=',')
	for row in addresses:
		if row[0] in prefixDict:
			prefixDict[row[0]].append(row[1])
		else:
			prefixDict[row[0]] = [row[1]]

pickle.dump(prefixDict, open('prefixDict_'+inputFileName, 'wb'))