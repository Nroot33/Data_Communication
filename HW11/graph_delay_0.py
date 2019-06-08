import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['figure.dpi']=100

M = ["100k","1Mb","10Mb","50Mb"]
stop = [17,78,709,2552]
go = [11,52,532,1834]
plt.plot(M,go,'.-',label = 'GoBackN')
plt.plot(M,stop,'o-',label = 'StopAndWait')
plt.xlabel('M Byte', fontsize=10)
plt.ylabel('Time(s)',fontsize=10)
plt.title('Packet Delay 0',fontsize=10)
plt.legend(('GoBackN','StopAndWait'))
plt.show()
