import re
from turtle import *
from math import *
from random import random, randint, shuffle
from itertools import chain
from warnings import warn
from search import Search
from copy import copy
# http://www.w3schools.com/html/html_colornames.asp

class Graph(Search):
	class graphError(RuntimeError): pass

	Colors = ['White','Black','Red','Blue','Green','Magenta','Cyan',
		'Yellow', 'Brown', 'Orange', 'Lime', 'Pink', 'Purple', 'Orchid',
		'Salmon', 'SeaGreen']
	INFTY = 1e10

	@staticmethod
	def turtleXY(T):
		return ((T[0]-0.5)*window_width(),(T[1]-0.5)*window_height())
	@staticmethod
	def initNode(e): return e[0]
	@staticmethod
	def termNode(e): return e[1]
	@staticmethod
	def index(e): return e[2]
	@staticmethod
	def twin(u,e):
		S={e[0],e[1]}
		if not (u in S):
			warn("Node {0} not on link {1}".format(u,e))
			return None
		elif len(S)==1: return u
		else: return ({e[0],e[1]}-{u}).pop()

	def __init__(self,simple=False,mode=1):
		self._graph = {'simple': simple,'mode': mode}
		self._nodes = {}
		self._links = {}
	def __str__(self): return "Graph:\nNodes: "+ \
		str(list(self.nodes()))+"\nLinks: "+ \
		str([("E" if k>0 else "A") + \
		str((u,v,k)) for (u,v,k) in self.links()])
	def __len__(self): return len(self._nodes)
	def __iter__(self):
		for v in self._nodes.keys(): yield v
	def nodes(self):
		for u in self._nodes.keys(): yield u
	def nodesMode(self,mode):
		for u in self._nodes.keys():
			if self._nodes[u][3]['mode'] == mode: yield u
	def links(self):
		for e in self._links.keys(): yield e
	def edges(self):
		for e in self._links.keys():
			if e[2]>0: yield e
	def arcs(self):
		for a in self._links.keys():
			if a[2]<0: yield a

	def addNode(self,u,mode=1):
		if (not u in self._nodes):
			self._nodes[u] = [{},{},{},{}]
			if self._graph['mode'] > 1:
				self._nodes[u][3]['mode'] = mode
		else: raise self.graphError(
			"Node {0} already defined".format(u))

	def addEdge(self,u,v,w=1):
		p,q = (u,v) if u < v else (v,u)
		if q in self._nodes[p][0]: k = self._nodes[p][0][q][0]+1
		else: k = 1
		edge = (p,q,k)
		if not self._graph['simple'] or (k==1):
			self._nodes[p][0][q] = []
			self._nodes[q][0][p] = []
			self._nodes[p][0][q].append(k)
			self._nodes[q][0][p].append(k)
			self._nodes[p][0][q].append(w)
			self._nodes[q][0][p].append(w)
			self._links[edge] = {'w':w}
		else: raise self.graphError(
			"Link {0} already defined".format(edge))

	def addArc(self,u,v,w=1):
		if v in self._nodes[u][2]: k = self._nodes[u][2][v]+1
		else: k = 1
		arc = (u,v,-k)
		if not self._graph['simple'] or (k==1):
			self._nodes[u][2][v] = []
			self._nodes[v][1][u] = []
			self._nodes[u][2][v].append(k)
			self._nodes[v][1][u].append(k)
			self._nodes[u][2][v].append(w)
			self._nodes[v][1][u].append(w)
			self._links[arc] = {'w':w}
		else: raise self.graphError(
			"Link {0} already defined".format(arc))

	def neighbors(self,u):
		return (set(self._nodes[u][0].keys()) |
				set(self._nodes[u][1].keys()) |
				set(self._nodes[u][2].keys()))
		
	def edgeNeighbors(self,u):
		return set(self._nodes[u][0].keys())
	def inArcNeighbors(self,u):
		return set(self._nodes[u][1].keys())
	def outArcNeighbors(self,u):
		return set(self._nodes[u][2].keys())
	
	def inNeighbors(self,u):
		return (set(self._nodes[u][0].keys()) |
				set(self._nodes[u][1].keys()))
	def outNeighbors(self,u):
		return (set(self._nodes[u][0].keys()) |
				set(self._nodes[u][2].keys()))
	
	def edgeStar(self,u):
		for (v,[k,w]) in self._nodes[u][0].items():
			for i in range(k):
				yield (u,v,i+1,w)
	def inArcStar(self,u):
		for (v,[k,w]) in self._nodes[u][1].items():
			for i in range(k): yield (v,u,-i-1,w)
	def outArcStar(self,u):
		for (v,[k,w]) in self._nodes[u][2].items():
			for i in range(k): yield (u,v,-i-1,w)

	def star(self,u):
		return chain(self.edgeStar(u),self.inArcStar(u),self.outArcStar(u))
	def inStar(self,u):
		return chain(self.edgeStar(u),self.inArcStar(u))
	def outStar(self,u):
		return chain(self.edgeStar(u),self.outArcStar(u))
	
	def lenStar(self, u):
		length = 0
		for (v,[k,w]) in self._nodes[u][0].items():
			length += k
		for (v,[k,w]) in self._nodes[u][1].items():
			length += k
		for (v,[k,w]) in self._nodes[u][2].items():
			length += k
		return length
	def lenInStar(self, u):
		length = 0
		for (v,[k,w]) in self._nodes[u][0].items():
			length += k
		for (v,[k,w]) in self._nodes[u][1].items():
			length += k
		return length
	def lenOutStar(self, u):
		length = 0
		for (v,[k,w]) in self._nodes[u][0].items():
			length += k
		for (v,[k,w]) in self._nodes[u][2].items():
			length += k
		return length

	
	def delEdge(self,u,v):
		p,q = (u,v) if u < v else (v,u)
		if q in self._nodes[p][0]:
			k = self._nodes[p][0][q]
			edge = (p,q,k)
			if k==1:
				del(self._nodes[p][0][q]); del(self._nodes[q][0][p])
			else:
				self._nodes[p][0][q] -= 1; self._nodes[q][0][p] -= 1
			del(self._links[edge])
		else:
			raise self.graphError(
				"Deleting nonexistent edge {0}".format(edge))
	def delArc(self,u,v):
		if v in self._nodes[u][2]:
			k = self._nodes[u][2][v]
			arc = (u,v,-k)
			if k==1:
				del(self._nodes[u][2][v]); del(self._nodes[v][1][u])
			else:
				self._nodes[u][2][v] -= 1; self._nodes[v][1][u] -= 1
			del(self._links[arc])
		else:
			raise self.graphError(
				"Deleting nonexistent edge {0}".format(arc))
	def delNode(self,u):
		for v in self.neighbors(u):
			p,q = (u,v) if u < v else (v,u)
			if q in self._nodes[p][0]:
				k = self._nodes[p][0][q][0]
				for i in range(k): del(self._links[(p,q,i+1)])
				del(self._nodes[v][0][u])
			elif v in self._nodes[u][2]:
				k = self._nodes[u][2][v]
				for i in range(k): del(self._links[(u,v,-i-1)])
				del(self._nodes[v][1][u])
			elif v in self._nodes[u][1]:
				k = self._nodes[u][1][v]
				for i in range(k): del(self._links[(v,u,-i-1)])
				del(self._nodes[v][2][u])
		del(self._nodes[u])
	def setGraph(self,key,val): self._graph[key] = val
	def getGraph(self,key): return self._graph[key]
	def setNode(self,u,key,val): self._nodes[u][3][key] = val
	def setNodes(self,key,val):
		for u in self._nodes.keys(): self._nodes[u][3][key] = val
	def getNode(self,u,key): return self._nodes[u][3][key]
	def setLink(self,e,key,val): self._links[e][key] = val
	def getLink(self,e,key): return self._links[e][key]
	def degree(self,u):
		return ( sum(self._nodes[u][0].values()) +
				 sum(self._nodes[u][1].values()) +
				 sum(self._nodes[u][2].values()) )
	def reverse(self):
		R = Graph()
		R._graph = copy(self._graph)
		for v in self._nodes.keys():
			R._nodes[v] = [ dict(self._nodes[v][0]),
				dict(self._nodes[v][2]),dict(self._nodes[v][1]),
				dict(self._nodes[v][3]) ]
		for e in self._links.keys():
			u,v,k = e
			if k < 0:
				R._links[(v,u,k)] = dict(self._links[e])
			else:
				R._links[e] = dict(self._links[e])
		return R
	def transpose(self):
		if self._graph['mode'] == 1: raise self.graphError(
			"transpose works on two-mode networks")
		T = Graph()
		n1 = len(list(self.nodesMode(1))); n2 = len(list(self.nodesMode(2)))
		T._graph = copy(self._graph)
		for v in self._nodes.keys():
			if self._nodes[v][3]['mode']==1:
				t = v+n2; mode = 2
			else: t = v-n1; mode = 1
			T.addNode(t)
			T._nodes[t][3] = dict(self._nodes[v][3])
			T._nodes[t][3]['mode'] = mode
		for p in self._links.keys():
			u,v,k = p; q = (v-n1,u+n2,k)
			if k < 0: T.addArc(v-n1,u+n2,-k)
			else: T.addEdge(v-n1,u+n2,k)
			T._links[q] = dict(self._links[p])
		return T
	def one2twoMode(self):
		T = Graph(); n = len(self._nodes)
		T._graph = copy(self._graph); T._graph['mode'] = 2
		for v in self._nodes.keys():
			T.addNode(v); T.addNode(v+n)
			T._nodes[v][3] = dict(self._nodes[v][3])
			T._nodes[v][3]['mode'] = 1
			T._nodes[v+n][3] = dict(self._nodes[v][3])
			T._nodes[v+n][3]['mode'] = 2
		for p in self._links.keys():
			u,v,k = p; q = (u,v+n,k)
			if k < 0: T.addArc(u,v+n,-k)
			else: T.addEdge(u,v+n,k)
			T._links[q] = dict(self._links[p])
		return T			
	def two2oneEq(self,noDup=True):
		n1 = len(list(self.nodesMode(1)))
		n2 = len(list(self.nodesMode(2)))
		if n1 != n2: raise Graph.graphError(
			"Nonsquare two-mode network {0} != {1}".format(n1,n2))			
		G = Graph()
		G._graph = copy(self._graph); G._graph['mode'] = 1
		for v in self.nodesMode(1):
			G.addNode(v)
			G._nodes[v][3] = dict(self._nodes[v][3])
			del(G._nodes[v][3]['mode'])
		for p in self._links.keys():
			u,v,k = p
			q = (u,v-n1,k) if (k < 0) or (u < v-n1) else (v-n1,u,k)
			u,v,k = q; add = True			
			if k < 0: G.addArc(u,v,-k)
			elif not((q in G._links) and noDup): G.addEdge(u,v,k)
			else: add = False
			if add:
				G._links[q] = dict(self._links[p])
		return G			
	def two2oneRows(self): 
		G = Graph(); G._graph['mode'] = 1
		for v in self.nodesMode(1):
			G.addNode(v)
			G._nodes[v][3] = dict(self._nodes[v][3])
			del(G._nodes[v][3]['mode'])
		for t in self.nodesMode(2):
			for p in self.inStar(t):
				u = Graph.twin(t,p); pw = self._links[p]['w']
				for q in self.inStar(t):
					v = Graph.twin(t,q)
					if u <= v:
						r = (u,v,1) 
						if not r in G._links: G._links[r] = {'w': 0}
						G._links[r]['w'] += pw*self._links[q]['w']
		return G
	def two2oneCols(self): 
		n1 = len(list(self.nodesMode(1)))
		G = Graph(); G._graph['mode'] = 1
		for v in self.nodesMode(2):
			G.addNode(v-n1)
			G._nodes[v-n1][3] = dict(self._nodes[v-n1][3])
			del(G._nodes[v-n1][3]['mode'])
		for t in self.nodesMode(1):
			for p in self.outStar(t):
				u = Graph.twin(t,p)-n1; pw = self._links[p]['w']
				for q in self.outStar(t):
					v = Graph.twin(t,q)-n1
					if u <= v:
						r = (u,v,1)
						if not r in G._links: G._links[r] = {'w': 0}
						G._links[r]['w'] += pw*self._links[q]['w']
		return G
	def multiply(A,B):
		na2 = len(list(A.nodesMode(2))); nb1 = len(list(B.nodesMode(1)))
		if na2 != nb1: raise Graph.graphError(
			"Noncompatible networks {0} != {1}".format(na2,nb1))			
		na1 = len(list(A.nodesMode(1))); nb2 = len(list(B.nodesMode(2)))
		C = Graph(); C._graph['mode'] = 2; mode = 1
		for v in range(na1+nb2):
			if v==na1: mode = 2
			C.addNode(v+1,mode)
			if v<na1: C._nodes[v+1][3] = dict(A._nodes[v+1][3])
			else: C._nodes[v+1][3] = dict(B._nodes[v+1+nb1-na1][3])
		for t in A.nodesMode(2):
			for p in A.inStar(t):
				u = Graph.twin(t,p); Apw = A._links[p]['w']
				for q in B.outStar(t-na1):
					v = Graph.twin(t-na1,q)+na1-nb1; r = (u,v,1)
					if not r in C._links: C._links[r] = {'w': 0}
					C._links[r]['w'] += Apw*B._links[q]['w']
		return C
	
	def loadPajek(self, file):
		try:
			net = open(file,'r')
		except:
			raise Graph.graphError(
				"Problems with Pajek file {0}".format(file))
		status = 0
		while True:
			line = net.readline()
			if not line: break
			if line[0] == '%': continue
			if line[0] == '*':
				L = re.split('\s+',line.strip())
				control = L[0].lower()
				if control=='*vertices':
					num = eval(L[1])
					twoMode = len(L)>2
					if twoMode:
						self._graph['mode'] = 2
						num1 = eval(L[2]); mode = 1
						for v in range(num):
							if v==num1: mode = 2
							self.addNode(v+1,mode)
					else:	
						for v in range(num): self.addNode(v+1)
					status = 1; continue
				elif control=='*arcs':
					status = 2; continue
				elif control=='*edges':
					status = 3; continue
				else: continue
			elif status == 1:
				L = re.split('\"',line.strip())
				if len(L) > 1:
					K = re.split('\s+',L[2].strip())
					L = L[:2]; L.extend(K)
				else:
					L = re.split('\s+',line.strip())
				node = eval(L[0]); name = L[1]
				self.setNode(node,'lab',name)
				if len(L) > 3:
					self.setNode(node,'x',eval(L[2]))
					self.setNode(node,'y',eval(L[3]))
			elif status == 2:
				L = re.split('\s+',line.strip())
				u = eval(L[0]); v = eval(L[1]);
				if len(L)>2: w = eval(L[2])
				else: w = 1
				self.addArc(u,v,w)
			elif status == 3:
				L = re.split('\s+',line.strip())
				u = eval(L[0]); v = eval(L[1]);
				if len(L)>2: w = eval(L[2])
				else: w = 1
				if u < v : self.addEdge(u,v,w)
				else: self.addEdge(v,u,w)
		net.close()
	def savePajek(self,file):
		net = open(file,'w'); n=len(self._nodes)
		net.write('*vertices '+str(n)+'\n')
		ind = {}
		for (i,v) in enumerate(self._nodes):
			xy = self.getXY(v); ind[v] = i+1
			net.write(str(i+1)+' "'+str(v)+'" '+
				str(xy[0])+' '+str(xy[0])+' 0.5\n')
		net.write('*arcs\n')
		for (u,v,k) in self.links():
			if k<0: net.write(str(ind[u])+' '+str(ind[v])+' '+
				str(self._links[(u,v,k)].get('w',1))+'\n')
		net.write('*edges\n')
		for (u,v,k) in self.links():
			if k>0: net.write(str(ind[u])+' '+str(ind[v])+' '+
				str(self._links[(u,v,k)].get('w',1))+'\n')
		net.close()
	def getXY(self,u):
		if not('x' in self._nodes[u][3]): self._nodes[u][3]['x'] = random()
		if not('y' in self._nodes[u][3]): self._nodes[u][3]['y'] = random()
		return (self._nodes[u][3]['x'],self._nodes[u][3]['y'])
	def drawNode(self,u,rr=10,cols=('white','black')):
		xy = Graph.turtleXY(self.getXY(u))
		pu(); setpos(xy); pd()
		dot(rr,cols[1]); dot(rr-2,cols[0])
		pu(); setpos(xy[0]+rr/1.3,xy[1]-rr/2)
		pencolor('black')
		write(self._nodes[u][3].get('lab',str(u)))
	def drawLink(self,u,v,w=1,col='blue',arc=False):
		xy1 = Graph.turtleXY(self.getXY(u))
		xy2 = Graph.turtleXY(self.getXY(v))
		pu(); setpos(xy2); pd()
		pencolor(col); pensize(w); setpos(xy1)
		if arc:
			seth(towards(xy2)); d = 5+4*w; pu()
			xy = ((xy1[0]+xy2[0])/2,(xy1[1]+xy2[1])/2)
			setpos(xy); pd(); rt(20); bk(d); pu()
			setpos(xy); pd(); lt(40); bk(d)
	def draw(self,W,H,bg,col='col',d=15):
		reset(); title("Draw graf"); colormode(255)
		screensize(W,H,bg); speed(0); ht()
		for (u,v,k) in self.links():
			if k==1: self.drawLink(u,v)
			elif k==-1: self.drawLink(u,v,col='red',arc=True)
		colored = col in self._nodes[u][3].keys()
		for v in self.nodes():
			fcol = self.getNode(v,col) if colored else 'yellow'
			self.drawNode(v,d,(fcol,'black'))
		exitonclick()
	def onCircle(self,p=None):
		if p == None: p = self.nodes()
		n = len(self._nodes); a = 2*pi/n
		for (i,v) in enumerate(p):
			self.setNode(v,'x',0.5+0.45*sin(i*a))
			self.setNode(v,'y',0.5+0.45*cos(i*a))
	def ErdosRenyiGraph(n,m):
		G = Graph()
		for v in range(n): G.addNode(v+1)
		for i in range(m):
			while True:
				u = randint(1,n); v = randint(1,n)
				edge = (u,v,1) if u < v else (v,u,1)
				if not edge in G._links: break
			G.addEdge(u,v)
		return G
	def seqColoring(self,cols):
		pal = cols; fresh = pal[0]; pal = set(pal[1:])
		for v in self.nodes(): self.setNode(v,'col',fresh)
		p=list(self._nodes.keys()); shuffle(p)
		used = set()
		for v in p:
			free = used - \
				{self.getNode(u,'col') for u in self.neighbors(v)}
			if len(free)==0:
				col = pal.pop()
				free.add(col); used.add(col)
			self.setNode(v,'col',free.pop())
		return len(used)