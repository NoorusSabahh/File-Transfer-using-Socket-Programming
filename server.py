#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import socket
import hashlib
import os

# define host, port and buffer size
HOST = socket.gethostname()
PORT = 5000
BUFFER_SIZE = 4096

# create socket object with Ipv4 and TCP connection
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind socket to host and port number
server_socket.bind((HOST, PORT))

# listen for incoming connections
server_socket.listen(1)

print('Server listening on port ', PORT)

while True:
    # accept incoming connections
    conn, addr = server_socket.accept()
    print('Connected to: ', addr)

    try:
        # receive the file name and checksum
        
        data = conn.recv(1024).decode().split('#')
        
        if len(data) == 3:
            file_name, checksum, filedata = data
            print('Received file path:', file_name)
            print('Received checksum:', checksum)
        else:
            raise ValueError('Invalid data received')

        # create a new file with unique name if file already exists
        file_root, file_ext = os.path.splitext(file_name)
        i = 1
        while os.path.exists(file_name):
            file_name = file_root + '_' + str(i) + file_ext
            i += 1

        # checksum and file writing
        md5 = hashlib.md5()
        with open(file_name, 'wb') as f:
            while True:
                filedata = conn.recv(1024)
                
                if not filedata:
                    break
                f.write(filedata)
                md5.update(filedata)
            print('Received Data:', filedata)  #To check all data has been received

        # compare received checksum with calculated checksum
        server_checksum = md5.hexdigest()
        if server_checksum == checksum:
            print('File received successfully')
        else:
            print('Error occurred while receiving file: checksum does not match')

    except Exception as e:
        print('Error occurred while receiving file:', e)

    # close connection
    conn.close()


# In[ ]:





# In[ ]:




