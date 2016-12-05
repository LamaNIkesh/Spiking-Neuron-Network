# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 11:01:29 2016

@author: Nikesh Lama
"""

from brian import *
'''****************************************************************************
Parameters & Variables
****************************************************************************'''

b_i = 0.2/ms
c = -65 * mvolt
V_th = 30 * mV

'''****************************************************************************
Create Population of Neurons
****************************************************************************'''

#Neuronal equations of the Izhikevich-neuron

Izhikevich =Equations('''

dv/dt = (0.04/ms/mV)*v**2 + (5/ms) * v + 140*mV/ms - u + ge/ms + gi/ms: mvolt
du/dt = a*((b_i*v) - u) : mvolt/msecond
dge/dt = - ge/(5 * ms) : volt
dgi/dt = -gi/(7 * ms) : volt
a: 1/msecond
d: mvolt/msecond
I_syn : mvolt
tau : msecond
''')

#reset specification of the Izhikevich model
reset = '''
v = c
u += d
'''

#Set up neuron population
N = 50

P = NeuronGroup(N, Izhikevich, threshold= V_th, reset=reset,max_delay = 5 * ms)
P.a = 0.02/ms
P.d = 8 * mV/ms
P.v =c + (V_th - c) * rand(len(P))
P.u = b_i*c
P.ge = 0 * mV
P.gi = 0 * mV

poissoninput = PoissonGroup(1, rates=50 * Hz)

Pe = P.subgroup(N-10)
Pi = P.subgroup(10)

Ce = Connection(Pe, P, 'ge', weight= 5.62*mV, sparseness=0.02)
CeP = Connection(poissoninput, Pe,'ge',weight = 4 * mV)
Ci = Connection(Pi, P, 'gi', weight= -4 * mV, sparseness=0.02)
M = SpikeMonitor(P)
Mv = StateMonitor(P,'v',record = True, when ='before_resets')
Mge = StateMonitor(P,'ge',record = True)
Mgi = StateMonitor(P,'gi',record = True)
MCeP = StateMonitor(P,'v',record = True, when = 'before_resets')
poiss = SpikeMonitor(poissoninput)

run(800 *ms)

print "The number of fires: ", M.nspikes

print "The firing rate is :", float(M.nspikes/0.5), "Hz"


subplot(311)
raster_plot(M)
title("Neurons Fired")
subplot(312)
for i in range (N):
	plot(Mv.times / ms, Mv[i] /mV)
xlabel('Time(ms)')
ylabel('Voltage(mV)')
subplot(313)
for i in range (N):
	plot(Mge.times / ms, Mge[i] /mV)
	plot(Mgi.times /ms, Mgi[i] /mV)
xlabel('Time(ms)')
ylabel('Voltage(mV)')

show()
plot(MCeP.times /ms, MCeP[11] /mV)
xlabel("Time (ms)")
ylabel("Voltage(mV)")
title("Neuron: 12(Time course)")
show()



