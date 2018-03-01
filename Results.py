############## SAVE PARTITION ##############
def makePartition(C1, C2, net, fName):
	print "Saving partition"
	# 1: in first subset, in generalized two-mode core
	# 2: in second subset, in generalized two-mode core
	# 3: in first subset, not in generalized two-mode core
	# 4: in second subset, not in generalized two-mode core
	writer = '*Vertices ' + str(len(net)) + '\n'
	for indeks in range(1, len(net)+1):
		if indeks in C1: writer += '1\n'
		elif indeks in C2: writer += '2\n'
		elif indeks <= len(list(net.nodesMode(1))): writer += '3\n'
		elif indeks > len(list(net.nodesMode(1))): writer += '4\n'
	f = open(fName.replace('.net', '.clu'),'w')
	f.write(writer)
	f.close()
	print "Partition saved"