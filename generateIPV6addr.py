output_file = 'IPV6Addresses.txt'
num_addr = 256
start_prefix = "20010db885a3000000008a2e0370"
curr_suffix = 0
addresses = []

delimiter = ';'
### simply increments the address by 1
for _ in range(num_addr):
	addresses.append(start_prefix + "%0.4x" % curr_suffix + delimiter)
	curr_suffix += 1

with open(output_file, 'w') as f:
	f.write(''.join(addresses))
