data = open('all_requested_data').readlines()

data.sort()

for line in data:
	print(line)