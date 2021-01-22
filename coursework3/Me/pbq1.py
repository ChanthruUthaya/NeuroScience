import numpy as np
import matplotlib.pyplot as plt
import random

milli = 0.001
mega = 1000000
nano = 0.000000001

#Configuration variables
taum = 10 * milli
El= -65*milli
Vrest = -65 * milli
Vth = -50 * milli
Rm = 100*mega
Ie = 0
pv = 0.5
taus = 2 * milli
Es = 0*milli #Change to excitor/inhabitory
r = 15

#Part 2 config
aplus = 0.2*nano
aminus = 0.25*nano
taup = 20*milli
taumin = 20*milli

STDPflag = 0 

timestep = 0.25 *milli
time = np.arange(0,1,timestep)

gi = np.zeros(40)
gi.fill(4*nano)
syn_s = np.zeros(40)
prespikes_t = np.zeros(40)
postspike_t = -1000

fire_times = []
membrane_potential_neuron = np.zeros(len(time))
membrane_potential_neuron[0] = Vrest


def d(V):
    return ((1/taum) *(El - V))

def ds(s):
    return ((1/taus)*(-s))

def int_fire(curr_mem, curr_time):
    for i in range(0, len(syn_s)):
        num = random.random()
        if num < r*timestep:
            syn_s[i] = syn_s[i] + timestep*ds(syn_s[i]) + pv
        else:
            syn_s[i] = syn_s[i] + timestep*ds(syn_s[i])

    sum_s_v = Rm*gi[0]*(np.sum(syn_s))*(Es - Vth)/40

    curr_mem = curr_mem + sum_s_v
    new_mem = curr_mem + timestep*d(curr_mem)

    if new_mem > (-50 * milli):
        new_mem = Vrest
        fire_times.append(curr_time)

    return new_mem

for i in range(1, len(time)):
    membrane_potential_neuron[i] = int_fire(membrane_potential_neuron[i-1], time[i])

plt.plot(time, membrane_potential_neuron,color='blue',linewidth=0.7)

for val in fire_times:
    plt.axvline(x=val, color='red', linestyle='dotted')

plt.ylim(-0.065,-0.05)
plt.xlabel('Time/s')
plt.ylabel('Membrane Potential/V')
plt.title('Voltage vs Time for Leaky Integrate-and-Fire Neuron')
plt.show()