############## AUXILIARY FUNCTIONS ##############
def indeg(network, v):
	# Get indegree neighbors
	instar1 = list(network.inArcStar(v))
	indeg = {}
	for el in instar1:
		indeg[el[0]] = el[3]
	return indeg
	
def instar(network, d, v):
	# Get indegree neighbors within given subset
	instar1 = indeg(network, v)
	instar = {}
	for node, value in instar1.iteritems():
		if node in d.keys():	instar[node] = value
	return instar

def outdeg(network, v):
	# Get outdegree neighbors
	outstar1 = list(network.outArcStar(v))
	outdeg = {}
	for el in outstar1:
		outdeg[el[0]] = el[3]
	return outdeg

def outstar(network, d, v):
	# Get outdegree neighbors within given subset
	outstar1 = outdeg(network, v)
	outstar = {}
	for node, value in outstar1.iteritems():
		if node in d.keys():	outstar[node] = value
	return outstar

def deg(network, v):
	# Get all neighbors
	edgestar = list(network.edgeStar(v))
	outstar1 = list(network.outArcStar(v))
	instar1 = list(network.inArcStar(v))
	deg = {}
	for el in instar1:
		deg[el[0]] = el[3]
	for el in outstar1:
		deg[el[1]] = el[3]
	for el in edgestar:
		deg[el[1]] = el[3]
	return deg

def star(network, d, v):
	# Get all neighbors within given subset
	deg1 = deg(network, v)
	star1 = {}
	for node, value in deg1.iteritems():
		if node in d.keys():	star1[node] = value
	return star1
		

############## CALCULATE PROPERTY FUNCTION ##############
#	One of the following functions for calculationg a property function is 
#	selected. This function is used in the initizalization - calculating values
#	of all nodes. When the value of a node is updated we do not use these 
#	functions but the functions following these.
#	The result is a pair of the denominator and the numerator of a value.
#	Rezultat je par: stevec in imenovalec stevila, ki predstavlja rezultat.
	
# degree of a node
def p1(network, v):	return (len(deg(network, v)), 1)
	
# indegree of a node
def p2(network, v):	return (len(indeg(network, v)), 1)
	
# outdegree of a node
def p3(network, v):	return (len(outdeg(network, v)), 1)
	
# indegree and outdegree of a node
def p4(network, v):	return (len(indeg(network, v)) + len(outdeg(network, v)), 1)

# sum of weights of links that have a node v for an end node
def p5(network, v):
	deg1 = deg(network, v)
	return (sum(deg1.values()), 1) if len(deg1)>0 else (0, 1)

# maximum of weights of links that have a node v for an end node
def p6(network, v):
	deg1 = deg(network, v)
	return (max(deg1.values()), 1) if len(deg1)>0 else (0, 1)

# number of neighbors of a node v
def p7(network, v):
	deg1 = len(deg(network, v))
	return (float(deg1), deg1) if deg1>0 else (0.0, 1)

# relative density of a neighborhood of a node v
def p8(network, v):
	deg1 = deg(network, v)
	value = 1
	for u in deg1:
		value = max([value, network.lenStar(u)])
	return (float(len(deg1)), value)

# range of degrees of neighbors of a node v
def p9(network, v):
	star1 = deg(network, v)
	mini, maksi = 1e308, 0
	for u in star1:
		degree = network.lenStar(u)
		maksi = max([maksi, degree])
		mini = min([mini, degree])
	return (maksi-mini, 1) if len(star1)>0 else (0.0, 1)

# total range of degrees of neighbors of a node v
def p10(network, v):
	star1 = deg(network, v)
	mini, maksi = len(star1), len(star1)
	for u in star1:
		degree = network.lenStar(u)
		maksi = max([maksi, degree])
		mini = min([mini, degree])
	return (maksi-mini, 1)

# proportion of weights of links with a node v as end node
def p11(network, v):
	star1 = deg(network, v)
	lenstar1 = sum(star1.values())
	return (float(lenstar1),lenstar1) if len(star1)>0 else (0.0,1)
	
	

############## UPDATE PROPERTY FUNCTION ##############
#	The following functions are the updates of values of a property function.
#	The node v is removed node, the node s is a neighbor of removed node.
#	The network is represented with the variable network.
#	The subset of a generalized teo-mode core with node v is represented with
#	the variable dv, the other subset is represented with the variable ds.
#	The value of the variable weight is equal to the weight of link between v and 
#	s. The values of variables st and im are equal to the current value of s.
#	These functions are listed in the same order as functions for calculation of
#	a values of a property function.
def p1C(v, s, network, dv, ds, weight, st, im=1):
	return (st-1, 1) if st>0 else (0,1)

def p2C(v, s, network, dv, ds, weight, st, im=1):
	if v in instar(network, ds, s):	
		return (st - 1, 1)
	return (st, 1)

def p3C(v, s, network, dv, ds, weight, st, im=1):
	if v in outstar(network, ds, s):
		return (st - 1, 1)
	return (st, 1)

def p4C(v, s, network, dv, ds, weight, st, im=1):
	curr = st
	if v in instar(network, ds, s):
		curr -= 1
	if v in outstar(network, ds, s):
		curr -= 1
	return (curr, 1)

def p5C(v, s, network, dv, ds, weight, st, im=1):
	return (st-weight, 1) if st>weight else (0.0, 1)

def p6C(v, s, network, dv, ds, weight, st, im=1):
	if st > weight:	return (st, 1)
	else:
		star1 = star(network, dv, s)
		return (max(star1.values()), 1) if len(star1)>0 else (0,1) 
		
def p7C(v, s, network, dv, ds, weight, st, im):
	return (st - 1, im)

def p8C(v, s, network, dv, ds, weight, st, im):
	return (st - 1, im)

def p9C(v, s, network, dv, ds, weight, st, im=1):
	star1 = star(network, dv, s)
	mini, maksi = 1e308, 0
	for u in star1:
		degree = len(star(network, ds, u))
		maksi = max([maksi, degree])
		mini = min([mini, degree])
	return (maksi-mini, 1)

def p10C(v, s, network, dv, ds, weight, st, im=1):
	star1 = star(network, dv, s)
	mini, maksi = len(star1), len(star1)
	for u in star1:
		degree = len(instar(network, ds, u)) + len(outstar(network, ds, u))
		maksi = max([maksi, degree])
		mini = min([mini, degree])
	return (maksi-mini, 1)

def p11C(v, s, network, dv, ds, weight, st, im):
	return (st - weight, im)
