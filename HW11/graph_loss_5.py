import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['figure.dpi']=100

M = ["100k","1Mb","10Mb","50Mb"]
stop = [174,974,1326,3604]
go = [78,748,1511,3087]
plt.plot(M,go,'.-',label = 'GoBackN')
plt.plot(M,stop,'o-',label = 'StopAndWait')
plt.xlabel('M Byte', fontsize=10)
plt.ylabel('Time(s)',fontsize=10)
plt.title('Packet Loss 5%',fontsize=10)
plt.legend(('GoBackN','StopAndWait'))
plt.show()
