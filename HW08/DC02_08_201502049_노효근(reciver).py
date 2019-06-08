import socket 
import os

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(('',6000))

name, senderaddr = s.recvfrom(2000)
total_size, _ = s.recvfrom(2000)

print("file recv start from ", senderaddr)
print("File Name : " , name.decode())
print("FIle Size : " , total_size.decode())

current_size = 0

with open(name, 'wb') as recive_file :
    for r in range(0,int(total_size),1024):
        current_size += 1024
        data, _ = s.recvfrom(1024)
        recive_file.write(data)
        percent = current_size/int(total_size)*100;
        #if(percent > 100):
            #current_size = total_size.decode()
            #percent = 100.0
        print("current_size / total_size : " , current_size, "/" , total_size.decode() , percent,"%")

