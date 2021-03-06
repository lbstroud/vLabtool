#!/usr/bin/python
from vLabtool.experiment import *
if __name__ == "__main__":
	Exp=Experiment(parent=None,showresult=False)

import vLabtool.interface as interface
from vLabtool.templates.template_Stream import Ui_Form
import numpy as np
import time
import scipy.optimize as optimize
import scipy.fftpack as fftpack

class Handler(QtGui.QFrame,ConvenienceClass,Ui_Form):
	def __init__(self):
		super(Handler, self).__init__()
		self.setupUi(self)
		self.I = interface.Interface()
		self.totalpoints=2000
		self.X=np.arange(self.totalpoints)
		self.Y=np.zeros(self.totalpoints)
		self.looptimer=QtCore.QTimer()
		self.plot = Exp.add2DPlot()
		self.plot.setXRange(0,self.totalpoints)
		self.plot.setYRange(-16,16)
		self.curve = Exp.addCurve(self.plot,'',(255,255,255))
		self.streamfunc="I."+self.cmdlist.currentText()
		self.start_time=time.time()
		self.num=0
		self.arrow=Exp.pg.ArrowItem(angle=90)
		self.plot.addItem(self.arrow)
		self.looptimer=Exp.loopTask(1,self.acquire)
		self.nm=0
		self.start_time=time.time()

	def stream(self):
		self.looptimer.stop()
		self.streamfunc="I."+self.cmdlist.currentText()
		self.X=np.arange(self.totalpoints)
		self.Y=np.zeros(self.totalpoints)
		self.num=0
		self.looptimer=Exp.loopTask(1,self.acquire)

	def acquire(self):
		#if(self.nm<4095):
		#	self.ad.set_voltage(self.nm)
		#	self.nm+=1
		#self.Y=np.roll(self.Y,-1)
		val=eval(self.streamfunc,{'I':self.I})
		self.Y[self.num]=val	#self.mag.read()[1]
		self.lastReading.setText('%.4f'%(val))
		try:
			self.arrow.setPos(self.num,self.Y[self.num])
		except:
			print self.num
		self.num+=1
		if self.num>=self.totalpoints:
			self.num=0
		T=time.time()
		if T-self.start_time>0.5:
			self.curve.setData(self.X,self.Y)
			self.start_time = T

	def parseFunc(self,fn):
		fn_name=fn.split('(')[0]
		args=str(fn.split('(')[1]).split(',')
		int_args=[]
		try:
			args[-1]=args[-1][:-1]
			int_args=[string.atoi(t) for t in args]
		except: 
			int_args=[]	#in case the function has zero arguments, args[-1] will fail.
		method = getattr(self.I,fn_name)
		if method == None :
			print 'no such command :',fn_name
			return None
		else:
			print method,int_args
			return method,int_args

if __name__ == "__main__":
	handler = Handler()
	Exp.addHandler(handler)
	Exp.run()
