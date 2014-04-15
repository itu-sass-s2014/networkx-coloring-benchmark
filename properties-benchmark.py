import networkx as nx
import sys
import re
import os
import glob
import time
import argparse

parser = argparse.ArgumentParser(description='Run benchmark on networkx graph coloring algorithms')
parser.add_argument('--output', default="./properties", required=False, help="choose which folder to output .csv file to")

args = parser.parse_args()

strategies = ['lf', 'rs', 'sf', 'sl', 'gis', 'cs-bfs', 'cs-dfs', 'slf']

# nanoseconds: 1000000000
# microseconds: 1000000
# milliseconds: 1000

current_milli_time = lambda: int(round(time.time() * 1000))

def benchmark(output, graph, graphname, strategy, interchange):
	times = []
	
	for i in range(0, 5):
		start_time = current_milli_time()
		result = nx.coloring(graph, strategy=strategy, interchange=interchange, returntype='sets')
		times.append(current_milli_time() - start_time)
		
	avg = sum(times) / len(times)
	opt = len(result)
	
	output.write(str.format("{0},{1},{2},{3},{4},{5},{6}\n", graphname, graph.number_of_nodes(), graph.number_of_edges(), strategy, interchange, opt, avg))
	
def helper(output, graph, graphname):
	for strategy in strategies:
		benchmark(output, graph, graphname, strategy, False)
		benchmark(output, graph, graphname, strategy, True)

if not os.path.exists(args.output):
    os.makedirs(args.output)

with open(args.output + '/output.csv', 'w') as output:
	helper(output, nx.cycle_graph(100), "cycle")
	helper(output, nx.complete_graph(100), "complete")