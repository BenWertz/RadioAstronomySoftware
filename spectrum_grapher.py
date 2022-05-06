import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import sys
from math import log10

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

matplotlib.rcParams.update({'font.size': 7})

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

raw_lines=data.split("\n")

lines=[]

for line in raw_lines:
	if len(line)>2 and line[0].isnumeric():lines.append(line)

#mments=splitMeasurements(lines,nbins,0,[5,1])
mments=splitMeasurements(lines,nbins,0,[0,0])


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
def graphMultiline(ax,mments,xarr,yarr,parr):
	ax.set_title("All spectra")
	ax.set_xlabel("Frequency (Hz)")
	if getArg("linear_power",0):
		ax.set_ylabel("Power")
	else:
		ax.set_ylabel("Power (dB)")
	for i in range(len(mments)):
		ax.plot(yarr[i],parr[i])
def graphAvg(ax,mments,xarr,yarr,parr):
	ax.set_title("Average power/measurement")
	ax.set_xlabel("Measurement #")
	if getArg("linear_power",0):
		ax.set_ylabel("Power")
	else:
		ax.set_ylabel("Power (dB)")
	avgs=[10*log10(sum([pow(10,0.1*q) for q in p])/len(p)) for p in parr]
	times=[xa[0] for xa in xarr]
	ax.plot(times,avgs)
def graphSpectrumAvg(ax,mments,xarr,yarr,parr):
	ax.set_title("Average spectrum")
	ax.set_xlabel("Frequency (Hz)")
	if getArg("linear_power",0):
		ax.set_ylabel("Power")
	else:
		ax.set_ylabel("Power (dB)")
	avgs=[10*log10(sum([pow(10,0.1*parr[i][p]) for i in range(len(parr))])/len(parr)) for p in range(len(parr[0]))]
	freqs=yarr[0]
	ax.plot(freqs,avgs)
def graphWaterfall(fig,ax,mments,xarr,yarr,parr):
	ax.set_title("Waterfall")
	pcm=ax.pcolormesh(xarr,yarr,parr,shading='gouraud')
	fig.colorbar(pcm,ax=ax)
if getArg("showAll",0):
	fig,axes=plt.subplots(2,2,figsize=(10,7))
	ax0=axes[0,0]
	ax1=axes[1,0]
	ax2=axes[0,1]
	ax3=axes[1,1]
#	ax0.title="Spectra (color-coded)"
	graphMultiline(ax0,mments,xarr,yarr,parr)
	graphAvg(ax1,mments,xarr,yarr,parr)
	graphSpectrumAvg(ax2,mments,xarr,yarr,parr)
	graphWaterfall(fig,ax3,mments,xarr,yarr,parr)
	fig.tight_layout()
elif getArg("multiline",0):
	fig,ax=plt.subplots()
	graphMultiline(ax,mments,xarr,yarr,parr)
elif getArg("avg",0):
	fig,ax=plt.subplots()
	graphAvg(ax,mments,xarr,yarr,parr)
elif getArg("spectrumAvg",0):
	fig,ax=plt.subplots()
	graphSpectrumAvg(ax,mments,xarr,yarr,parr)
elif getArg("graphSwitch",0):
	fig,ax=plt.subplots()
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
		if a in ["exit","x","/"]:
			plt.close()
			exit(0)
		elif a in ["<",","]:
			idx=(idx-1)%len(mments)
		elif a in [">","."]:
			idx=(idx+1)%len(mments)
		ax.cla()
else:
	fig,ax=plt.subplots()
	graphWaterfall(fig,ax,mments,xarr,yarr,parr)
plt.show()

#print(spectra)
#for num,spectrum in enumerate(spectra):
#	print(f"{num}:\t{spectrum[:2]}")

