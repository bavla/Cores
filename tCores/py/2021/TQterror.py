gdir = 'D:/vlado/work/Python/graph/Nets'
ndir = 'D:/vlado/work/Python/graph/JSON/tcores/json'
wdir = 'D:/vlado/work/Python/graph/JSON/tcores'
import sys, os, json
sys.path = [gdir]+sys.path; os.chdir(wdir)
from Nets import Network as N
from TQ import *
from datetime import datetime
import cores

prLevel = 2 # basic reports
# prLevel = 1 # detailed reports

# fJSON = 'ExampleA.json'
# fJSON = 'TerrorNews50.json'
# fJSON = "violenceTQ.json"
fJSON = ndir+"/Terror.json"
# fJSON = 'stem.json'
# fJSON = ndir+'/ConnectivityTest.json'

G = N.loadNetsJSON(fJSON); G.delLoops(); G.Info()
print("Temporal cores in: ",fJSON)
t1 = datetime.now()
print("started: ",t1.ctime(),"\n")
Core = cores.TQcores(G,prLevel)
t2 = datetime.now()
print("\nfinished: ",t2.ctime(),"\ntime used: ", t2-t1)

res = { "program": "TQcores", "date": datetime.now().ctime() }
res["network"] = G._info["network"]
res["time"] = G._info["time"]
res["Tlabs"] = G._info["legends"]["Tlabs"]
res["core"] = { u: (G._nodes[u][3]['lab'],Core[u]) for u in Core } 
js = open("TerAllcore.json","w"); js.write(json.dumps(res)); js.close()

