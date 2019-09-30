## @package dmd_plotting
## Defines functions for making plots
## and movies based on results from the
## DMD methods
from plot_attributes import *
from scipy.interpolate import griddata
from scipy.signal import spectrogram
from map_probes import \
    sp_name_dict, imp_name_dict, \
    imp_rads, imp_phis8, imp_phis32
from mpl_toolkits.mplot3d import Axes3D

## Plots the power spectrum for the DMD
# @param b The bs determined from any DMD algorithm
# @param omega The complex DMD frequencies
# @param f_1 Injector frequency
# @param filename Name of the file corresponding to the shot
# @param typename type string indicating which algorithm is being used
def power_spectrum(b,omega,f_1,filename,typename):
    plt.figure(1000,figsize=(figx, figy+12))
    plt.subplot(4,1,4)
    f_k = np.imag(omega)/(pi*2*1000.0)
    delta_k = abs(np.real(omega)/(pi*2*1000.0))
    sort = np.argsort(f_k)
    power = (b[sort]*np.conj(b[sort])).astype('float')
    power = power/np.max(power)
    if typename=='DMD':
        #plt.scatter(np.sort(f_k), \
        #    power,s=300,c='b',linewidths=3,edgecolors='k')
        #plt.plot(np.sort(f_k), \
        #    power,color='b',linewidth=lw,label=typename)
        plt.semilogy(np.sort(f_k), \
            power,color='b',linewidth=lw,label=typename, \
            path_effects=[pe.Stroke(linewidth=lw+4,foreground='k'), \
            pe.Normal()])
    elif typename=='sparse DMD':
        #plt.scatter(np.sort(f_k), \
        #    power,s=300,c='r',linewidths=3,edgecolors='k')
        #plt.plot(np.sort(f_k), \
        #    power,color='r',linewidth=lw,label=typename)
        plt.semilogy(np.sort(f_k), \
            power,color='r',linewidth=lw,label=typename, \
            path_effects=[pe.Stroke(linewidth=lw+4,foreground='k'), \
            pe.Normal()])
    elif typename=='optimized DMD':
        #plt.scatter(np.sort(f_k), \
        #    power,s=300,c='g',linewidths=3,edgecolors='k')
        #plt.plot(np.sort(f_k), \
        #    power,color='g',linewidth=lw,label=typename)
        plt.semilogy(np.sort(f_k), \
            power,color='g',linewidth=lw,label=typename, \
            path_effects=[pe.Stroke(linewidth=lw+4,foreground='k'), \
            pe.Normal()])
    elif typename[9]=='=':
        plt.semilogy(np.sort(f_k), \
            power,color=np.ravel(np.random.rand(1,3)),linewidth=lw, \
            label=typename, \
            path_effects=[pe.Stroke(linewidth=lw+4,foreground='k'), \
            pe.Normal()])
    plt.yscale('log')
    #plt.legend(loc='upper left',fontsize=ls-8,ncol=3)
    plt.ylabel(r'$|b_k|^2/|b_{max}|^2$',fontsize=fs)
    plt.xlabel(r'$f_k$ (kHz)',fontsize=fs)
    plt.xlim(-3*f_1,3*f_1)
    h=plt.ylabel(r'$|b_k|^2/|b_{max}|^2$',fontsize=fs)
    plt.xlabel(r'f (kHz)',fontsize=fs+4)
    #plt.xlim(-120,120)
    plt.xlim(-3*f_1,3*f_1)
    plt.grid(True)
    ax = plt.gca()
#    ax.set_xticks([-3*f_1,-2*f_1,-f_1, \
#        0,f_1,2*f_1,3*f_1])
#    ax.set_xticklabels([r'$-f_3$',r'$-f_2$',r'$-f_1$', \
#        '0',r'$f_1$',r'$f_2$',r'$f_3$'])

    #ax.set_xticks([-120,-5*f_1,-3*f_1,-f_1, \
    #    f_1,3*f_1,5*f_1,120])
    #ax.set_xticklabels([-120,r'$-f_5$',r'$-f_3$',r'$-f_1$', \
    #    r'$f_1$',r'$f_3$',r'$f_5$',120])
    plt.ylim((1e-10,1e0))
    #ax.set_yticks([1e-12,1e-10,1e-8,1e-6,1e-4,1e-2,1e0])
    #ax.set_yticklabels([1e-10,1e-8,1e-6,1e-4,1e-2,1e0])
    ax.set_xticks([-3*f_1,-2*f_1,-f_1,0, \
        f_1,2*f_1,3*f_1])
    ax.set_xticklabels([r'$-f_3^{inj}$',r'$-f_2^{inj}$',r'$-f_1^{inj}$',0, \
        r'$f_1^{inj}$',r'$f_2^{inj}$',r'$f_3^{inj}$'])
    ax.tick_params(axis='both', which='major', labelsize=ts)
    ax.tick_params(axis='both', which='minor', labelsize=ts)
    plt.grid(True)
    plt.yticks([1e-10,1e-5,1e0])

    plt.figure(10000,figsize=(figx, figy))
    f_k = np.imag(omega)/(pi*2*1000.0)
    delta_k = abs(np.real(omega)/(pi*2*1000.0))
    sort = np.argsort(f_k)
    power = (b[sort]*np.conj(b[sort])).astype('float')
    power = power/np.max(power)
    if typename=='DMD':
        plt.semilogy(np.sort(f_k), \
            power,color='b',linewidth=lw,label=typename, \
            path_effects=[pe.Stroke(linewidth=lw+4,foreground='k'), \
            pe.Normal()])
    elif typename=='sparse DMD':
        plt.semilogy(np.sort(f_k), \
            power,color='r',linewidth=lw,label=typename, \
            path_effects=[pe.Stroke(linewidth=lw+4,foreground='k'), \
            pe.Normal()])
    elif typename=='optimized DMD':
        plt.semilogy(np.sort(f_k), \
            power,color='g',linewidth=lw,label=typename, \
            path_effects=[pe.Stroke(linewidth=lw+4,foreground='k'), \
            pe.Normal()])
    elif typename[9]=='=':
        alphas = np.flip(np.linspace(0.1,1.0,4))
        if float(typename[11:]) == 1e-1:
            alpha = alphas[0]
        if float(typename[11:]) == 1e0:
            alpha = alphas[1]
        if float(typename[11:]) == 1e1:
            alpha = alphas[2]
        if float(typename[11:]) == 1e2:
            alpha = alphas[3]
        plt.semilogy(np.sort(f_k), \
            power,color='r',linewidth=lw, \
            label=typename,alpha=alpha, \
            path_effects=[pe.Stroke(linewidth=lw+4,foreground='k'), \
            pe.Normal()])
    plt.legend(edgecolor='k',facecolor='lightgrey',fontsize=ls,loc='upper left')
    plt.ylabel(r'$|b_k|^2/|b_{max}|^2$',fontsize=fs)
    plt.xlabel('f (kHz)',fontsize=fs)
    plt.xlim(-3*f_1,3*f_1)
    h=plt.ylabel(r'$|b_k|^2/|b_{max}|^2$',fontsize=fs)
    plt.xlabel(r'f (kHz)',fontsize=fs+4)
    #plt.xlim(-120,120)
    plt.xlim(-3*f_1,3*f_1)
    plt.grid(True)
    ax = plt.gca()
#    ax.set_xticks([-3*f_1,-2*f_1,-f_1, \
#        0,f_1,2*f_1,3*f_1])
#    ax.set_xticklabels([r'$-f_3$',r'$-f_2$',r'$-f_1$', \
#        '0',r'$f_1$',r'$f_2$',r'$f_3$'])

    #ax.set_xticks([-120,-5*f_1,-3*f_1,-f_1, \
    #    f_1,3*f_1,5*f_1,120])
    #ax.set_xticklabels([-120,r'$-f_5$',r'$-f_3$',r'$-f_1$', \
    #    r'$f_1$',r'$f_3$',r'$f_5$',120])
    plt.ylim((1e-23,1e0))
    #ax.set_yticks([1e-12,1e-10,1e-8,1e-6,1e-4,1e-2,1e0])
    #ax.set_yticklabels([1e-10,1e-8,1e-6,1e-4,1e-2,1e0])
    ax.set_xticks([-3*f_1,-2*f_1,-f_1,0, \
        f_1,2*f_1,3*f_1])
    ax.set_xticklabels([r'$-f_3$',r'$-f_2$',r'$-f_1$',0, \
        r'$f_1$',r'$f_2$',r'$f_3$'])
    ax.tick_params(axis='both', which='major', labelsize=ts)
    ax.tick_params(axis='both', which='minor', labelsize=ts)
    plt.grid(True)
    plt.yticks([1e-21,1e-14,1e-7,1e0])
    plt.savefig(out_dir+filename)

## Plots real part vs imag part of the f_k frequencies
# @param b The bs determined from any DMD algorithm
# @param omega The complex DMD frequencies
# @param f_1 Injector frequency
# @param filename Name of the file corresponding to the shot
# @param typename type string indicating which algorithm is being used
def freq_phase_plot(b,omega,f_1,filename,typename):
    amp = abs(b)/np.max(abs(b))*1000 #/np.max(abs(b))
    camp = np.log(abs(b)/np.max(abs(b))) #/np.max(abs(b))
    for j in range(len(amp)):
        amp[j] = max(amp[j],100.0)
    sort = np.argsort(amp)
    amp = amp[sort]
    delta_k = np.real(omega[sort])/1000.0/(2*pi)
    f_k = np.imag(omega[sort])/1000.0/(2*pi)
    plt.figure(1000,figsize=(figx, figy+12))
    #plt.subplot(2,1,1)
    if typename=='DMD':
        plt.subplot(4,1,1)
        for snum in range(len(delta_k)):
            h0 = plt.scatter(f_k[snum],delta_k[snum],c='b',s=amp[snum], \
                linewidths=3,edgecolors='k', \
                label=typename,alpha=transparency)
    elif typename=='sparse DMD':
        plt.subplot(4,1,3)
        for snum in range(len(delta_k)):
            h0 = plt.scatter(f_k[snum],delta_k[snum],c='r',s=amp[snum], \
                linewidths=3,edgecolors='k', \
                label=typename,alpha=transparency)
        #plt.scatter(f_k,delta_k,c=amp,s=amp,cmap=plt.cm.get_cmap('Reds'), \
        #    linewidths=2,edgecolors='k', \
        #    label=typename,alpha=transparency)
        #plt.xlabel(r'f (kHz)',fontsize=fs)
    elif typename=='optimized DMD':
        plt.subplot(4,1,2)
        for snum in range(len(delta_k)):
            h0 = plt.scatter(f_k[snum],delta_k[snum],c='g',s=amp[snum], \
                linewidths=3,edgecolors='k', \
                label=typename,alpha=transparency)
        #plt.scatter(f_k,delta_k,c=amp,s=300.0,cmap=plt.cm.get_cmap('Greens'), \
        #    linewidths=2,edgecolors='k', \
        #    label=typename,alpha=transparency)
    plt.legend([h0.get_label()],edgecolor='k',facecolor='lightgrey',fontsize=ts,loc='lower right')
    plt.ylim(-1e3,1e0)
    plt.yscale('symlog',linthreshy=1e-2)
    ax = plt.gca()
    ax.set_yticks([-1e3,-1,-1e-2,1e-2,1e0])
    plt.axhline(y=0,color='k',linewidth=3,linestyle='--')
    #ax.set_yticklabels([r'$-10^2$','',r'$-10^1$','',r'$-10^{-1}$','',0,'',r'$10^{-1}$','',r'$10^1$'])
    #plt.xscale('symlog')
    plt.ylabel(r'$\delta_k$ (kHz)',fontsize=fs+4)
    #plt.title(typename,fontsize=fs)
    plt.xlim(-120,120)
    #plt.xlim(-f_1*3,f_1*3)
    plt.grid(True)
    ax.set_xticks([-120,-5*f_1,-3*f_1,-f_1, \
        f_1,3*f_1,5*f_1,120])
    #ax.set_xticks([-3*f_1,-2*f_1,-f_1, \
    #    0,f_1,2*f_1,3*f_1])
    ax.set_xticklabels([])
    #ax.set_xticklabels(['-100',r'$-f_5$',r'$-f_3$',r'$-f_1$', \
    #    '0',r'$f_1$',r'$f_3$',r'$f_5$','100'])
    #ax.set_xticklabels([r'$-f_3$',r'$-f_2$',r'$-f_1$', \
    #    '0',r'$f_1$',r'$f_2$',r'$f_3$'])
    #ax.tick_params(axis='x', which='major', labelsize=ts)
    #ax.tick_params(axis='x', which='minor', labelsize=ts)
    ax.tick_params(axis='y', which='major', labelsize=ts)
    ax.tick_params(axis='y', which='minor', labelsize=ts)
    plt.savefig(out_dir+filename)

## Creates a sliding window animation
# @param dict A psi-tet dictionary
# @param numwindows Number of sliding windows
# @param dmd_flag Flag to indicate what type of dmd algorithm is being used
def dmd_animation(dict,numwindows,dmd_flag):
    FPS = 5
    f_1 = dict['f_1']
    t0 = dict['t0']
    tf = dict['tf']
    data = dict['SVD_data']
    time = dict['sp_time'][t0:tf]
    dt = dict['sp_time'][1] - dict['sp_time'][0]
    r = np.shape(data)[0]
    tsize = np.shape(data)[1]
    windowsize = int((tsize-1)/float(numwindows))
    if tsize > windowsize:
        starts = np.linspace(0, \
            tsize-windowsize-1,numwindows, dtype='int')
        ends = starts + np.ones(numwindows,dtype='int')*windowsize
    else:
        print('windowsize > tsize, dmd invalid')
    if numwindows > 1:
        if dmd_flag == 1:
            moviename = out_dir+'dmd_movie.mp4'
            typename = 'DMD'
        elif dmd_flag == 2:
            moviename = out_dir+'sdmd_movie.mp4'
            typename = 'sparse DMD'
        elif dmd_flag == 3:
            moviename = out_dir+'odmd_movie.mp4'
            typename = 'optimized DMD'
        fig = plt.figure(5000+dmd_flag,figsize=(figx, figy))
        ani = animation.FuncAnimation( \
            fig, dmd_update, range(numwindows), \
            fargs=(dict,windowsize, \
                numwindows,starts,ends,dmd_flag),
                repeat=False, \
                interval=100, blit=False)
        ani.save(moviename,fps=FPS)
    else:
        print('Using a single window,'+ \
            ' aborting dmd sliding window animation')

## Update function for making the sliding window spectrogram movies
# @param i The ith frame
# @param dict A psi-tet dictionary
# @param windowsize The size of the sliding window
# @param numwindows The number of windows that are used
# @param starts The start points of each of the windows
# @param ends The end points of each of the windows
# @param dmd_flag Which DMD method to use
def dmd_update(i,dict,windowsize,numwindows,starts,ends,dmd_flag):
    f_1 = dict['f_1']
    if dmd_flag == 1:
        Bfield = dict['Bfield']
        Bfield_f1 = dict['Bfield_f1']
        Bfield_f2 = dict['Bfield_f2']
        Bfield_f3 = dict['Bfield_f3']
        Bfield_f0 = dict['Bfield_f0']
        b = np.asarray(dict['Bfield'])[i,:]
        omega = np.asarray(dict['omega'])[i,:]
    if dmd_flag == 2:
        Bfield = dict['sparse_Bfield']
        Bfield_f1 = dict['Bfield_f1']
        Bfield_f2 = dict['Bfield_f2']
        Bfield_f3 = dict['Bfield_f3']
        Bfield_f0 = dict['sparse_Bfield_f0']
        b = np.asarray(dict['sparse_Bfield'])[i,:]
        omega = np.asarray(dict['sparse_omega'])[i,:]
    if dmd_flag == 3:
        Bfield = dict['optimized_Bfield']
        Bfield_f1 = dict['Bfield_f1']
        Bfield_f2 = dict['Bfield_f2']
        Bfield_f3 = dict['Bfield_f3']
        Bfield_f0 = dict['optimized_Bfield_f0']
        b = np.asarray(dict['optimized_Bfield'])[i,:]
        omega = np.asarray(dict['optimized_omega'])[i,:]
    t0 = dict['t0']
    tf = dict['tf']
    data = dict['SVD_data']
    time = dict['sp_time'][t0:tf]
    dt = dict['sp_time'][1] - dict['sp_time'][0]
    r = np.shape(data)[0]
    fig=plt.figure(5000+dmd_flag,figsize=(figx, figy))
    plt.subplot(2,2,1)
    ax1 = plt.gca()
    ax1.clear()
    plt.grid(True)
    index = np.shape(dict['sp_Bpol'])[0]
    inj_index = 2
    if dict['is_HITSI3']:
        inj_index = 3
    plt.plot(time*1000, \
        #dict['tcurr'][:len(dict['tcurr'])-1]/1000.0,'k',label='Itor')
        dict['SVD_data'][index+inj_index,:]*1e4,'k',
        label='B_L01T000',linewidth=lw)

    plt.plot(time[starts[i]:ends[i]]*1000,Bfield[index+inj_index,starts[i]:ends[i]]*1e4,'r',\
        label='sparse DMD',linewidth=lw)
        #dict['tcurr'][t0:tf]/1000.0,'r')
    plt.axvline(dict['sp_time'][t0+starts[i]]*1000,color='k')
    plt.axvline(dict['sp_time'][t0+ends[i]]*1000,color='k')
    plt.xlabel('Time (ms)',fontsize=fs)
    plt.ylabel('B (G)',fontsize=fs)
    ax1.tick_params(axis='both', which='major', labelsize=ts)
    ax1.tick_params(axis='both', which='minor', labelsize=ts)
    plt.xlim(time[0]*1000,time[len(time)-1]*1000)
    #plt.ylim(-500,1000)
    plt.ylim(-150,300)
    ax1.set_yticks([-150,0,150,300])
    #ax1.set_yticks([-500,0,500,1000])
    ax1.set_xticks([0,1,2])
    ax1.set_xticklabels([0,1,2])
    plt.legend(edgecolor='k',facecolor='lightgrey',fontsize=ls,loc='upper left')
    delta_k = np.real(omega)/1000.0/(2*pi)
    f_k = np.imag(omega)/1000.0/(2*pi)

    plt.subplot(2,2,2)
    ax2 = plt.gca()
    ax2.clear()
    sort = np.argsort(f_k)
    power = b[sort]*np.conj(b[sort])
    plt.plot(np.sort(f_k), \
        power/np.max(power), \
        'r',label=r'$|b_k|^2/|b_{max}|^2$',linewidth=lw, \
         path_effects=[pe.Stroke(linewidth=lw+4,foreground='k'), \
         pe.Normal()])

    plt.yscale('log')
    plt.legend(edgecolor='k',facecolor='lightgrey',fontsize=ls,loc='lower right')
    #plt.xlim(-100,100)
    plt.xlim(-3*f_1,3*f_1)
    plt.grid(True)
    ax2.set_xticks([-3*f_1,-2*f_1,-f_1, \
        0,f_1,2*f_1,3*f_1])
    ax2.set_xticklabels([r'$-f_3$','',r'$-f_1$', \
        '',r'$f_1$','',r'$f_3$'])
    #ax2.set_xticks([-5*f_1,-3*f_1,-f_1, \
    #    0,f_1,3*f_1,5*f_1])
    #ax2.set_xticklabels([r'$-f_5$','',r'$-f_1$', \
    #    '',r'$f_1$','',r'$f_5$'])

    plt.ylim((1e-20,1e0))
    ax2.set_yticks([1e-20,1e-15,1e-10,1e-5,1e0])
    plt.xlabel(r'f (kHz)',fontsize=fs)
    ax2.tick_params(axis='both', which='major', labelsize=ts)
    ax2.tick_params(axis='both', which='minor', labelsize=ts)

    plt.subplot(2,2,3)
    plt.grid(True)
    ax3 = plt.gca()
    num_signals = np.shape(Bfield_f1[:,starts[i]:ends[i]])[0]
    nseg = int((tf-t0)/numwindows)
    spectros=np.zeros((66,numwindows))
    #spectros=np.zeros((113,numwindows))
    sample_freq = 1.0/dict['dt']
    for j in range(num_signals):
        freq, stime, spec = spectrogram( \
            np.real(Bfield[j,:numwindows*nseg]), \
            sample_freq, \
            nperseg=nseg, \
            scaling='spectrum', \
            noverlap=0)
        spectros += spec
        print('j=: ',j,', shape=, ',np.shape(Bfield_f1[j,:numwindows*nseg]))
    print((time[0]+stime)*1000,time[0],stime,sample_freq,nseg,tf,t0,numwindows)
    ptime = np.hstack(([0.0],(stime+stime[0])*1000.0))
    pcm = plt.pcolormesh(ptime, freq/1e3, spectros, \
        norm=colors.LogNorm(vmin=1e-10, \
        vmax=1e0),cmap=colormap)
    for starti in range(len(starts)):
        plt.axvline(dict['sp_time'][t0+starts[starti]]*1000,color='k')
    #plt.axvline(dict['sp_time'][t0+ends[i]]*1000,color='k')
    #plt.axvline(dict['sp_time'][t0+starts]*1000,color='k')

    ax3 = plt.gca()
    ax3.set_xticks([0,1,2])
    ax3.set_xticklabels([0,1,2])
    ax3.set_yticks([0,f_1,2*f_1,3*f_1])
    #ax3.set_yticks([0,f_1,3*f_1,5*f_1,100])
    ax3.set_yticklabels([0,r'$f_1$',r'$f_2$',r'$f_3$'])
    #ax3.set_yticklabels([0,r'$f_1$',r'$f_3$',r'$f_5$',100])
    try:
        cb=ax3.collections[-2].colorbar
        cb.remove()
    except:
        print("nothing to remove")
    #cb = plt.colorbar(pcm,ticks=[1e-8,1e-6,1e-4,1e-2])
    #cb = plt.colorbar(pcm,ticks=[1e-8,1e-6,1e-4,1e-2,1e0])
    #cb.ax.tick_params(labelsize=ts)
    #plt.ylim(0,100)
    plt.ylim(0,3*f_1)
    plt.title('All modes',fontsize=fs-14)
    plt.xlabel('Time (ms)',fontsize=fs)
    h=plt.ylabel(r'f (kHz)',fontsize=fs)
    ax3.tick_params(axis='both', which='major', labelsize=ts)
    ax3.tick_params(axis='both', which='minor', labelsize=ts)

    plt.subplot(2,2,4)
    plt.grid(True)
    ax4 = plt.gca()
    ax4.set_xticks([0,1,2])
    ax4.set_xticklabels([0,1,2])

    ax4.set_yticks([0,f_1,2*f_1,3*f_1])
    #ax4.set_yticks([0,f_1,3*f_1,5*f_1,100])
    ax4.set_yticklabels([0,r'$f_1$',r'$f_2$',r'$f_3$'])
    #ax4.set_yticklabels([0,r'$f_1$',r'$f_3$',r'$f_5$',100])
    nseg = int((tf-t0)/numwindows)
    spectros=np.zeros((66,numwindows+1))
    #spectros=np.zeros((113,numwindows+1))
    sample_freq = 1/dict['dt']
    for j in range(num_signals):
        freq, stime, spec = spectrogram( \
            np.real(Bfield_f1[j,:numwindows*nseg]), \
            sample_freq, \
            nperseg=nseg, \
            scaling='spectrum')
        print(j,np.shape(Bfield_f1[j,:numwindows*nseg]))
        spectros += spec
    print((time[0]+stime)*1000,time[0],stime,sample_freq,nseg,tf,t0,numwindows)
    pcm = plt.pcolormesh(ptime, freq/1e3, spectros, \
        norm=colors.LogNorm(vmin=1e-10, \
        vmax=1e0),cmap=colormap)
    for starti in range(len(starts)):
        plt.axvline(dict['sp_time'][t0+starts[starti]]*1000,color='k')
    #plt.axvline(dict['sp_time'][t0+ends[i]]*1000,color='k')
    plt.title('Only $f_1$ mode',fontsize=fs-14)
    try:
        cb=ax4.collections[-2].colorbar
        cb.remove()
    except:
        print("nothing to remove")
    #cb = plt.colorbar(pcm,ticks=[1e-8,1e-6,1e-4,1e-2])
    #cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    cb = plt.colorbar(pcm,ticks=[1e-10,1e-8,1e-6,1e-4,1e-2,1e0])#,cax=cbar_ax)
    cb.ax.tick_params(labelsize=ts)
    plt.xlabel('Time (ms)',fontsize=fs)
    #plt.ylim(0,100)
    plt.ylim(0,3*f_1)
    ax4.tick_params(axis='both', which='major', labelsize=ts)
    ax4.tick_params(axis='both', which='minor', labelsize=ts)
    plt.savefig(out_dir+'spectrogram_'+str(i)+'.png')

## Shows reconstructions using the DMD methods
## of a particular SP and a particular IMP probe
# @param dict A psi-tet dictionary
# @param dmd_flag Flag to indicate what type of dmd algorithm is being used
def make_reconstructions(dict,dmd_flag):
    t0 = dict['t0']
    tf = dict['tf']
    dictname = dict['filename']
    data = dict['SVD_data']
    size_bpol = np.shape(dict['sp_Bpol'])[0]
    size_btor = np.shape(dict['sp_Btor'])[0]
    index = size_bpol
    if dict['num_IMPs'] == 8:
    	imp_index = size_bpol+size_btor+1
    elif dict['num_IMPs'] == 32:
    	imp_index = size_bpol+size_btor+80
    inj_index = 2
    if dict['is_HITSI3']:
        inj_index = 3
    time = dict['sp_time'][t0:tf]*1000
    tsize = len(time)
    plt.figure(2000,figsize=(figx, figy))
    if dmd_flag==1:
        plt.subplot(3,1,1)
        plt.title(dict['filename'][7:13]+', Probe: B_L01T000', \
            fontsize=fs)
        reconstr = dict['Bfield']
        labelstring = 'DMD'
        color = 'b'
    elif dmd_flag==2:
        plt.subplot(3,1,2)
        reconstr = dict['sparse_Bfield']
        labelstring = 'sparse DMD'
        color = 'r'
    elif dmd_flag==3:
        plt.subplot(3,1,3)
        reconstr = dict['optimized_Bfield']
        labelstring = 'optimized DMD'
        color = 'g'
        plt.xlabel('Time (ms)',fontsize=fs)

    plt.plot(time, \
        data[index+inj_index,:]*1e4,'k',linewidth=lw)
    plt.plot(time[:tsize-1], \
        reconstr[index+inj_index,:tsize-1]*1e4,color,\
        label=labelstring+' reconstruction',linewidth=lw, \
        path_effects=[pe.Stroke(linewidth=lw+4,foreground='k'), \
        pe.Normal()])
    plt.grid(True)
    ax = plt.gca()
    ax.tick_params(axis='both', which='major', labelsize=ts)
    ax.tick_params(axis='both', which='minor', labelsize=ts)
    plt.legend(edgecolor='k',facecolor='lightgrey',fontsize=ls,loc='upper left')
    plt.ylabel('B (G)',fontsize=fs)
    #plt.ylim((-150,300))
    #ax.set_yticks([-150,0,150,300])
    plt.ylim((-500,600))
    ax.set_yticks([-500,0,500])
    plt.savefig(out_dir+'reconstructions'+str(dictname[:len(dictname)-4])+'_sp.png')

    plt.figure(3000,figsize=(figx, figy))
    if dmd_flag==1:
        plt.subplot(3,1,1)
        plt.title('BIG-HIT, Probe: IMP #8',fontsize=fs)
        reconstr = dict['Bfield']
        labelstring = 'DMD'
        color = 'b'
    elif dmd_flag==2:
        plt.subplot(3,1,2)
        reconstr = dict['sparse_Bfield']
        labelstring = 'sparse DMD'
        color = 'r'
    elif dmd_flag==3:
        plt.subplot(3,1,3)
        reconstr = dict['optimized_Bfield']
        labelstring = 'optimized DMD'
        color = 'g'
        plt.xlabel('Time (ms)',fontsize=fs)

    if dict['use_IMP']:
        plt.plot(time, \
            data[imp_index+inj_index,:]*1e4,'k',linewidth=3)
        plt.plot(time[:tsize-1], \
            reconstr[imp_index+inj_index,:tsize-1]*1e4,color,\
            label=labelstring+' reconstruction',linewidth=3) #, \
            #path_effects=[pe.Stroke(linewidth=lw+4,foreground='k'), \
            #pe.Normal()])
        plt.grid(True)
        ax = plt.gca()
        ax.tick_params(axis='both', which='major', labelsize=ts)
        ax.tick_params(axis='both', which='minor', labelsize=ts)
        plt.legend(edgecolor='k',facecolor='lightgrey',fontsize=ls,loc='upper left')
        plt.ylabel('B (G)',fontsize=fs)
        plt.savefig(out_dir+'reconstructions'+str(dictname[:len(dictname)-4])+'_imp.png')

## Makes (R,phi) contour plots of B_theta (poloidal B field)
# @param dict A psi-tet dictionary
# @param dmd_flag which DMD method to use
def toroidal_plot(dict,dmd_flag):
    num_IMPs = dict['num_IMPs']
    t0 = dict['t0']
    tf = dict['tf']
    time = dict['sp_time'][t0:tf]*1000.0
    tsize = len(time)
    tstep = 500
    if dmd_flag == 3:
        tstep = 1
    FPS = 4
    offset = 2
    if dict['is_HITSI3']:
        offset = 3
    bpol_size = np.shape(dict['sp_Bpol'])[0]
    btor_size = np.shape(dict['sp_Btor'])[0]
    bpol_imp_size = np.shape(dict['imp_Bpol'])[0]
    phis_imp = np.zeros(160*num_IMPs)
    rads_imp = np.zeros(160*num_IMPs)
    for i in range(num_IMPs):
        if num_IMPs == 8:
          phis_imp[i*160:(i+1)*160] = np.ones(160)*imp_phis8[i]
          skip = 40
        elif num_IMPs == 32:
          phis_imp[i*160:(i+1)*160] = np.ones(160)*imp_phis32[i]
          skip = 1
        else:
          print('Invalid number of IMPs, exiting')
          exit()
        rads_imp[i*160:(i+1)*160] = np.ones(160)*imp_rads
    if dmd_flag == 1:
        bpol_f0_imp = dict['Bfield_f0'] \
            [offset+bpol_size+btor_size: \
            offset+bpol_size+btor_size+bpol_imp_size,:]
        bpol_f1_imp = dict['Bfield_f1'] \
            [offset+bpol_size+btor_size: \
            offset+bpol_size+btor_size+bpol_imp_size,:]
        bpol_f2_imp = dict['Bfield_f2'] \
            [offset+bpol_size+btor_size: \
            offset+bpol_size+btor_size+bpol_imp_size,:]
        bpol_f3_imp = dict['Bfield_f3'] \
            [offset+bpol_size+btor_size: \
            offset+bpol_size+btor_size+bpol_imp_size,:]
        bpol_imp = dict['Bfield'] \
            [offset+bpol_size+btor_size: \
            offset+bpol_size+btor_size+bpol_imp_size,:]
        bpol_kink_imp = dict['Bfield_kink'] \
            [offset+bpol_size+btor_size: \
            offset+bpol_size+btor_size+bpol_imp_size,:]
    elif dmd_flag == 2:
        bpol_f0_imp = dict['sparse_Bfield_f0'] \
            [offset+bpol_size+btor_size: \
            offset+bpol_size+btor_size+bpol_imp_size,:]
        bpol_f1_imp = dict['sparse_Bfield_f1'] \
            [offset+bpol_size+btor_size: \
            offset+bpol_size+btor_size+bpol_imp_size,:]
        bpol_f2_imp = dict['sparse_Bfield_f2'] \
            [offset+bpol_size+btor_size: \
            offset+bpol_size+btor_size+bpol_imp_size,:]
        bpol_f3_imp = dict['sparse_Bfield_f3'] \
            [offset+bpol_size+btor_size: \
            offset+bpol_size+btor_size+bpol_imp_size,:]
        bpol_imp = dict['sparse_Bfield'] \
            [offset+bpol_size+btor_size: \
            offset+bpol_size+btor_size+bpol_imp_size,:]
        bpol_kink_imp = dict['sparse_Bfield_kink'] \
            [offset+bpol_size+btor_size: \
            offset+bpol_size+btor_size+bpol_imp_size,:]
    elif dmd_flag == 3:
        bpol_f0_imp = dict['optimized_Bfield_f0'] \
            [offset+bpol_size+btor_size: \
            offset+bpol_size+btor_size+bpol_imp_size,:]
        bpol_f1_imp = dict['optimized_Bfield_f1'] \
            [offset+bpol_size+btor_size: \
            offset+bpol_size+btor_size+bpol_imp_size,:]
        bpol_f2_imp = dict['optimized_Bfield_f2'] \
            [offset+bpol_size+btor_size: \
            offset+bpol_size+btor_size+bpol_imp_size,:]
        bpol_f3_imp = dict['optimized_Bfield_f3'] \
            [offset+bpol_size+btor_size: \
            offset+bpol_size+btor_size+bpol_imp_size,:]
        bpol_imp = dict['optimized_Bfield'] \
            [offset+bpol_size+btor_size: \
            offset+bpol_size+btor_size+bpol_imp_size,:]
        bpol_kink_imp = dict['optimized_Bfield_kink'] \
            [offset+bpol_size+btor_size: \
            offset+bpol_size+btor_size+bpol_imp_size,:]

    movie_bpol = np.vstack((bpol_imp,bpol_imp))
    movie_bpol = np.vstack((movie_bpol,bpol_imp))
    fig = plt.figure(figsize=(figx, figy))
    rimp = rads_imp[::skip]
    pimp = phis_imp[::skip]
    if num_IMPs==8:
        bindices = slice(0,29,4)
        indices = list(range(0,32))
        del indices[bindices]
        rimp = rimp[indices]
        pimp = pimp[indices]
    rorig = np.ravel([rimp, rimp, rimp])
    phiorig = np.ravel([pimp-2*pi, pimp, pimp+2*pi])
    midplanePhi = np.linspace(-2*pi,4*pi,len(imp_rads)*3)
    midplaneR, midplanePhi = np.meshgrid(imp_rads,midplanePhi)
    moviename = out_dir+'toroidal_Rphi_reconstruction.mp4'
    ani = animation.FuncAnimation( \
        fig, update_tor_Rphi, range(0,tsize,tstep), \
        fargs=(movie_bpol,midplaneR,midplanePhi, \
        rorig,phiorig,time),repeat=False, \
        interval=100, blit=False)
    ani.save(moviename,fps=FPS)
    update_tor_Rphi(tstep,movie_bpol,midplaneR,midplanePhi,rorig,phiorig,time)
    plt.savefig(out_dir+'contour.eps')
    plt.savefig(out_dir+'contour.pdf')

    bpol_imp = bpol_imp - bpol_f1_imp - bpol_f0_imp
    movie_bpol = np.vstack((bpol_imp,bpol_imp))
    movie_bpol = np.vstack((movie_bpol,bpol_imp))
    moviename = out_dir+'toroidal_Rphi_subtracted_reconstruction.mp4'
    ani = animation.FuncAnimation( \
        fig, update_tor_Rphi, range(0,tsize,tstep), \
        fargs=(movie_bpol,midplaneR,midplanePhi, \
        rorig,phiorig,time),repeat=False, \
        interval=100, blit=False)
    ani.save(moviename,fps=FPS)
    update_tor_Rphi(tstep,movie_bpol,midplaneR,midplanePhi,rorig,phiorig,time)
    plt.savefig(out_dir+'contour_subtracted.eps')
    plt.savefig(out_dir+'contour_subtracted.pdf')

    bpol_imp = bpol_kink_imp
    movie_bpol = np.vstack((bpol_imp,bpol_imp))
    movie_bpol = np.vstack((movie_bpol,bpol_imp))
    moviename = out_dir+'toroidal_Rphi_kink_reconstruction.mp4'
    ani = animation.FuncAnimation( \
       fig, update_tor_Rphi, range(0,tsize,tstep), \
       fargs=(movie_bpol,midplaneR,midplanePhi, \
       rorig,phiorig,time),repeat=False, \
       interval=100, blit=False)
    ani.save(moviename,fps=FPS)
    update_tor_Rphi(tsize-2,movie_bpol,midplaneR,midplanePhi,rorig,phiorig,time)
    plt.savefig(out_dir+'contour_kink.eps')
    plt.savefig(out_dir+'contour_kink.pdf')

    #bpol_imp = bpol_kink_imp
    #movie_bpol = np.vstack((bpol_imp,bpol_imp))
    #movie_bpol = np.vstack((movie_bpol,bpol_imp))
    #midplaneR, midplanePhi = np.meshgrid(imp_rads[60:120],midplanePhi)
    #moviename = out_dir+'toroidal_Rphi_kink_zoomed_reconstruction.mp4'
    #ani = animation.FuncAnimation( \
    #   fig, update_tor_Rphi, range(0,tsize,tstep), \
    #   fargs=(movie_bpol,midplaneR,midplanePhi, \
    #   rorig,phiorig,time),repeat=False, \
    #   interval=100, blit=False)
    #ani.save(moviename,fps=FPS)

    bpol_imp = bpol_f0_imp
    movie_bpol = np.vstack((bpol_imp,bpol_imp))
    movie_bpol = np.vstack((movie_bpol,bpol_imp))
    moviename = out_dir+'toroidal_Rphi_f0_reconstruction.mp4'
    ani = animation.FuncAnimation( \
        fig, update_tor_Rphi, range(0,tsize,tstep), \
        fargs=(movie_bpol,midplaneR,midplanePhi, \
        rorig,phiorig,time),repeat=False, \
        interval=100, blit=False)
    ani.save(moviename,fps=FPS)
    update_tor_Rphi(tstep,movie_bpol,midplaneR,midplanePhi,rorig,phiorig,time)
    plt.savefig(out_dir+'contour_f0.eps')
    plt.savefig(out_dir+'contour_f0.pdf')

    bpol_imp = bpol_f1_imp
    movie_bpol = np.vstack((bpol_imp,bpol_imp))
    movie_bpol = np.vstack((movie_bpol,bpol_imp))
    moviename = out_dir+'toroidal_Rphi_f1_reconstruction.mp4'
    ani = animation.FuncAnimation( \
        fig, update_tor_Rphi, range(0,tsize,tstep), \
        fargs=(movie_bpol,midplaneR,midplanePhi, \
        rorig,phiorig,time),repeat=False, \
        interval=100, blit=False)
    ani.save(moviename,fps=FPS)
    update_tor_Rphi(tstep,movie_bpol,midplaneR,midplanePhi,rorig,phiorig,time)
    plt.savefig(out_dir+'contour_f1.eps')
    plt.savefig(out_dir+'contour_f1.pdf')

    bpol_imp = bpol_f2_imp
    movie_bpol = np.vstack((bpol_imp,bpol_imp))
    movie_bpol = np.vstack((movie_bpol,bpol_imp))
    moviename = out_dir+'toroidal_Rphi_f2_reconstruction.mp4'
    ani = animation.FuncAnimation( \
        fig, update_tor_Rphi, range(0,tsize,tstep), \
        fargs=(movie_bpol,midplaneR,midplanePhi, \
        rorig,phiorig,time),repeat=False, \
        interval=100, blit=False)
    ani.save(moviename,fps=FPS)
    update_tor_Rphi(tstep,movie_bpol,midplaneR,midplanePhi,rorig,phiorig,time)
    plt.savefig(out_dir+'contour_f2.eps')
    plt.savefig(out_dir+'contour_f2.pdf')

    bpol_imp = bpol_f3_imp
    movie_bpol = np.vstack((bpol_imp,bpol_imp))
    movie_bpol = np.vstack((movie_bpol,bpol_imp))
    moviename = out_dir+'toroidal_Rphi_f3_reconstruction.mp4'
    ani = animation.FuncAnimation( \
        fig, update_tor_Rphi, range(0,tsize,tstep), \
        fargs=(movie_bpol,midplaneR,midplanePhi, \
        rorig,phiorig,time),repeat=False, \
        interval=100, blit=False)
    ani.save(moviename,fps=FPS)
    update_tor_Rphi(tstep,movie_bpol,midplaneR,midplanePhi,rorig,phiorig,time)
    plt.savefig(out_dir+'contour_f3.eps')
    plt.savefig(out_dir+'contour_f3.pdf')
    update_tor_Rphi(tstep+5,movie_bpol,midplaneR,midplanePhi,rorig,phiorig,time)
    plt.savefig(out_dir+'contour_f3_1.eps')
    plt.savefig(out_dir+'contour_f3_1.pdf')
    update_tor_Rphi(tstep+10,movie_bpol,midplaneR,midplanePhi,rorig,phiorig,time)
    plt.savefig(out_dir+'contour_f3_2.eps')
    plt.savefig(out_dir+'contour_f3_2.pdf')
    update_tor_Rphi(tstep+15,movie_bpol,midplaneR,midplanePhi,rorig,phiorig,time)
    plt.savefig(out_dir+'contour_f3_3.eps')
    plt.savefig(out_dir+'contour_f3_3.pdf')

## Update function for FuncAnimation object
## for the (R,phi) contour plots
# @param frame A movie frame number
# @param Bpol Poloidal B in the plane
# @param midplaneR Radial coordinates where we interpolate
# @param midplanePhi Toroidal coordinates where we interpolate
# @param R Radial coordinates of the probes
# @param phi Toroidal coordinates of the probes
# @param time Array of times
def update_tor_Rphi(frame,Bpol,midplaneR,midplanePhi,R,phi,time):
    print(frame)
    plt.clf()
    #plt.xlabel('R (m)',fontsize=fs+10)
    #h = plt.ylabel(r'$\phi$',fontsize=fs+10)
    #h.set_rotation(0)
    #plt.title('Time = '+'{0:.3f}'.format(time[frame])+' ms',fontsize=fs)
    ax = plt.gca()
    # plot the probe locations
    #plt.plot(R, phi,'ko',markersize=5,label='Probes')
    #plt.plot([(1.0+0.625)/2.0,(1.0+0.625)/2.0], \
    #    [pi/8.0,pi+pi/8.0],'co',markersize=ms+8, \
    #    markeredgecolor='k',label='X Injector Mouths')
    #plt.plot([(1.0+0.625)/2.0,(1.0+0.625)/2.0], \
    #    [pi/2.0+pi/8.0,3*pi/2.0+pi/8.0],'yo', \
    #    markersize=ms+8,markeredgecolor='k',label='Y Injector Mouths')
    #ax.set_yticks([])
    ax.set_yticks([0,pi/2,pi,3*pi/2,2*pi])
    ax.set_yticklabels(['','',r'$\pi$','',r'$2\pi$'])
    ax.tick_params(axis='x', which='major', labelsize=fs+30)
    ax.tick_params(axis='x', which='minor', labelsize=fs+30)
    ax.tick_params(axis='y', which='major', labelsize=fs+30)
    ax.tick_params(axis='y', which='minor', labelsize=fs+30)
    Bpol_frame = Bpol[:,frame]
    grid_bpol = np.asarray( \
        griddata((R,phi),Bpol_frame,(midplaneR,midplanePhi),'cubic'))
    v = np.logspace(-3,0,10)
    v = np.ravel([-np.flip(v),v])
    grid_bpol = grid_bpol/np.max(np.max(abs(np.nan_to_num(grid_bpol))))
    contour = plt.contourf(midplaneR,midplanePhi, \
        grid_bpol,v,cmap=colormap,label=r'$B_\theta$', \
        norm=colors.SymLogNorm(linthresh=1e-3,linscale=1e-3))
    #cbar = plt.colorbar(ticks=v,extend='both')
    #cbar.ax.tick_params(labelsize=ts)
    #cbar.ax.set_yticks([-1, -0.1, -0.01, -0.001, \
    #    0.001,0.01,0.1,1])
    #cbar.ax.set_yticklabels(['-1', '-0.1', '-0.01', '-0.001', \
    #    '0.001','0.01','0.1','1'])
    #ax.set_xticks([])
    ax.set_xticks([0,0.25,0.5,0.75,1.0,1.25])
    ax.set_xticklabels(['0','','0.5','','1',''])
    #ax.fill_between([1.052,1.2849],0,2*pi,facecolor='lightgrey')
    #ax.fill_between([0.0,0.368],0,2*pi,facecolor='lightgrey')
    #ax.set_xticks([0.37,0.7,1.05])
    #ax.set_xticklabels([0.37,0.7,1.05])
    #plt.legend(edgecolor='k',facecolor='gainsboro',fontsize=50,loc='lower left',
    #    framealpha=1.0)
    plt.ylim((0,2*pi))
    plt.xlim(0,1.2849)
    #plt.xlim(0.3678,1.052)
    #plt.xlim(imp_rads[60],imp_rads[119])
