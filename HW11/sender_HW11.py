import socket 
import os
import struct
import sys
import time as t

 # checksum 계산
def calc_checksum(string):
    sum = 0
    for i in range(len(string)):
        sum = sum + string[i]
    temp = sum >> 16
    chs = sum + temp
    if chs >= 65536 :
        chs -= 65536
    if chs >= 131072 : 
        chs -= 131072
    chs = chs ^ 0xffff
    return chs


 # 퍼센트 계산
def calc_percent(current_length,file_size):
    percent = current_length/file_size*100
    if(current_length >= file_size):
        current_length = file_size
        percent = 100
        print("current_size / total_size : " , current_length, "/" , file_size , "=" ,round(percent),"%\n")
        print("File send end")
        end = t.time()
        print(end-start)
        sys.exit()
    print("current_size / total_size : " , current_length, "/" , file_size , "=" ,round(percent),"%\n")

 # checksum을 계산하여 payload를 만듦 
def make_payload(current_length,seq_num):
    file_type = "d"
    current_length +=1024
    b_current_length = current_length.to_bytes(20,byteorder = "big")
    b_seq_num = str(seq_num).encode().ljust(15)
    payload = file.read(1024)
    b_payload = file_type.encode()+b_current_length+b_seq_num+payload
    payload_checksum = calc_checksum(b_payload).to_bytes(20,byteorder = "big")
    payload_frame = file_type.encode()+payload_checksum+b_current_length+b_seq_num+payload
    return payload_frame


## GoBackN ##    
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.settimeout(4)

host = '192.168.230.128'
port = 6000

print("Sender Socket open...")
print("Receiver IP : ", host)
print("Receiver Port : ", port)

file_type = "s"
file_name = input("Input File name : ")
file_size = os.path.getsize(file_name)

b_file_size = file_size.to_bytes(20,byteorder = "big")
b_file_name = file_name.encode().ljust(15)
current_length = 0
seq_num = 0
window =[]
window_size = 4


with open(file_name, 'rb') as file:
    payload = file.read(1024)
    header_frame = file_type.encode()+b_file_size+b_file_name+payload
    header_checksum = calc_checksum(header_frame).to_bytes(20,byteorder = "big")
    header_frame = file_type.encode()+header_checksum+b_file_size+b_file_name+payload
    start = t.time()
    s.sendto(header_frame,(host,port))
    print("Send File Info(file_Type, Checksum, file Name, file Size, Payload ) to Server...")
    while(1) :
        try :    
            ACK, _ = s.recvfrom(1000)
            break
    
        except socket.timeout: # timeout으로 인한 재전송 요청
            print("* TimeOut!! ***")
            print("Retransmission")
            s.sendto(header_frame,(host,port))
            s.settimeout(4)
            continue

    if(ACK.decode() == "head"):
        print("Start File send")
        current_length +=1024
        calc_percent(current_length,file_size)

    for i in range(window_size):
        current_length += 1024
        payload_frame = make_payload(current_length,seq_num)
        s.sendto(payload_frame,(host,port))
        if(len(window) > 3):
            window.pop(0)
            window.append(seq_num)
            print("**** Window Change! ****")
            print("Present Window : ",window)
        else:
            window.append(seq_num)
        seq_num += 1
        seq_num = seq_num % 8
        calc_percent(current_length,file_size)

    while(1) :    
        current_length += 1024
        payload_frame = make_payload(current_length,seq_num)
        s.sendto(payload_frame,(host,port))
        if(len(window) > 3):
            window.pop(0)
            window.append(seq_num)
            print("**** Window Change! ****")
            print("Present Window : ",window)
        else:
            window.append(seq_num)
        seq_num += 1
        seq_num = seq_num % 8
        calc_percent(current_length,file_size)
        n = 1
            
        try:
            ACK,_ = s.recvfrom(1000)
            ACK = int.from_bytes(ACK,byteorder = "big")
            if(ACK == (window[0]+n)%8):
                n+=1
                if(n>4) :
                    break
                continue
    
        except socket.timeout: # timeout으로 인한 재전송 요청
            print("**** TimeOut!! ****")
            file.seek(-1024*window_size,1)
            current_length = current_length-1024*window_size
            for i in range(window_size):
                current_length += 1024
                payload_frame = make_payload(current_length,window[0+i])
                s.sendto(payload_frame,(host,port))
                calc_percent(current_length,file_size)
            continue
