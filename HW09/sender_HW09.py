import socket 
import os
import struct
import time as t

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(('',6000))

host = '192.168.100.153'
port = 6000

print("Sender Socket open...")
print("Receiver IP : ", host)
print("Receiver Port : ", port)

file_type = 0
file_name = input("Input File name : ")
file_size = os.path.getsize(file_name)
current_size = 1024
Seq_Num = 0
percent = current_size/file_size*100
stack = 0

def calc_checksum(string):
    sum = 0
    for i in range(len(string)):
        sum = sum + string[i]
    temp = sum >> 16  # mod256
    chs = sum + temp
    chs = chs ^ 0xffff  
    return chs

with open(file_name, 'rb') as send_file:
    line = send_file.read(1024)

    info = struct.pack("!1b11si1024s",file_type,file_name.encode(),file_size,line)
    chs = calc_checksum(info)
    info = struct.pack("!20s1b11si1024s",bytes(chs),file_type,file_name.encode(),file_size,line)
    s.sendto(info,(host,int(port)))

    print("Send File Info(file Name,file Size, seqNum) to Server...")

    ACK, _ = s.recvfrom(2000)
    if(ACK.decode() == "1"):
        print("Start File send")
        percent = current_size/file_size*100
        print("current_size / total_size : " , current_size, "/" , file_size , percent,"%")
    
    while (1) :
        stack += 1

        t.sleep(0.5)
        line = send_file.read(1024)
        
        line_info = struct.pack("!1b1024s",Seq_Num,line)
        chs = calc_checksum(line_info)
        line_info = struct.pack("!20s1b1024s", bytes(chs),Seq_Num,line)
        s.sendto(line_info,(host,int(port)))
        
        current_size += 1024
        percent = current_size/file_size*100
        if(percent > 100):
            current_size = file_size
            percent = 100.0
        print("current_size / total_size : " , current_size, "/" , file_size , percent,"%")

        if(percent == 100.0):
            print("File send end")
            break
        ACK, _ = s.recvfrom(2000)

        if(ACK.decode() == "wait"):
            print("---------Time_Out!---------")
            print("Retransmit")
            current_size -= 1024
            continue

        if(ACK.decode() == "2"):
            print("Retransmit")
            current_size -=1024
            if(Seq_Num == 1):
                Seq_Num = 0
                continue
            if(Seq_Num == 0):
                Seq_Num = 1
                continue

        elif(ACK.decode() == "NAK"):
            print("Retransmit")
            current_size -= 1024
            continue

        if(ACK.decode() == "1"):
            if(stack == 7):
                continue
            if(Seq_Num == 1):
                Seq_Num = 0
                continue
            if(Seq_Num == 0):
                Seq_Num = 1
                continue



        
            
            
        

