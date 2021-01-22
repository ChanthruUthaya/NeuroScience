import random as rnd
import statistics as stats
import math
import numpy as np
import matplotlib.pyplot as plt

def get_spike_train(rate,big_t,tau_ref):

    if 1<=rate*tau_ref:
        print("firing rate not possible given refractory period f/p")
        return []


    exp_rate=rate/(1-tau_ref*rate)

    spike_train=[]

    t=rnd.expovariate(exp_rate)

    while t< big_t:
        spike_train.append(t)
        t+=tau_ref+rnd.expovariate(exp_rate)

    return spike_train


def inter_spike(spike_train):
    inter_spike_t = []
    for i,x in enumerate(spike_train):
        next = i+1
        if(next < len(spike_train)):
            inter = spike_train[next]-x
            inter_spike_t.append(inter)
    return inter_spike_t

    
def count_spikes(spike_train, window_size,big_t):
    a = []
    count = 0
    start = 1
    for i,x in enumerate(spike_train):
        curr = float(window_size*start)
        if(x > curr):
            a.append(count)
            start += 1
            curr = float(window_size*start)
            while(x > curr):
                a.append(0)
                start += 1
                curr = float(window_size*start)
            count = 1
        else:
            count += 1
        if(i == len(spike_train) -1):
            a.append(count)
    return a

def fano(counts):
    var = stats.variance(counts)
    mu = stats.mean(counts)
    return var / mu

def var_coef(inter_spikes):
    sig = np.std(inter_spikes)
    mu = np.mean(inter_spikes)
    return sig / mu

def load_data(filename,T):

    data_array = [T(line.strip()) for line in open(filename, 'r')]

    return data_array

def gen_times(spikes):
    times = []
    period = 2 * 0.001
    running = float(0)
    for i in range(len(spikes)):
        if(spikes[i] == 0):
            running += period
        else:
            running +=period
            times.append(running)
    return times

def auto_corr_array(spike_train, num_spikes):
    arr = np.zeros((101,), dtype=int)
    for i in range(len(spike_train)):
        if(spike_train[i] == 1):
            for j in range(-50,51):
                if(i+j > 0 and i+j < len(spike_train)-1):
                    if(spike_train[i+j] == 1):
                        arr[j+50] += 1
    print(num_spikes)
    arr = [float(num)/num_spikes for num in arr]
    return arr

def plot_auto(corr_arr):
    x_label = np.arange(-100,102,2)
    plt.bar(x_label,corr_arr)
    plt.ylabel('Autocorrelation')
    plt.title('Time Interval -ms')
    plt.show()

def sta(spike_train, num_spikes, stim_train):
    
    arr = np.zeros((50,), dtype=float)
    for i in range(len(spike_train)):
        
        if(spike_train[i] == 1):
            
            for j in range(-50,0):
                
                if(i+j > 0):
                    
                    arr[j+50] += stim_train[i+j]
    print(num_spikes)
    print(arr)
    arr = [float(num)/num_spikes for num in arr]
    print(len(arr))
    return arr

def plot_sta(sta_arr):
    x_label = np.arange(-100,0,2)
    plt.bar(x_label,sta_arr)
    plt.ylabel('spike trigge average')
    plt.title('Time Interval -ms')
    plt.show()