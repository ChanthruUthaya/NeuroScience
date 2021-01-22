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
taum = 20 * mille
El= -70*mille
Vrest = -80 * mille
Vth = -54 * mille
RmIe = 18*mille
RmGs = 0.15
P = 0.5
taus = 10 * mille
Es = 0*mille #Change to excitor/inhabitory

#Time Variables
timestep = 0.25 * mille
tstart = 0
tend = 1
time = np.arange( tstart , tend , timestep)


membrane_potential_neuron_1 = np.zeros(len(time))
membrane_potential_neuron_1[0] = random.randint(-80,-54)*mille

membrane_potential_neuron_2 = np.zeros(len(time))
membrane_potential_neuron_2[0] = random.randint(-80,-54)*mille

def delta_value(V):
    return ((1/taum) * ((El - V) + (RmIe)))

def leaky_fire_model(current_membrane_potential, neuron_number, current_time):
    global voltage_synapse_1_2
    global voltage_synapse_2_1
    if neuron_number == 1:
        new_membrane_potential = current_membrane_potential + timestep*delta_value(current_membrane_potential) + (voltage_synapse_2_1)
        if new_membrane_potential > Vth:
            fire_times_1.append(current_time)
            voltage_synapse_1_2 = synapse_model(voltage_synapse_1_2, current_time, True, new_membrane_potential,s_1_2)
            new_membrane_potential = Vrest
        else:
            voltage_synapse_1_2 = synapse_model(voltage_synapse_1_2, current_time, False, new_membrane_potential,s_1_2)
        #print(voltage_synapse_1_2)

    if neuron_number == 2:
        new_membrane_potential = current_membrane_potential + timestep*delta_value(current_membrane_potential) + (voltage_synapse_1_2)
        if new_membrane_potential > Vth:
            fire_times_2.append(current_time)
            voltage_synapse_2_1 = synapse_model(voltage_synapse_2_1, current_time, True, new_membrane_potential,s_2_1)
            new_membrane_potential = Vrest
        else:
            voltage_synapse_2_1 = synapse_model(voltage_synapse_2_1, current_time, False, new_membrane_potential, s_2_1)

    return new_membrane_potential

def synapse_delta_s(s):
    temp = ((1/taus)*(-s))
    return temp

def synapse_model(voltage_synapse, current_time, spiked, voltage_neuron, s):
    if spiked:
        return RmGs*(s + (timestep*synapse_delta_s(s) + P))*(Es - voltage_neuron)
    else:
        return  RmGs*(s + timestep*synapse_delta_s(s))*(Es - voltage_neuron)

voltage_synapse_1_2 = 0
fire_times_1 = []
voltage_synapse_2_1 = 0
fire_times_2 = []
s_1_2 = 0
s_2_1 = 0
for i in range(1, len(time)):
    membrane_potential_neuron_1[i] = leaky_fire_model(membrane_potential_neuron_1[i-1], 1, time[i])
    print(voltage_synapse_1_2)
    membrane_potential_neuron_2[i] = leaky_fire_model(membrane_potential_neuron_2[i-1], 2, time[i])
    print(voltage_synapse_2_1)
#Plot main data
plt.plot(time, membrane_potential_neuron_1,color='black')
plt.plot(time, membrane_potential_neuron_2,color='red')

for xc in fire_times_1:
    plt.axvline(x=xc, color='black', linestyle='dotted')
for xc in fire_times_2:
    plt.axvline(x=xc, color='red', linestyle='dotted')

plt.ylim(-0.08,-0.045)
plt.xlabel('Time/s')
plt.ylabel('Membrane Potential/V')
plt.title('Voltage as a function of time for Leaky Integrate-and-Fire Neuron')
plt.show()
