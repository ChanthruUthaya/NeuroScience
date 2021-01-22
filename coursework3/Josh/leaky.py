import numpy as np
import matplotlib.pyplot as plt

#SI Conversion Variables
Hz=1.0
sec=1.0
mille=0.001
nano = 0.000000001
mega = 1000000

#Neuron Configuration
taum =10 * mille
El= -70*mille
Vrest = -70*mille
Vth = -40 * mille
Rm = 10 * mega
Ie = 3.1 * nano
V0 = -70*mille

#Time Variables
timestep = 0.25 * mille
tstart = 0
tend = 1
time = np.arange( tstart , tend , timestep)


def delta_value(V):
    return ((1/taum) * ((El - V) + (Rm*Ie)))

def leaky_fire_model(time):
    #Output variables
    membrane_potential = np.zeros(len(time))
    membrane_potential[0] = V0
    fire_times = []
    #Eulers method for ODE
    for i in range(1, len(time)):
        membrane_potential[i] = membrane_potential[i-1] + timestep*delta_value(membrane_potential[i-1])
        if membrane_potential[i] > Vth:
            fire_times.append(time[i])
            membrane_potential[i] = Vrest
    return membrane_potential, fire_times

#Call function with output values
membrane_potential, fire_times = leaky_fire_model(time)
#Plot main data
plt.plot(time, membrane_potential,color='black')
#Plot times of neuron "firing"
for xc in fire_times:
    plt.axvline(x=xc, color='black', linestyle='dotted')

plt.ylim(-0.07,0)
plt.xlabel('Time/s')
plt.ylabel('Membrane Potential/V')
plt.title('Voltage as a function of time for Leaky Integrate-and-Fire Neuron')
plt.show()
