import socket 
import os
import struct

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
        current_size = file_size
        percent = 100.0
        
    print("current_size / total_size : " , current_length, "/" , file_size , percent,"%")

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.settimeout(4)

host = '127.0.0.1'
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

seq_num = "1"

with open(file_name, 'rb') as file:

    payload = file.read(1024)

    header_frame = file_type.encode()+b_file_size+b_file_name+payload
    
    header_checksum = calc_checksum(header_frame).to_bytes(20,byteorder = "big")

    header_frame = file_type.encode()+header_checksum+b_file_size+b_file_name+payload

    pre_header_frame = header_frame
    
    s.sendto(header_frame,(host,port))

    print("Send File Info(file_Type, Checksum, file Name, file Size, Payload ) to Server...")

    while(1) :

        try :    
            ACK, _ = s.recvfrom(1000)
            break
    
        except socket.timeout: # timeout으로 인한 재전송 요청
            print("* TimeOut!! ***")
            print("Retransmission")
            s.sendto(pre_header_frame,(host,port))
            calc_percent(current_length,file_size)
            s.settimeout(4)
            continue

    if(ACK.decode() == "1"):
        print("Start File send")
        current_length +=1024
        calc_percent(current_length,file_size)

    
    while (1) :

        file_type = "d"

        current_length +=1024
    
        b_current_length = current_length.to_bytes(20,byteorder = "big")

        b_seq_num = seq_num.encode().ljust(15)

        payload = file.read(1024)

        pre_payload = payload

        b_payload = file_type.encode()+b_current_length+b_seq_num+payload

        payload_checksum = calc_checksum(b_payload).to_bytes(20,byteorder = "big")
        
        payload_frame = file_type.encode()+payload_checksum+b_current_length+b_seq_num+payload

        pre_payload_frame = file_type.encode()+payload_checksum+b_current_length+b_seq_num+payload
        
        s.sendto(payload_frame,(host,port))

        if(current_length >= file_size):
            calc_percent(current_length,file_size)
            print("File send end")
            break

        try:
            
            ACK,_ = s.recvfrom(1000)
        

            if(ACK.decode() == "1"):
                calc_percent(current_length,file_size)
                seq_num = "1"
                continue
        
            elif(ACK.decode() == "0"):
                calc_percent(current_length,file_size)
                seq_num = "0"
                continue

            elif(ACK.decode() == "NAK2"): #프레임 손상으로 재전송 요청 / 수신측에서 버림
                print("* Received NAK2")
                s.sendto(pre_payload_frame,(host,port))
                calc_percent(current_length,file_size)
                continue

            elif(ACK.decode() == "NAK1"): #순서가 뒤 바뀌어 재전송 요청/ 수신측에서 버림 
                print("* Received NAK1")
                s.sendto(pre_payload_frame,(host,port))
                calc_percent(current_length,file_size)
                continue
                
        except socket.timeout: # timeout으로 인한 재전송 요청
            print("* TimeOut!! ***")
            print("Retransmission")
            s.sendto(pre_payload_frame,(host,port))
            calc_percent(current_length,file_size)
            s.settimeout(4)
            continue
        
                
