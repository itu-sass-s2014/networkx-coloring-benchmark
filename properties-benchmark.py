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

strategies = ['lf', 'rs', 'sl', 'gis', 'cs-bfs', 'cs-dfs', 'slf']

# nanoseconds: 1000000000
# microseconds: 1000000
# milliseconds: 1000

current_milli_time = lambda: int(round(time.time() * 1000))

def benchmark(output, graph, graphname, strategy, interchange):
	times = []
	opt = sys.maxint
	
	iteration = 5
	
	if strategy == 5:
		iteration = graph.number_of_nodes()
	
	for i in range(0, iteration):
		start_time = current_milli_time()
		opt = min(opt, len(nx.coloring(graph, strategy=strategy, interchange=interchange, returntype='sets')))
		times.append(current_milli_time() - start_time)
		
	avg = sum(times) / len(times)
	
	print graphname, strategy, interchange
	output.write(str.format("{0},{1},{2},{3},{4},{5},{6}\n", graphname, graph.number_of_nodes(), graph.number_of_edges(), strategy, interchange, opt, avg))
	
def helper(output, graph, graphname):
	for strategy in strategies:
		try:
			benchmark(output, graph, graphname, strategy, False)	
			benchmark(output, graph, graphname, strategy, True)
		except nx.exception.NetworkXPointlessConcept:
			print ""

if not os.path.exists(args.output):
    os.makedirs(args.output)

with open(args.output + '/output.csv', 'w') as output:
	helper(output, nx.balanced_tree(2, 5), "balanced_tree") # branching factor, height
	helper(output, nx.barbell_graph(50, 50), "barbell_graph")
	helper(output, nx.complete_graph(50), "complete_graph")
	helper(output, nx.complete_bipartite_graph(50, 50), "complete_bipartite_graph")
	helper(output, nx.circular_ladder_graph(50), "circular_ladder_graph")
	helper(output, nx.cycle_graph(50), "cycle_graph")
	helper(output, nx.dorogovtsev_goltsev_mendes_graph(5), "dorogovtsev_goltsev_mendes_graph")
	helper(output, nx.empty_graph(50), "empty_graph")
	helper(output, nx.grid_2d_graph(5, 20), "grid_2d_graph")
	helper(output, nx.grid_graph([2, 3]), "grid_graph")
	helper(output, nx.hypercube_graph(3), "hypercube_graph")
	helper(output, nx.ladder_graph(50), "ladder_graph")
	helper(output, nx.lollipop_graph(5, 20), "lollipop_graph")
	helper(output, nx.path_graph(50), "path_graph")
	helper(output, nx.star_graph(50), "star_graph")
	helper(output, nx.trivial_graph(), "trivial_graph")
	helper(output, nx.wheel_graph(50), "wheel_graph")
	
	helper(output, nx.random_regular_graph(1, 50, 678995), "random_regular_graph_1")
	helper(output, nx.random_regular_graph(3, 50, 683559), "random_regular_graph_3")
	helper(output, nx.random_regular_graph(5, 50, 515871), "random_regular_graph_5")
	helper(output, nx.random_regular_graph(8, 50, 243579), "random_regular_graph_8")
	helper(output, nx.random_regular_graph(13, 50, 568324), "random_regular_graph_13")
	
	
	helper(output, nx.diamond_graph(), "diamond_graph")