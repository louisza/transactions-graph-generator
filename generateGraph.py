import argparse
import math
import threading
import time
import os

from generator.generateNodes import generateNodes
from generator.generateEdges import generateEdges
from generator.generateTransactions import generateTransactions
from generator.generatePatterns import generatePatterns
from generator.utils import log

### Script arguments setup ###
parser = argparse.ArgumentParser("Generate Graph")
parser.add_argument("population", help="Population count of the graph", type=int)
parser.add_argument("--data", help="path to the data folder", type=str,  action="store", default='./data')
parser.add_argument(
	"--probs",
	help="list of connection creation probabilities. Format: client-client,client-company,client-atm,company-client",
	type=str,
	action="store",
	default="0.004,0.01,0.3,0.005"
)

parser.add_argument(
	"--steps",
	help="Steps to do. possible values (comma - separated): nodes, edges, transactions, patterns",
	type=str,
	action="store",
	default="nodes,edges,transactions,patterns"
)
parser.add_argument(
	"--batch-size",
	help="Size of batch window to write",
	type=int,
	action="store",
	default=10000
)

args = parser.parse_args()
### ### ###

### Variables definition ###
dataDir = args.data + '/' + time.strftime("%H.%M.%S_%d-%m-%Y")
os.makedirs(dataDir)

files = {
	"client" : dataDir + '/nodes.clients.csv',
	"company" : dataDir + '/nodes.companies.csv',
	"atm" : dataDir + '/nodes.atms.csv',

	"clients-clients-edges": dataDir + '/edges.client-client.csv',
	"clients-companies-edges": dataDir + '/edges.client-company.csv',
	"clients-atms-edges": dataDir + '/edges.client-atm.csv',
	"companies-clients-edges": dataDir + '/edges.company-client.csv',

	"clients-sourcing-transactions": dataDir + '/nodes.transactions.client-sourcing.csv',
	"companies-sourcing-transactions": dataDir + '/nodes.transactions.company-sourcing.csv',

	"flow-pattern-transactions": dataDir + '/nodes.transactions.patterns.flow.csv',
	"circular-pattern-transactions": dataDir + '/nodes.transactions.patterns.circular.csv',
	"time-pattern-transactions": dataDir + '/nodes.transactions.patterns.time.csv'
}

statistics = {
	"company": 0.00025,
	"atm": 0.00005
}

counts = {
	"client" : args.population,
	"company" : math.ceil(statistics['company'] * args.population),
	"atm" : math.ceil(statistics['atm'] * args.population)	,
}
### ### ###

probs = list(map(lambda x : float(x), args.probs.split(',')))
steps = set(map(lambda x: x, args.steps.split(',')))
batchSize = getattr(args, 'batch_size')

log('Steps to execute: ' + str(steps))


# Nodes generation process
if 'nodes' in steps:
	log()
	log('------------##############------------')
	log('Generating nodes')
	generateNodes(files, counts, batchSize)

# Edges generation processes
if 'edges' in steps:
	log()
	log('------------##############------------')
	log('Generating edges')
	generateEdges(files, probs, batchSize)

# Transactions generation processes
if 'transactions' in steps:
	log()
	log('------------##############------------')
	log('Generating transactions')
	generateTransactions(files, batchSize)

# Inserting patterns in edges
if 'patterns' in steps:
	log()
	log('------------##############------------')
	log('Generating patterns')
	generatePatterns(files, counts, batchSize)
