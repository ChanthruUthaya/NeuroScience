import numpy as np
import matplotlib.pyplot as plt
import random

#units
milli = 0.001
mega = 1000000
nano = 0.000000001

#parameters

taum = 20*milli
El = -70*milli
Vth = -54*milli
RmIe = 18 *milli
Vrest = -80*milli

Rmgs = 0.15
p = 0.5
taus = 10*milli
Es = 0*milli

timestep = 0.25 *milli
time = np.arange( 0 , 1 , 0.25*milli)
mem_pot_1 = np.zeros(len(time))
mem_pot_1[0] = random.randint(-80,-54)*milli

mem_pot_2 = np.zeros(len(time))
mem_pot_2[0] = random.randint(-80,-54)*milli

def d(V):
    return ((1/taum) * ((El - V) + (RmIe)))

def ds(s):
    return ((1/taus)*(-s))
    

def leaky_fire_model(current_membrane_potential,current_time,voltage_synapse,s,n):
    new_membrane_potential = current_membrane_potential + timestep*d(current_membrane_potential) + (voltage_synapse)
    if new_membrane_potential > Vth:
        fire_times[n].append(current_time)
        other_vs = Rmgs*(s + (timestep*ds(s) + p))*(Es - new_membrane_potential)
        new_membrane_potential = Vrest
    else:
        other_vs = Rmgs*(s + timestep*ds(s))*(Es - new_membrane_potential)
    return new_membrane_potential, other_vs

vs1to2 = 0
vs2to1 = 0
fire_times= [[],[]]
s_1_2 = 0
s_2_1 = 0
for i in range(1, len(time)):
    mem_pot_1[i], vs1to2 = leaky_fire_model(mem_pot_1[i-1],time[i],vs2to1,s_1_2,0)
    #print("vs2to1: " + str(vs2to1))
    mem_pot_2[i], vs2to1 = leaky_fire_model(mem_pot_2[i-1],time[i],vs1to2,s_2_1,1)
    #print("vs1to2: " + str(vs1to2))

plt.plot(time, mem_pot_1,color='blue')
plt.plot(time, mem_pot_2,color='green')

for v in fire_times[0]:
    plt.axvline(x=v, color='blue', linestyle='dotted')
for v in fire_times[1]:
    plt.axvline(x=v, color='green', linestyle='dotted')

plt.ylim(-0.08,-0.045)
plt.xlabel('Time/s')
plt.ylabel('Membrane Potential/V')
plt.title('Voltage vs Time for Leaky Integrate-and-Fire Neuron')
plt.show() 
