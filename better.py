filename = "./trick/output.csv"

data = dict()

with open(filename, 'r') as lines:
	for line in lines:
		values = line.split(",")
		
		graph = values[0]
		strategy = values[1]
		trick = values[8]
		optimal_without_ic = values[9]
		optimal_with_ic = values[13]
		
		print trick, optimal_without_ic, optimal_with_ic
		
		if strategy == "slf":
			optimal = int(optimal_without_ic)
		else:
			optimal = min(int(optimal_without_ic), int(optimal_with_ic))
		
		if not graph in data:
			data[graph] = [[], [], [], [], []]
		
		optimal = int(optimal)
		trick = int(trick)
		
		if strategy != "sf":
			data[graph][4].append(optimal)
			data[graph][3].append(trick)
			
			if trick == -1:
				data[graph][2].append(strategy)
			elif optimal > trick:
				data[graph][1].append(strategy)
			else:
				data[graph][0].append(strategy)
		

with open('better.csv', 'w') as output:
	for key in data.keys():
		output.write(str.format("{0}\t{4}\t{1}\t{5}\t{2}\t{3}\n", key, ', '.join(data[key][0]), ', '.join(data[key][1]), ', '.join(data[key][2]), min(data[key][3]),  min(data[key][4])))