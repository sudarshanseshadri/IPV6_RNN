import argparse

parser = argparse.ArgumentParser(description='Input arguments for generating input addresses to Character RNN')
parser.add_argument('inputFile', nargs='?', type=str)
parser.add_argument('functionName', nargs='?', default='increment', type=str)
parser.add_argument('delimeter', nargs='?', default=';', type=str)

args = parser.parse_args()

def increment(addr):
	return addr+1

def skipOne(addr):
	return addr+2

functionDict = {
	'increment': increment,
	'skipOne' : skipOne
}

funcToUse = functionDict[args.functionName]

with open(args.inputFile, 'r') as f:
	addrs = [int(addr, 16) for addr in f.read().split(args.delimeter)]

numCorrect = 0
numTotal = len(addrs)-1
for i in xrange(numTotal):
	if addrs[i+1] == funcToUse(addrs[i]):
		numCorrect += 1

print "Testing {} with function {}: {} correct out of {} total ({} percent)".format(args.inputFile, args.functionName, numCorrect, numTotal, float(numCorrect)/numTotal)


