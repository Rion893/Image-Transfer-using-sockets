import socket
from utility import wait_for_acknowledge
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_addr = (socket.gethostname(), 2019) 
client.connect(server_addr)
print(f"Connected to server!")
client.settimeout(5) 
print("Client is now waiting for server's command.")
cmd_from_server = wait_for_acknowledge(client,"Start sending image.")
imgCount_from_server = 0
if cmd_from_server == "Start sending image.":
    print("Command \"Start sending image.\" received.")
    print("Loading ...")
    client.sendall(bytes("ACK","utf-8"))
    try:
        print("Client is now waiting for the number of images.")
        imgCount_from_server = int(wait_for_acknowledge(client,str(3)))  
        
    except:
        raise ValueError("Number of images received is buggy.")

if imgCount_from_server > 0:
    print("Number of images to receive: ",imgCount_from_server)
    print("Sending Image...")
    client.sendall(bytes("ACK","utf-8"))

print(f"Client is now receiving {imgCount_from_server} images.")



for i in range(imgCount_from_server):
    index = i+1
    file = f"./imgfromserver{index}.jpg"
    try:                                         
        f = open(file, "x")           
        f.close()
    except:
        pass
    finally:
        f = open(file, "wb")
    print(f"\tReceiving image {index}")
    imgsize = int(wait_for_acknowledge(client,str(3)))
    print(f"\tImage size of {imgsize}B received by Client")
    print("Sending Image...")
    client.sendall(bytes("ACK","utf-8"))  
    buff = client.recv(imgsize)
    f.write(buff)
    f.close()
    print(f"File {file} received!")
    print("Sending Image...")
    client.sendall(bytes("ACK","utf-8"))


print("All images received.")
print("Closing connection.")
client.close()