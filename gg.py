
# import socket
#
# client = socket.socket()
# client.connect(('10.10.17.219',9999))
#
# while True:
#     msg = input(">>:").strip()  # strip方法是去掉两头的空格或者指定字符串
#     if len(msg) == 0:continue  # 这里不能send空（输入时直接回车），不然客户端就会卡住，所以要加一个判断
#     client.send(msg.encode())  # encode转换为byte，如果是单纯的字符串，前面加b
#     data = client.recv(1024456)
#     print('recv:',data.decode())  # decode与encode相反

# data_list = b'$@\x00\x00\x00\xf4\x02{"msgId":"4356c3d59e284ccc8816e9789fecb627","cmd":"UPDATE_IDLE_SHOW","sign":"4ebb50a16dd61076a17c4bc7aa21345e","data":"{\\"screen\\":\\"2KSQ9ZMB\xe5\x85\xa5\xe5\x8f\xa320200116100318200\\\\\\\\%T\\\\\\\\\\\\\\\\\\",\\"displayViewModel\\":0}","ts":"20200417145851","ver":"V1.0.0"}'
# data= data_list.split(b'$@')[1]
#
# print((data[4:5][0]))
# request_type = int(hex(data[4:5][0]), 16)
# print(request_type)
# # print('解析消息：{}'.format(str(data[7:data_len])))
# recv_msg = str(data[5:int(len(data))], encoding="utf-8")
# print(recv_msg)
statusStr = "有车"

diciCode = statusStr if statusStr == '无车' else ""
print(diciCode)