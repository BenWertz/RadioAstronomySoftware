import numpy as np
import matplotlib.pyplot as plt
import sys

def splitMeasurements(lines,nlines,offset=0,lineMargins=[0,0]):
	output=[]
	size=nlines+lineMargins[0]+lineMargins[1]
	for n in range(offset+lineMargins[0],len(lines),size):
		output.append(lines[n:n+nlines])
	return output
def getArg(name,defaultValue=0):
	return (defaultValue if name not in argKeys else int(arguments[name]))


if len(sys.argv)<2:
	print("No file selected. Exiting.")
	exit(0)

argPairs=[]
arguments=dict()
argKeys=[]

for arg in sys.argv[2:]:
	if "=" not in arg:continue
	else:
		pair=arg.split("=")
		if pair[1].lower() in ["true","false", "yes", "no"]:
			pair[1]=int(pair[1].lower() in ["true","yes"])
		arguments[pair[0]]=float(pair[1])
		argPairs.append([pair[0],float(pair[1])])
		argKeys.append(pair[0])

print(arguments)

nbins=getArg("bins",256)

file=open(sys.argv[1])

data=file.read()

file.close()

lines=data.split("\n")
mments=splitMeasurements(lines,nbins,0,[5,1])


#print([[a.split(" ") for a in b] for b in mments])
data=[[[float(b),float(a.split(" ")[0]),float(a.split(" ")[1])] for a in mments[b]] for b in range(len(mments))]



#[print(a) for a in mments[10]]
[print(a[0].split(" ")[0]) for a in mments]

xarr=np.array([[data[b][a][0] for a in range(len(mments[b]))] for b in range(len(mments))],dtype=float)
yarr=np.array([[data[b][a][1] for a in range(len(mments[b]))] for b in range(len(mments))],dtype=float)
#parr=np.array([[data[b][a][2]-(data[0][a][2] if getArg("init_baseline",0)==1 else 0) for a in range(len(mments[b]))] for b in range(len(mments))],dtype=float)
parr=np.array([[data[b][a][2]-(data[0][a][2] if getArg("init_baseline",0)==1 else (data[b][0][2] if getArg("f0_baseline") else 0)) for a in range(len(mments[b]))] for b in range(len(mments))],dtype=float)

if getArg("linear_power"):
    for b in range(len(mments)):
        for a in range(len(mments[0])):
            parr[b][a]=pow(10,parr[b][a]*0.1)

if getArg("avg_baseline"):
    avgs=[sum(p)/len(p) for p in parr]
    for b in range(len(mments)):
        for a in range(len(mments[0])):
            parr[b][a]-=avgs[b]

if getArg("time_diff",0):
	for i in range(len(mments)-1,0,-1):
		for j in range(len(mments[i])):
			parr[i][j]-=parr[i-1][j]

#yarr=[[0 for b in range(len(mments[0]))] for a in range(len(mments))]
#parr=[[0 for b in range(len(mments[0]))] for a in range(len(mments))]
#for b in range(len(mments)):
#	for a in range(len(mments[0])):
#		parr[b][a]=float(mments[b][a][1])
#		xarr[b][a]=b
#		yarr[b][a]=mments[b][a][0]
#spectra=np.array(xarr,dtype=float),np.array(yarr,dtype=float),np.array(parr,dtype=float),dtype=float)
fig,ax=plt.subplots()
if getArg("multiline",0):
	for i in range(len(mments)):
		ax.plot(yarr[i],parr[i])
elif getArg("avg",0):
	avgs=[sum(p)/len(p) for p in parr]
	times=[xa[0] for xa in xarr]
	ax.plot(times,avgs)
elif getArg("graphSwitch",0):
	idx=0
	min_val=min([min(k) for k in parr])
	max_val=max([max(k) for k in parr])
	while True:
		plt.title(f"{idx}/{len(mments)}")
		plt.xlim([min(yarr[0]),max(yarr[0])])
		plt.ylim([min_val,max_val])
		ax.plot(yarr[idx],parr[idx])
		fig.canvas.draw()
		plt.draw()
		plt.pause(0.1)
#		fig.canvas.flush_events()
#		plt.flush_events()
		a=input("< / > / exit: ")
		if a=="exit":break
		elif a=="<":
			idx=(idx-1)%len(mments)
		elif a==">":
			idx=(idx+1)%len(mments)
		ax.cla()
else:
	ax.pcolormesh(xarr,yarr,parr,shading='gouraud')
plt.show()

#print(spectra)
#for num,spectrum in enumerate(spectra):
#	print(f"{num}:\t{spectrum[:2]}")

