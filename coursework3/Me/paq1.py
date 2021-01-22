import numpy as np
import matplotlib.pyplot as plt

#units
milli = 0.001
mega = 1000000
nano = 0.000000001


#parameters

tau = 10*milli
El = -70*milli
Vth = -40*milli
Rm = 10*mega
Ie = 3.1*nano
V0 = -70*milli
Vrest = -70*milli

timestep = 0.25*milli
times = np.arange(0,1,timestep)

def d(V):
    return ((1/tau) * ((El - V) + (Rm*Ie)))

def leaky_fire(times, membrane_pot, firing_times):
    membrane_pot[0] = V0
    for i in range(1, len(times)):
        V = membrane_pot[i-1]
        membrane_pot[i] = V + timestep*d(V)
        if membrane_pot[i] > Vth:
            firing_times.append(times[i])
            membrane_pot[i] = Vrest
    return firing_times, membrane_pot

fire_times, membrane_pot = leaky_fire(times, np.zeros(len(times)), [])

plt.plot(times, membrane_pot,color='blue')
#Plot times of neuron "firing"
for val in fire_times:
    plt.axvline(x=val, color='red', linestyle='dotted')

plt.ylim(-0.07,0)
plt.xlabel('Time/s')
plt.ylabel('Membrane Potential/V')
plt.title('Voltage vs Time for Leaky Integrate-and-Fire Neuron')
plt.show()
