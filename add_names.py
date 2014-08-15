import json
names = open("names.txt").read().split('\n')
data = json.loads(open("result_nodes.json",'r').read())