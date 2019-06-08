import socket 
import os
import struct
import time as t
import random as r

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(('',6000))

port = 6000

info, addr = s.recvfrom(1060)

print("Sender Socket open...")
print("Receiver IP : ", addr)
print("Receiver Port : ",port )
u_info = struct.unpack("!20s1b11s1i1024s",info)
file_name = u_info[2].decode().strip('\0')
file_size = u_info[3]
print("File Name = ", file_name)
print("File Size = ", file_size)

ACK = 1
current_size = 0
check = 1
percent = 0
stack = 0

def calc_checksum(string):
    sum = 0
    for i in range(len(string)):
        sum = sum + string[i]
    temp = sum >> 16
    chs = sum + temp
    
    if chs >= 65536
        chs -= 65536
    if chs >= 131072
        chs -= 131072    
    chs = chs ^ 0xffff

    return chs

with open(file_name, 'wb') as recive_file :

    recive_file.write(u_info[4])
    current_size += 1024
    percent = current_size/file_size*100
    if(percent > 100):
        current_size = file_size
        percent = 100.0
    print("current_size / total_size : " , current_size, "/" , file_size , percent,"%")
    s.sendto(str(ACK).encode(),(host,int(port)))

    while (1) :
        if(percent == 100.0):
            print("file receive end")
            break
        rand = r.randint(1,10)
        stack += 1
        
        if(rand == 3):
            print("Wait for 5...")
            ACK = "wait"
            t.sleep(5)
            s.sendto(str(ACK).encode(),(host,int(port)))
            continue

        
        ACK = 1
        data, _ = s.recvfrom(1045)
        u_data = struct.unpack("!20s1b1024s",data)

        chs=u_data[0]
        seq=u_data[1]
        line=u_data[2]
        
        r_chs = struct.pack("1b1024s",seq,line)
        r_chs = calc_checksum(r_chs)
        r_chs = struct.pack("20s",bytes(r_chs))

        if(stack == 5 ):
            r_chs = r_chs+bytes(2)
            
        if(chs == 0):
            if(u_data[1] == check):
                print("* Packet corrupted!! *** - Send To Sender NAK(2)")
                ACK = "2"
                s.sendto(str(ACK).encode(),(host,int(port)))
                continue
            else:
                recive_file.write(line)
                current_size += 1024
                percent = current_size/file_size*100
                if(percent > 100):
                    current_size = file_size
                    percent = 100.0
                print("current_size / total_size : " , current_size, "/" , file_size , percent,"%")

                check = u_data[1]

            # ACK 보내기
                s.sendto(str(ACK).encode(),(host,int(port)))
                if(current_size > file_size ):
                    print("file receive end")
                    break
        else:
            print("*Received NAK - Retransmit!")
            ACK = "NAK"
            s.sendto(str(ACK).encode(),(host,int(port)))
            continue
            



            
