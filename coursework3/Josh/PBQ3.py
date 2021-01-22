import numpy as np
import matplotlib.pyplot as plt
import random
import math

#SI Conversion Variables
Hz=1.0
sec=1.0
mille=0.001
nano = 0.000000001
mega = 1000000

#Configuration variables
taum = 10 * mille
El= -65*mille
Vrest = -65 * mille
Vth = -50 * mille
Rm = 100*mega
Ie = 0
P = 0.5
taus = 2 * mille
Es = 0*mille
# r = 20
# freq = 20
gi = 4*nano

t_post = -1000
t_pre = [0] * 40
t_diff = 0

aplus = 0.2*nano
amin = 0.25*nano
tplus = 20*mille
tmin = 20*mille
STDP = True

s_array = np.zeros(40)
g_array = [4*nano]*40 #IF STDP ON

#Time Variables
timestep = 0.25 * mille
tstart = 0
tend = 300
time = np.arange( tstart , tend , timestep)
count = 0
rs = []
rates = []



mean_output_fr = []
input_firerate = []

def delta_value(V, v_synapse):
    return ((1/taum) * ((El - V + v_synapse)))

def synapse_delta_s(s):
    return ((1/taus)*(-s))

def sdtp_calc(g, t_diff):
    g = g + aplus * math.exp(-abs(t_diff)/tplus)
    if g > 4*nano:
        return 4*nano
    elif g < 0:
        return 0
    else:
        return g

def sdtp_calc_min(g, t_diff):
    g = g - amin * math.exp(-abs(t_diff)/tmin)
    if g > 4*nano:
        return 4*nano
    elif g < 0:
        return 0
    else:
        return g

for r in range(10,21):
    print(r)
    s_array = np.zeros(40)
    g_array = [4*nano]*40 #IF STDP ON
    running_voltage = Vrest
    for t in range(1,len(time)):
        if running_voltage > Vth:
            running_voltage = Vrest
            count += 1
            t_post = time[t]
            if STDP == True:
                for i in range(len(g_array)):
                    t_diff = t_post - t_pre[i]
                    g_array[i] = sdtp_calc(g_array[i],t_diff)
        svolt = 0
        for j in range(len(s_array)):
            s_array[j] = s_array[j] + timestep*synapse_delta_s(s_array[j])
            random_num = random.random()
            if random_num < r*timestep:
                s_array[j] += P
                t_pre[j] = time[t]
                if STDP == True:
                    t_diff = t_post - t_pre[j]
                    g_array[j] = sdtp_calc_min(g_array[j],t_diff)
            svolt += Rm * g_array[j] * s_array[j] *(Es - running_voltage)

        running_voltage = running_voltage + timestep*delta_value(running_voltage,svolt)

        if (time[t]%10 == 0 or time[t] == 300-(0.25*mille)):
            rates.append(count/10)
            rs.append(time[t])
            count = 0

    mean_output_fr.append(np.sum(rates[-3:])/3)
    input_firerate.append(r)
    count  = 0
    rates = []



plt.hist(g_array,10,color='black')
plt.xlabel("Synapse Weights /nS")
plt.ylabel("Frequency of the synapse weight /Hz")
plt.title("Histogram showing the steady state synaptic weights")
plt.show()
#

#print(mean_output_fr)
plt.plot(input_firerate,mean_output_fr,color='black')
plt.xlabel("Input firerate /Hz")
plt.ylabel("Mean output firerate /Hz ")
plt.title("Mean output firing rate as a function of the input firing. SDTP = Off")
plt.show()
