gdir = 'D:/vlado/work/Python/graph/Nets'
# wdir = 'D:/vlado/work/Python/graph/JSON'
# wdir = 'D:/vlado/work/Python/graph/JSON/terror'
ndir = 'D:/vlado/work/Python/graph/JSON/tcores/net'
wdir = 'D:/vlado/work/Python/graph/JSON/tcores'
import sys, os, datetime, json
sys.path = [gdir]+sys.path; os.chdir(wdir)
from Nets import Network as N
from TQ import *

prLevel = 0
# fJSON = ndir+'/ExampleC.json'
# fJSON = "Terror.json"
# fJSON = 'stem.json'
# fJSON = 'Terror news 50.json'
# S = N.loadNetsJSON(fJSON); G = S.pairs2edges()
fJSON = ndir+'/ConnectivityTest.json'
# fJSON = 'ExampleB.json'
# fJSON = 'PathfinderTest.json'
G = N.loadNetsJSON(fJSON)
G.delLoops()

def TQcores(G,prLevel=2):
   D = { u: G.TQnetDeg(u) for u in G._nodes }
   if prLevel<2: print("Deg =",D,"\n")
   Core = { u: TQ.cutLE(D[u],0) for u in G.nodes() }
   # core number = 0
   D = { u: TQ.cutGT(D[u],0) for u in G.nodes() }
   D = { u: d for u,d in D.items() if d!=[] }
   Dmin = { u: TQ.minval(D[u]) for u in D }
   step = 0
   while len(D)>0:
      step += 1
      dmin,u = min( (v,k) for k,v in Dmin.items() )
      if (step % 500 == 1) or (prLevel < 2):
         print("{0:3d}. dmin={1:3d}   node={2:4d}".format(step,dmin,u))
      core = TQ.cutEQ(D[u],dmin)
      Core[u] = TQ.sum(Core[u],core)
      change = TQ.setConst(core,-1)
      D[u] = TQ.cutGE(TQ.sum(D[u],change),dmin)
      if len(D[u])==0: del D[u]; del Dmin[u]
      else: Dmin[u] = TQ.minval(D[u])
      for link in G.star(u):
         v = G.twin(u,link)
         if not(v in D): continue
         chLink = TQ.extract(G.getLink(link,'tq'),change)
         if chLink==[]: continue
         diff = TQ.cutGE(TQ.sum(D[v],chLink),0)
         if len(diff)==0: del D[v]; del Dmin[v]
         else:
            D[v] = TQ.lower(diff,dmin)
            Dmin[v] = TQ.minval(D[v])
   print("{0:3d}. dmin={1:3d}   node={2:4d}".format(step,dmin,u))
   if prLevel<2: print("\n-----\nCore =",Core)
   return(Core)

print("Temporal cores in: ",fJSON)
t1 = datetime.datetime.now()
print("started: ",t1.ctime(),"\n")
Core = TQcores(G,prLevel)
t2 = datetime.datetime.now()
print("\nfinished: ",t2.ctime(),"\ntime used: ", t2-t1)


