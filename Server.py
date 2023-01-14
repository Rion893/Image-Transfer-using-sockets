import socket
from os import listdir
from re import findall
from utility import wait_for_acknowledge

"""Global Var"""
buff_size = 1024
fileList = [file for file in listdir() if findall(r'.jpg',file) != []] 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_addr = (socket.gethostname(), 2019) 
s.bind(server_addr)
s.listen(5)

client, address = s.accept()
print(f"Connection from {address} has been established!")

print("Server sending command: \"Start sending image.\"")
client.sendall(bytes("Start sending image." ,"utf-8"))

print("Server is now waiting for acknowledge from client.")
ack_from_client = wait_for_acknowledge(client,"ACK")
if ack_from_client != "ACK":
    raise ValueError('Client does not acknowledge command.')
imgCount = len(fileList)
print("Server sends the number of images to be transfered client.")
client.sendall(bytes(str(imgCount) ,"utf-8"))

print("Server is now waiting for acknowledge from client.")
ack_from_client = wait_for_acknowledge(client,"ACK")
if ack_from_client != "ACK":
    raise ValueError('Client does not acknowledge img count.')
    

print("Server will now send the images.",end='')
for file in fileList:
    
    img = open(file, 'rb')
    b_img = img.read()
    imgsize = len(b_img)        
    client.sendall(bytes(str(imgsize) ,"utf-8"))
    print(f"\t sending image {file} size of {imgsize}B.")
    
    print("Server is now waiting for acknowledge from client.")
    ack_from_client = wait_for_acknowledge(client,"ACK")
    if ack_from_client != "ACK":
        raise ValueError('Client does not acknowledge img size.')
    client.sendall(b_img)
    img.close()
    print(f"Image {file} sent!")
    
    print("Server is now waiting for acknowledge from client.")
    ack_from_client = wait_for_acknowledge(client,"ACK")
    if ack_from_client != "ACK":
        raise ValueError('Client does not acknowledge image transfer completion.')
print("All images sent.\nClosing connection.")
client.close()
