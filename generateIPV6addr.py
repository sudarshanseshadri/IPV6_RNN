import argparse
import random 

start_prefix = "20010db885a3000000008a2e0370"
curr_suffix = 0
addresses = []
delimiter = ';'

parser = argparse.ArgumentParser(description='Input arguments for generating input addresses to Character RNN')
parser.add_argument('outputFile', nargs='?', default='IPV6Addresses.txt', type=str)
parser.add_argument('dropProb', nargs='?', default=0.0, type=float)
parser.add_argument('numAddr', nargs='?', default=1024, type=int)
parser.add_argument('numPatt', nargs='?', default=1, type=int)
args = parser.parse_args()


if args.numPatt == 1:
	### simply increments the address by 1
	for _ in range(args.numAddr):
		if random.random() > args.dropProb: addresses.append(start_prefix + "%0.4x" % curr_suffix + delimiter)
		curr_suffix += 1

elif args.numPatt == 2:
	for _ in range(args.numAddr / 2):
		if random.random() > args.dropProb: addresses.append(start_prefix + "%0.4x" % curr_suffix + delimiter)
		curr_suffix += 1
	for _ in range(args.numAddr / 2):
		if random.random() > args.dropProb: addresses.append(start_prefix + "%0.4x" % curr_suffix + delimiter)
		curr_suffix += 2

with open(args.outputFile, 'w') as f:
	f.write(''.join(addresses))
