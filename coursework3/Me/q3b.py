import numpy as np
import matplotlib.pyplot as plt
import random
import math


Hz=1.0
sec=1.0
milli=0.001
nano = 0.000000001
mega = 1000000


taum = 10 * milli
El= -65*milli
Vrest = -65 * milli
Vth = -50 * milli
Rm = 100*mega
Ie = 0
P = 0.5
taus = 2 * milli
Es = 0*milli
aplus = 0.2*nano
amin = 0.25*nano
tplus = 20*milli
tmin = 20*milli
STDP = True

s_array = np.zeros(40)
g_array = [4*nano]*40 #IF STDP ON
#g_array = [1.9807067881569178e-09]*40 #IF STDP OFF

#Time Variables
timestep = 0.25 * milli
tstart = 0
tend = 300
time = np.arange(tstart , tend , timestep)
voltage = Vrest
count = 0
post_st = -1000
pre_st = [0] * 40
t_diff = 0

def d(V):
    return ((1/taum) *(El - V))

def ds(s):
    return ((1/taus)*(-s))

def stdp(g, t_diff):
    if(t_diff <= 0):
        g = g - amin * math.exp(-abs(t_diff)/tmin)
        if g > 4*nano:
            return 4*nano
        elif g < 0:
            return 0
        else:
            return g
    elif(t_diff > 0):
        g = g + aplus * math.exp(-abs(t_diff)/tplus)
        if g > 4*nano:
            return 4*nano
        elif g < 0:
            return 0
        else:
            return g

def sum_voltage(time,r):
    global voltage
    global post_st
    sumv = 0
    for i in range(len(s_array)):
        s_array[i] = s_array[i] + timestep*ds(s_array[i])
        rand = random.random()
        if rand < r*timestep:
            s_array[i] += P
            pre_st[i] = time
            if STDP:
                t_diff = post_st - pre_st[i]
                g_array[i] = stdp(g_array[i],t_diff)
        sumv += Rm*g_array[i]*s_array[i]*(Es-voltage)
    return sumv

def spike(time,r):
    global voltage
    global count
    global post_st
    if voltage >Vth:
        voltage = Vrest
        count += 1
        post_st = time
        if STDP:
            for i in range(len(g_array)):
                t_diff = post_st -pre_st[i]
                g_array[i] = stdp(g_array[i],t_diff)
    sumv = sum_voltage(time,r)
    voltage = voltage + timestep*d(voltage-sumv)

rates = []
rs = []
input_firerate =[]
mean_output_fr =[]
count = 0
for r in range(10,21):
    voltage = Vrest
    count = 0
    g_array = [4*nano]*40
    s_array = np.zeros(40)
    post_st = -1000
    pre_st = [0] * 40
    t_diff = 0
    for i in range(1,len(time)):
        spike(time[i],r)
        if (time[i]%10 == 0 or time[i] == 300-(0.25*milli)):
            print(r)
            print(time[i])
            rates.append(count/10)
            rs.append(time[i])
            count = 0
    mean_output_fr.append(np.sum(rates[-3:])/3)
    input_firerate.append(r)
    rates = []

plt.hist(g_array,10,color='blue')
plt.xlabel("Synapse Weights /nS")
plt.ylabel("Frequency of the synapse weight /Hz")
plt.title("Histogram showing the steady state synaptic weights")
plt.show()
#


plt.plot(input_firerate,mean_output_fr,color='blue')
plt.xlabel("Input firerate /Hz")
plt.ylabel("Mean output firerate /Hz ")
plt.title("Mean output firing rate vs input firing. SDTP On")
plt.show()
