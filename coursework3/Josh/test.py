import numpy as np
import matplotlib.pyplot as plt
import random

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
Es = 0*mille #Change to excitor/inhabitory
r = 15

#Time Variables
timestep = 0.25 * mille
tstart = 0
tend = 1
time = np.arange( tstart , tend , timestep)

fire_times = []

membrane_potential_neuron = np.zeros(len(time))
membrane_potential_neuron[0] = Vrest

gi_synapses = np.zeros(40)
gi_synapses.fill(4*nano)
s_synapses = np.zeros(40)

def synapse_delta_s(s):
    return ((1/taus)*(-s))


def delta_value(V):
    return ((1/taum) * ((El - V)))

def leaky_fire_model(current_membrane_potential, current_time):
    sum_synapse_voltages = 0
    for j in range(0,len(s_synapses)):
        random_num = random.random()
        if random_num < 0.00375:
            s_synapses[j] = s_synapses[j] + timestep*synapse_delta_s(s_synapses[j]) + P
        else:
            s_synapses[j] = s_synapses[j] + timestep*synapse_delta_s(s_synapses[j])


    sum_synapse_voltages =  Rm*gi_synapses[0]*(np.sum(s_synapses))*(Es - Vth)/40

    current_membrane_potential = current_membrane_potential + sum_synapse_voltages
    new_membrane_potential = current_membrane_potential + timestep*delta_value(current_membrane_potential)

    if new_membrane_potential > Vth:
        new_membrane_potential = Vrest
        fire_times.append(current_time)

    return new_membrane_potential


for i in range(1,len(time)):
    membrane_potential_neuron[i] = leaky_fire_model(membrane_potential_neuron[i-1], time[i])

#Plot main data

plt.plot(time, membrane_potential_neuron,color='black')

for xc in fire_times:
    plt.axvline(x=xc, color='red', linestyle='dotted')

plt.ylim(-0.065,-0.05)
plt.xlabel('Time/s')
plt.ylabel('Membrane Potential/V')
plt.title('Voltage as a function of time for Leaky Integrate-and-Fire Neuron')
plt.show()
