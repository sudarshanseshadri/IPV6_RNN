import argparse
import random 

#start_prefix = "20010db885a3000000008a2e0370"
currSuffix = 0
addresses = []
delimiter = ';'

parser = argparse.ArgumentParser(description='Input arguments for generating input addresses to Character RNN')
parser.add_argument('outputFile', nargs='?', default='IPV6Addresses.txt', type=str)
parser.add_argument('dropProb', nargs='?', default=0.0, type=float)
parser.add_argument('numAddr', nargs='?', default=1024, type=int)
parser.add_argument('numPatt', nargs='?', default=1, type=int)
parser.add_argument('addrLen', nargs='?', default=4, type=int)
parser.add_argument('startPrefix', nargs='?', default='', type=str)
args = parser.parse_args()

def nextSuffix(currSuffix, incrBy=1):
	return currSuffix+incrBy

if args.numPatt == 1:
	### simply increments the address by 1
	for _ in range(args.numAddr):
		if random.random() > args.dropProb: addresses.append(args.startPrefix + ('%0.{}x'.format(args.addrLen - len(args.startPrefix)) % currSuffix) + delimiter)
		currSuffix = nextSuffix(currSuffix)

elif args.numPatt == 2:
	for _ in range(args.numAddr/3*2):
		if random.random() > args.dropProb: addresses.append(args.startPrefix + ('%0.{}x'.format(args.addrLen - len(args.startPrefix)) % currSuffix) + delimiter)
		currSuffix = nextSuffix(currSuffix, 1)
	for _ in range(args.numAddr/3):
		if random.random() > args.dropProb: addresses.append(args.startPrefix + ('%0.{}x'.format(args.addrLen - len(args.startPrefix)) % currSuffix) + delimiter)
		currSuffix = nextSuffix(currSuffix, 2)
with open(args.outputFile, 'w') as f:
	f.write(''.join(addresses))
