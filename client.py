#!/usr/bin/env python
# coding: utf-8

# In[1]:


import socket
import hashlib
import os

# define host, port and buffer size
HOST = socket.gethostname()
PORT = 5000
BUFFER_SIZE = 4096


# create socket object with Ipv4 and TCP connection
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    
         #connect to server
        client_socket.connect((HOST, PORT))
        print(f'Connected to server {HOST}:{PORT}')
           

    # get file that needs to be sent
        file_path = input("Enter the file path (without quotation marks): ")


        try:
            # open the file in binary mode
            with open(file_path, 'rb') as f:

                # calculate checksum
                md5 = hashlib.md5(f.read())
                client_checksum = md5.hexdigest()

                #send data to server using '#' as delimiter 
                data = f"{file_path}#{client_checksum}#"
                client_socket.sendall(data.encode())

                # Move file pointer to start of file
                f.seek(0)
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    try:
                        client_socket.sendall(data) 
                    except socket.error as e:
                        print(f'Error sending data: {e}')


            print('File sent successfully')

            #Exception if file path is incorrect
        except FileNotFoundError:
            print('File not found')

#Throws an exception if server is offline
except ConnectionRefusedError:
    print('Server is offline or cannot be reached')

# close connection
client_socket.close()


# In[ ]:





# In[ ]:





# In[ ]:




