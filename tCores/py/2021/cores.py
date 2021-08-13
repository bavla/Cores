from TQ import *

def TQcores(G,prLevel=2):
   D = { u: G.TQnetDeg(u) for u in G._nodes }
   for u in G._nodes:
      if D[u] == []: D[u] = [G._info['time'] + (0,)]
   if prLevel<2: print("Deg =",D,"\n")
   Core = { u: TQ.cutLE(D[u],0) for u in G.nodes() }
   # core number = 0
   D = { u: TQ.cutGT(D[u],0) for u in G.nodes() }
   D = { u: d for u,d in D.items() if d!=[] }
   Dmin = { u: TQ.minval(D[u]) for u in D }
   step = 0; oldmin = -1
   while len(D)>0:
      step += 1
      dmin,u = min( (v,k) for k,v in Dmin.items() )
      if (oldmin < dmin) or (prLevel < 2):
         print("{0:3d}. dmin={1:3d}   node={2:4d}".format(step,dmin,u))
         oldmin = dmin
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
