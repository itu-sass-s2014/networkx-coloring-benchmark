import networkx as nx
import sys
import re
import glob
import time
import argparse

parser = argparse.ArgumentParser(description='Run benchmark on networkx graph coloring algorithms')
parser.add_argument('--folder', default=".", required=True, help="choose which folder to point to with .col files")
parser.add_argument('--output', default=".", required=False, help="choose which folder to output .csv file to")

args = parser.parse_args()

# nanoseconds: 1000000000
# microseconds: 1000000
# milliseconds: 1000

current_milli_time = lambda: int(round(time.time() * 1000))

def getGraphFromFile(filename):
	G = nx.Graph()
	
	with open(filename, 'r') as lines:
		for line in lines:
			result = re.search("^e.([0-9]+).([0-9]+)", line)

			if result:
				v1 = int(result.groups()[0])
				v2 = int(result.groups()[1])

				G.add_edge(v1, v2)

	return G

information = dict()

try:
	with open(args.folder + '/information.csv', 'r') as lines:
		for line in lines:
			parts = line.replace('\n', '').split(',')
			information[parts[0]] = parts
except IOError as e:
    print "running without supplementary information.csv file"

with open(args.output + '/output.csv', 'w') as output:
	for filename in glob.glob(args.folder + '/*.col'):
		key = filename.split('/').pop()
		print key
		G = getGraphFromFile(filename)

		strategies = ['lf', 'rs', 'sf', 'sl', 'gis', 'cs-bfs', 'cs-dfs', 'slf']

		for strategy in strategies:
			times = []
			times_ic = []

			print key, strategy

			for i in range(0, 5):
				start_time = current_milli_time()
				result = nx.coloring(G, strategy=strategy, interchange=False, returntype='sets')
				times.append(current_milli_time() - start_time)

			print key, strategy, "interchange"

			for i in range(0, 5):
				start_time = current_milli_time()
				result_ic = nx.coloring(G, strategy=strategy, interchange=True, returntype='sets')
				times_ic.append(current_milli_time() - start_time)

			average_time = sum(times) / len(times)
			average_time_ic = sum(times_ic) / len(times_ic)

			result_optimal = len(result)
			result_optimal_ic = len(result_ic)
			result_nodes = G.number_of_nodes()
			result_edges = G.number_of_edges()

			if key in information:
				info = information[key]
				if info[3] == '?':
					info[3] = -1
				
				instance_optimal = int(info[3])
				instance_nodes = info[1]
				instance_edges = info[2]

				diff_percent = 100 * (result_optimal - instance_optimal) / instance_optimal
				diff_number = result_optimal - instance_optimal
				diff_percent_ic = 100 * (result_optimal_ic - instance_optimal) / instance_optimal
				diff_number_ic = result_optimal_ic - instance_optimal
			else:
				instance_optimal = -1
				instance_nodes = -1
				instance_edges = -1

				diff_percent = -1
				diff_number = -1
				diff_percent_ic = -1
				diff_number_ic = -1
			
			output.write(str.format("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16}\n", key, strategy, instance_nodes, result_nodes, int(instance_nodes)==result_nodes, instance_edges, result_edges, int(instance_edges)==result_edges, instance_optimal, result_optimal, diff_number, diff_percent, average_time, result_optimal_ic, diff_number_ic, diff_percent_ic, average_time_ic))
			
			# print key, strategy, info[1], '==', G.number_of_nodes(), ',', info[2], '==', G.number_of_edges(), ',', info[3], '==', len(result), diffNumber, diffPercent
