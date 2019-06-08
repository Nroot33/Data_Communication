import socket 
import os
import time as t
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(('',6000))

host = '192.168.230.128' 
port=6000 

name = input("Input your file name : ")

total_size = os.path.getsize(name)
print("File Transmit Start") 

s.sendto(name.encode(),(host,int(port)))
s.sendto(str(total_size).encode(),(host,int(port)))

current_size = 0

with open(name, 'rb') as send_file: 
    for r in range(0,total_size,1024):
        current_size += 1024
        line = send_file.read(1024)
        t.sleep(0.2)
        s.sendto(line,(host,int(port)))
        percent = current_size/total_size*100;
        if(percent > 100):
            current_size = total_size
            percent = 100.0
        print("current_size / total_size : " , current_size, "/" , total_size , percent,"%")

