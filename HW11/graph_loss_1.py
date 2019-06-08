import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['figure.dpi']=100

M = ["100k","1Mb","10Mb","50Mb"]
stop = [42,587,904,2913]
go = [37,328,804,2137]
plt.plot(M,go,'.-',label = 'GoBackN')
plt.plot(M,stop,'o-',label = 'StopAndWait')
plt.xlabel('M Byte', fontsize=10)
plt.ylabel('Time(s)',fontsize=10)
plt.title('Packet Loss 1%',fontsize=10)
plt.legend(('GoBackN','StopAndWait'))
plt.show()
