## data conversion of real-time CSV data to JSON data
##
##csv should be node1,node2,time
##want a list of graphs (easy) and links (not easy) 
import json
import csv
import sys, getopt
node_list = []
edge_list = []

def find(lst, key, value):
	"""Input: list of dics, a possible key and value for a given dic. Output: index #"""
	for i, dic in enumerate(lst):
		if dic[key] == value:
			return i
	return -1

	
def find_two(lst, key, value):
	"""Input: list of dics, two keys and two values for a given dic to match on."""
	for i, dic in enumerate(lst):
		if dic[key[0]] == value[0] and dic[key[1]] == value[1]:
			return i
	return -1


def add_to_node_list(id_number):
	index = find(node_list,"id",id_number)
	if index >= 0:
		node_list[index]['weight'] += 1
	else:
		node_list.append({'id':id_number,'weight':1})

def add_to_edge_list(row):
	index = find_two(edge_list,key = ["id1","id2"], value = row[0:2])
	if index >= 0:
		edge_list[index]['timestamps'].append(row[2])
	else:
		edge_list.append({'id1':row[0],'id2':row[1],'timestamps':[row[2]]})


def main(argv):
	inputfile = ''
	outputfile = ''
	number_to_parse = 0
	print argv
	try:
		opts, args = getopt.getopt(argv,"hn:i:",["ifile=","ofile="])
	except getopt.GetoptError:
		print 'error: test.py -i <inputfile> -n <number_to_parse>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'test.py -i <inputfile> -n <number_to_parse>'
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-n", "--ofile"):
			number_to_parse = arg
	print 'Input file is "', inputfile
	print 'number is "', number_to_parse
	## Go through the list of interactions and add them to our edges and graph files ##
	with open(inputfile, 'rb') as f:
		reader = csv.reader(f)
		i = 0 #just to say hi
		for row in reader:
			i += 1
			 #just to track the progress
			if i % 1000 == 0:
				print i
			if i == number_to_parse:
				print("parsing complete")
				break
			#increase the weight of both the first and 2nd ids. 
			add_to_node_list(row[0])
			add_to_node_list(row[1])
			add_to_edge_list(row)
	##Now we print the results to two files##
	with open('result_edges.json','w') as f_edges:
		f_edges.write(json.dumps(edge_list))
	with open('result_nodes.json','w') as f_nodes:
		f_nodes.write(json.dumps(node_list))
	print("completed")
	

if __name__ == "__main__":
   main(sys.argv[1:])