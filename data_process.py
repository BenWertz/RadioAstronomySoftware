#!/usr/bin/python3
import numpy as np
from datetime import datetime
from sys import argv
from os import system as CMD

def splitMeasurements(lines,nlines,offset=0,lineMargins=[0,0]):
        output=[]
        size=nlines+lineMargins[0]+lineMargins[1]
        for n in range(offset+lineMargins[0],len(lines),size):
                output.append(lines[n:n+nlines])
        return output

class Spectrum:
	INTENDED_NAMES=dict()
	NAME_LIST=[]
	SPECTRUM_NAMES=dict()
	def __init__(self, name, freqs, values, history=""):
		if name not in Spectrum.INTENDED_NAMES:
			Spectrum.INTENDED_NAMES[name]=1
			self.name=name
		else:
			self.name=name+"("+str(Spectrum.INTENDED_NAMES[name])+")"
			Spectrum.INTENDED_NAMES[name]+=1
		Spectrum.NAME_LIST.append(self.name)
		Spectrum.SPECTRUM_NAMES[self.name]=self
		self.name=name
		self.bins=len(freqs)
		self.freqs=freqs
		self.values=values
		#self.originalName=self.name
		self.hasHistory=(len(history)!=0)
		self.history=(history if self.hasHistory else "'"+name+"'")
		self.pairs=np.array(list(zip(self.freqs,self.values)))
	def rename(self,name):
		if Spectrum.INTENDED_NAMES[self.name]==1:
			del Spectrum.INTENDED_NAMES[self.name]
		else:
			Spectrum.INTENDED_NAMES[self.name]-=1
		Spectrum.NAME_LIST.remove(self.name)
		del Spectrum.SPECTRUM_NAMES[self.name]
		if name not in Spectrum.INTENDED_NAMES:
			Spectrum.INTENDED_NAMES[name]=1
			self.name=name
		else:
			self.name=name+"("+str(Spectrum.INTENDED_NAMES[name])+")"
			Spectrum.INTENDED_NAMES[name]+=1
		Spectrum.NAME_LIST.append(self.name)
		Spectrum.SPECTRUM_NAMES[self.name]=self
		return self
	def __repr__(self):
		return f"Spectrum(\n\tname={self.name},\n\tfreqs={repr(self.freqs)},\n\tvalues={repr(self.values)}\n)"
	def checkValidity(self, spectrum2):
		if self.bins!=spectrum2.bins:
			print("[ERROR]: Spectra are not compatible (different bin counts)!")
			return False
		elif any([self.freqs[i]!=spectrum2.freqs[i] for i in range(self.bins)]):
			print("[ERROR]: Spectra are not compatible (frequencies do not match up)!")
			return False
		else:
			return True
	def operate(spectrum1,spectrum2,operator,output_name):
#		elif type(spectrum1)==float:
#			return Spectrum(output_name,
#				np.array(spectrum2.freqs),
#				np.array([operator(spectrum1,spectrum2.values[i]) for i in range(spectrum2.bins)])
#			)
		if type(spectrum2) in [float,int]:
			return Spectrum(output_name,
				np.array(spectrum1.freqs),
				np.array([operator(spectrum1.values[i],spectrum2) for i in range(spectrum1.bins)])
			)
		elif spectrum1.checkValidity(spectrum2):
			return Spectrum(output_name,
				np.array(spectrum1.freqs),
				np.array([operator(spectrum1.values[i],spectrum2.values[i]) for i in range(spectrum1.bins)])
			)
		else:
			return "INVALID"
	def __add__(self,spectrum2):
		return self.operate(spectrum2,lambda x,y:x+y,f"([{self.name}]+[{(str(spectrum2) if type(spectrum2) in [float,int] else spectrum2.name)}])")
	def __radd__(self,spectrum2):
		return self.operate(spectrum2,lambda x,y:x+y,f"([{(str(spectrum2) if type(spectrum2) in [float,int] else spectrum2.name)}]+[{self.name}])")
	def __sub__(self,spectrum2):
		return self.operate(spectrum2,lambda x,y:x-y,f"([{self.name}]-[{(str(spectrum2) if type(spectrum2) in [float,int] else spectrum2.name)}])")
	def __rsub__(self,spectrum2):
		return self.operate(spectrum2,lambda x,y:y-x,f"([{(str(spectrum2) if type(spectrum2) in [float,int] else spectrum2.name)}]-{self.name})")
	def __mul__(self,spectrum2):
		return self.operate(spectrum2,lambda x,y:x*y,f"([{self.name}]*[{(str(spectrum2) if type(spectrum2) in [float,int] else spectrum2.name)}])")
	def __rmul__(self,spectrum2):
		return self.operate(spectrum2,lambda x,y:y*x,f"([{(str(spectrum2) if type(spectrum2) in [float,int] else spectrum2.name)}]*[{self.name}])")
	def __truediv__(self,spectrum2):
		return self.operate(spectrum2,lambda x,y:x/y,f"([{self.name}]/[{(str(spectrum2) if type(spectrum2) in [float,int] else spectrum2.name)}])")
	def __rtruediv__(self,spectrum2):
		return self.operate(spectrum2,lambda x,y:y/x,f"([{(str(spectrum2) if type(spectrum2) in [float,int] else spectrum2.name)}]/[{self.name}])")
	def __neg__(self):
		return Spectrum(f"-[{self.name}]",np.array(self.freqs),
			np.array([-v for v in self.values],dtype=np.float32)
		)
def read(path,name="",quiet=False):
	freqs=[]
	powers=[]
	with open(path,"r") as file:
		text=file.read()
		lines=text.split("\n")
		for l in lines:
			if "#" in l or len(l)<=1:
				continue
			values=l.split(" ")
			freqs.append(float(values[0]))
			powers.append(float(values[1]))
	if not quiet:print(f"File: {path}, bins: {len(freqs)}")
	spectrum=Spectrum((name if len(name)!=0 else path),np.array(freqs,dtype=np.float32),np.array(powers,dtype=np.float32),f"File: '{path}'")
	if not quiet:print(f"Data read from {path}, stored as '{spectrum.name}'")
	return spectrum
#	print(set(zip(freqs,powers)))
def multiRead(path,name="",nbins=1024,quiet=False):
    text=""
    with open(path,"r") as file:
        text=file.read()
    lines=text.split("\n")
    mments=splitMeasurements(lines,nbins,0,[5,1])
    data=[[[float(a.split(" ")[0]),float(a.split(" ")[1])] for a in mments[b]] for b in range(len(mments))]
    spectra=[]
    if not quiet:print(f"File: {path}, bins: {nbins}")
    for i in range(len(mments)):
        spectra.append(
            Spectrum(
                name+"["+str(i)+"]",
                np.array([data[i][a][0] for a in range(len(mments[i]))],dtype=np.float32),
                np.array([data[i][a][1] for a in range(len(mments[i]))],dtype=np.float32),
                f"File: '{path}', entry {i}/{len(mments)}"
            )
        )
    if not quiet:print(f"Data read from {path}, stored as list of {len(spectra)} spectra.")
    return spectra
def writeArray(spectra,path,quiet=False):
    with open(path,"w") as file:
        for i in range(len(spectra)):
            spectrum=spectra[i]
            file.write(f"# '{path}': Output from data_process.py (data from rtl_power_fftw)\n")
            file.write(f"# Date created: {str(datetime.now())}\n")
            file.write(f"# Name: {spectrum.name}\n")
            file.write(f"# Bins: {spectrum.bins}\n")
            file.write(f"# Frequency range: [{min(spectrum.freqs)} Hz {max(spectrum.freqs)} Hz]\n")
            for i in range(spectrum.bins):
                file.write(str(spectrum.freqs[i])+" "+str(spectrum.values[i])+"\n")
            file.write("\n")
            if not quiet:print(f"Spectrum {i}/{len(spectra)} written to file.")
    if not quiet:print(f"Spectra were succesfully written to {path}!")
def write(spectrum,path,quiet=False):
	with open(path,"w") as file:
		file.write(f"# '{path}': Output from data_process.py (data from rtl_power_fftw)\n")
		file.write(f"# Date created: {str(datetime.now())}\n")
		file.write(f"# Operations: {spectrum.name}, where:\n")
		for name in Spectrum.NAME_LIST:
			spectrum=Spectrum.SPECTRUM_NAMES[name]
			if spectrum.history!=f"'{spectrum.name}'":
				file.write(f"#    {name} = {Spectrum.SPECTRUM_NAMES[name].history}\n")
		file.write(f"# Bins: {spectrum.bins}\n")
		file.write(f"# Frequency range: [{min(spectrum.freqs)} Hz <-> {max(spectrum.freqs)} Hz]\n")
		for i in range(spectrum.bins):
			file.write(str(spectrum.freqs[i])+" "+str(spectrum.values[i])+"\n")
	if not quiet:print(f"'{spectrum.name}' was succesfully written to {path}!")
if len(argv)==2 and argv[1]=="shell":
	while True:
		i=input(">>> ")
		if i=="exit":break
		try:
			if i in globals():
				print(eval(i))
			else:
				output=exec(i)
				print("Output: "+str(output))
		except Exception as e:
			print(str(e))
#a=read("b_008.dat","$1")
#b=read("b_009.dat","$2")
#write((a-b).rename("OUTPUT"),"test_output.dat")
