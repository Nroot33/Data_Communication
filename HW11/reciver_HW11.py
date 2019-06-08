import socket 
import os
import struct
import time as t
import sys

 # checksum 계산
def calc_checksum(string,header_checksum):
    sum = 0
    for i in range(len(string)):
        sum = sum + string[i]
    temp = sum >> 16
    chs = sum + temp + header_checksum #byte형 
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

## GoBackN ##
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(('',6000))

header_frame, addr = s.recvfrom(1080)
start = t.time()

print("Reciver Socket open...")
print("Sender IP : ", addr[0] )
print("Sender Port : ",addr[1] )

file_type = chr(header_frame[0])
header_checksum = int.from_bytes(header_frame[1:21],byteorder = "big")
file_size = int.from_bytes(header_frame[21:41],byteorder = "big")
file_name = header_frame[41:56]
file_name = file_name[0:file_name.find(32)].decode()
header_payload = header_frame[56:]
print("File Name = ", file_name)
print("File Size = ", file_size)
check_frame = file_type.encode()+file_size.to_bytes(20,byteorder = "big")+file_name.encode().ljust(15)+header_payload
check_sum = calc_checksum(check_frame,header_checksum)
current_length = 0
ACK = "head"
pre_payload_seqnum = 0
while (1) :
    if(check_sum == 0):
        with open(file_name, 'wb') as file :
            file.write(header_payload)
            current_length += 1024
            calc_percent(current_length,file_size)
            s.sendto(ACK.encode(),addr)
            while (1) :
                payload_frame,addr = s.recvfrom(1080)
                payload_type = chr(payload_frame[0])
                payload_checksum = int.from_bytes(payload_frame[1:21],byteorder = "big")
                payload_current_length = int.from_bytes(payload_frame[21:41],byteorder = "big")
                payload_seqnum = payload_frame[41:56]
                payload_seqnum = payload_seqnum[0:payload_seqnum.find(32)].decode()
                payload = payload_frame[56:]
                check_frame = payload_type.encode()+payload_current_length.to_bytes(20,byteorder = "big")+payload_seqnum.encode().ljust(15)+payload
                check_sum = calc_checksum(check_frame,payload_checksum)

                if(check_sum == 0):
                    file.write(payload)
                    current_length += 1024
                    ACK = (int(payload_seqnum)+1) % 8
                    ACK = ACK.to_bytes(4,byteorder = "big")
                    calc_percent(current_length,file_size)
                    t.sleep(1)
                    s.sendto(ACK,addr)
                    #print("Send to ACK ",int.from_bytes(ACK,byteorder="big"))




