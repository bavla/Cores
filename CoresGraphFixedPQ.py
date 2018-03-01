from Graph import Graph
from heapdict import heapdict
from Results import makePartition
from pFunctionC import *
import sys

############# GLOBAL VARIABLES ############
d1, d2 = heapdict(), heapdict()										# heapdict {node index: pF}
C1, C2 = [], []															# subsets of the generalized two-mode core
pValues1, pValues2 = {}, {}											# lists of property function values


############## REMOVAL FROM MIN-HEAP INSIDE MAIN LOOP  ##############
def RemoveFromHeap(dRemove, removing, t, CRemove, network, pValues, COther, dOther, pC, mode):
	# Save size of min-heap before removal starts
	length = len(dRemove)
	while True:
		# Check if the removal of nodes is done: the condition
		# for the end is empty min-heap
		if len(CRemove) == 0:
			# If the min-heap is empty before this while loop,
			# no node was removed
			if length == 0: removing = False
			# Else at least one node was removed
			else: removing = True
			break
		# The variable top is the node with the smallest value
		# of the property function in the min-heap.
		top = dRemove.peekitem()
		# If the node top suffice the condition we end the removing of nodes
		if top[1] >= t:
			if length == len(dRemove):
				removing = False
			else: removing = True
			break
		# Remove the node top from min-heap and gen. two-mode core
		top = dRemove.popitem()
		CRemove.remove(top[0])
		
		# Update values of neighbors of the node top
		starOFtop = star(network, dOther, top[0])
		for v in starOFtop:
			pValues[v] = pC(top[0], v, network, dRemove, dOther, starOFtop[v], pValues[v][0], pValues[v][1])
			dOther.__setitem__(v, pValues[v][0]/pValues[v][1])
	return removing
		

############## GENERALIZED TWO-MODE CORES ##############
def CoresBothFixed(network, p1, p1C, p2, p2C, t1, t2):
	print "Algorithm started - both fixed"
	# We assume that the network is two-mode.
	global C1, C2, d1, d2, pValues1, pValues2
	
	# Initialize both min-heaps (C1, C2)
	first = len(list(network.nodesMode(1)))
	for node in network._nodes:
		if node <= first:	C1.append(int(node))
		else: C2.append(int(node))
			
	# Save the values of property function of nodes in dictionaries
	# The starting values of nodes are now set.
	for node in C1:
		pValues1[node] = p1(network, node)
	for node in C2:
		pValues2[node] = p2(network, node)
		
	# Build mim-heap dictionary
	for node, value in pValues1.iteritems():
		d1.__setitem__(node, value[0]/value[1])
	for node, value in pValues2.iteritems():
		d2.__setitem__(node, value[0]/value[1])
	
	print "calculating cores started"
	# Remove all nodes that do not satisfy the condition
	# The variable removing is used to see if any node is removed in one repetition of the loop.
	removing1 = False
	removing2 = False
	while True:
		# Remove nodes from the first subset
		removing1 = RemoveFromHeap(d1, removing1, t1, C1, network,
										pValues2, C2, d2, p2C, 1)
		# Remove nodes from the second subset
		removing2 = RemoveFromHeap(d2, removing2, t2, C2, network,
										pValues1, C1, d1, p1C, 2)
		# If no node was removed end the loop
		if not (removing1 or removing2):
			break
	return C1, C2

def CoresBothFixedHeaps(network, p1, p1C, p2, p2C, t1, t2):
	C1, C2 = CoresBothFixed(network, p1, p1C, p2, p2C, t1, t2)
	return d2


if __name__ == '__main__':
	net = Graph()
	net.loadPajek(sys.argv[1])
	C1, C2 = [], []   
	C1, C2 = CoresBothFixed(net, eval(sys.argv[2]), eval(sys.argv[2] + 'C'), eval(sys.argv[3]), eval(sys.argv[3] + 'C'), float(sys.argv[4]), float(sys.argv[5]))
	print 'The end'
	print 'Size of first subset: %i, size of second subset: %i.' % (len(C1), len(C2))
	makePartition(C1, C2, net, sys.argv[1])
	