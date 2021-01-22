from poisson import *

if __name__ == "__main__":

    #PART1
    
    Hz=1.0
    sec=1.0
    ms=0.001

    rate=35.0 *Hz
    tau_ref=[0,5*ms]

    big_t=1000*sec
   
    window = [10*ms,50*ms,100*ms]

    outF = open("results.txt", "w")
    outF.write("PART1:" + "\n")

    for i in range(len(tau_ref)):
        spike_train=get_spike_train(rate,big_t,tau_ref[i])
        inter_spikes = inter_spike(spike_train)
        outF.write("Refac = " + str(tau_ref[i]*1000) + "ms" + "\n")
        for j in range(len(window)):
            outF.write("Window = " + str(window[j]*1000) + "ms" + "\n")
            counts = count_spikes(spike_train,window[j],big_t)
            f = fano(counts)
            outF.write("fano = " + str(f) + "\n" + "\n")
        v = var_coef(inter_spikes)
        outF.write("var coef = " + str(v) + "\n" + "\n")

    
    #PART2
    #spikes=[int(x) for x in load_data("rho.dat")]
    spikes=load_data("rho.dat",int)

    #print(len(spikes))
    #print(spikes[0:200])
    times = gen_times(spikes)
    inter_spikes_2 = inter_spike(times)
    outF.write("PART2" + "\n")
    for i in range(len(window)):
        outF.write("window = " + str(window[i]*1000) + "ms" + "\n")
        counts_2 = count_spikes(times,window[i],big_t)
        fano_2 = fano(counts_2)
        outF.write("fano = " + str(fano_2) + "\n" +"\n")
    var_coef_2 = var_coef(inter_spikes_2)
    outF.write("var coef = " + str(var_coef_2))
    outF.write("\n" + "\n")


    #PART3
    arr = auto_corr_array(spikes, len(times))
    plot_auto(arr)

    #PART4

    #stimulus=[float(x) for x in load_data("stim.dat")]
    stimulus=load_data("stim.dat",float)

    sta_arr = sta(spikes,len(times),stimulus)
    plot_sta(sta_arr)


