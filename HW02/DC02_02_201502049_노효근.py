import socket
import struct

socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0800))

def init(x):
	result = ''
	for i in range(0,5):
		result += x[i*2:i*2+2]+":"
	result += x[10:]
	return result

while True:
	packet = socket.recvfrom(20000)
        
	ethernet_header = struct.unpack('!6s6s2s',packet[0][0:14])
	dst_ethernet_addr = init(ethernet_header[0].hex())
	src_ethernet_addr = init(ethernet_header[1].hex())
	protocol_type = "0x" + ethernet_header[2].hex()

	print("<<<<<<Packet Capture Start>>>>>>")
	print("=======ethernet_header=======")
	print("src_mac_address : ", src_ethernet_addr)
	print("dest_mac_address : ", dst_ethernet_addr)	
	print("ip_version : ", protocol_type)

	if(protocol_type=="0x0800"):
		print("=======ip_header=======")

		ip_header = struct.unpack('!1B1B1H1H1H1B1B1H', packet[0][14:26])
	
		version = ip_header[0]>>4
		print("ip_version : ", version)

		header_length = (ip_header[0]&15)<<2
		print("ip_Length : ", header_length)

		dif_ser_code = ip_header[1]//4
		print("differentiated_service_codepoint : ", dif_ser_code)
		
		ex_con_noti = ip_header[1]%4
		print("explicit_congestion_notification : ", ex_con_noti)

		ip_total_length = ip_header[2]
		print("total_length : ", ip_total_length)

		identification = ip_header[3]
		print("identification : ", identification)
	
		flag = ip_header[4]
		print("flags : ", flag)
			
		r_v = ip_header[4]//(2**15)
		print(">>>reserved_bit : ", r_v)
		
		n_f = ip_header[4]//(2**14)
		print(">>>non_fragments : ", n_f)
			
		fragments = ip_header[4]//(2**13)
		print(">>>fragments : ", fragments)

		offset = ip_header[4]&8191
		flag = flag>>13
		print(">>>fragment offset : ", offset)

		ttl = ip_header[5]
		print("Time_to_live : ", ttl)

		protocol = ip_header[6]
		print("protocol : ", protocol)

		checksum = ip_header[7]
		print("header_checksum = ", checksum)

		srcip = struct.unpack('!BBBB', packet[0][26:30])
		print("source_ip_address : ", '%d.%d.%d.%d' %(srcip))

		dstip = struct.unpack('!BBBB', packet[0][30:34])
		print("dest_iP_address : ", '%d.%d.%d.%d' %(dstip))


		n=0
		if(header_length>20):
			n = header_length-20
			opt_pad = struct.unpack('!3B1B', packet[0][34:(34+n)])

		if(protocol == 6):
#tcp 진행
			print("=======tcp_header=======")
	
		
			tcp_header = struct.unpack('!1H1H1L1L1B1B1H1H1H', packet[0][(34+n):(54+n)])
	
			tcp_srcPort = tcp_header[0]
			print("src_port : ", tcp_srcPort)
	
			tcp_dstPort = tcp_header[1]
			print("dec_port : ", tcp_dstPort)

			tcp_seqNum = tcp_header[2]
			print("seq_num : ", tcp_seqNum)

			tcp_ackNum = tcp_header[3]
			print("ack_num : ", tcp_ackNum)

			head_len = tcp_header[4]//4
			print("head_len : ", head_len)

			flags = tcp_header[4]
			print("flags : ", flags)

			tcp_reserved = (tcp_header[4]>>1)&7
			print(">>>reserved : ", tcp_reserved)

			tcp_ns = tcp_header[4]&1
			print(">>>nonce : ", tcp_ns)

			tcp_cwr = (tcp_header[5]>>7)&1
			print(">>>cwr : ", tcp_cwr)

			tcp_urg = (tcp_header[5]>>5)&1
			print(">>>urgent : ", tcp_urg)

			tcp_ack = (tcp_header[5]>>4)&1
			print(">>>ack : ", tcp_ack)
			
			tcp_psh = (tcp_header[5]>>3)&1
			print(">>>push : ", tcp_psh)

			tcp_rst = (tcp_header[5]>>2)&1
			print(">>>reset : ", tcp_rst)

			tcp_syn = (tcp_header[5] >>1)&1
			print(">>>syn : ", tcp_syn)

			tcp_fin = tcp_header[5]&1
			print(">>>fin : ", tcp_fin)

			tcp_windowsize = tcp_header[6]
			print("window_size_value : ", tcp_windowsize)

			tcp_checkSum = tcp_header[7]
			print("checksum : ", tcp_checkSum)

			tcp_urgentPointer = tcp_header[8]
			print("urgent_pointer : ", tcp_urgentPointer)


		if(protocol == 17):
#udp 진행
			print("=======udp_header=======")
			udp_header = struct.unpack('!1H1H1H1H', packet[0][(34+n):(42+n)])

			udp_srcPort = udp_header[0]
			print("src_port : ", udp_srcPort)

			udp_dstPort = udp_header[1]
			print("dest_port : ", udp_dstPort)

			udp_length = udp_header[2]
			print("leng : ", udp_length)

			udp_checksum = udp_header[3]
			print("header checkSum : ", udp_checksum)

	break


