import socket
import json

IP_ADDRESS = input("Enter address to listen: ")
PORT_NO = int(input("Enter port number: "))
bufferSize = 1024

#create datagram socket
server_socket= socket.socket(family=socket.AF_INET, type = socket.SOCK_DGRAM)

#bind to address and ip
server_socket.bind((IP_ADDRESS, PORT_NO))

#continue listening

#setup client connections through dictionary format {"client_address":"alias"}
client_conns = {}

while(True):
    byte_address = server_socket.recvfrom(bufferSize)
    received_data = byte_address[0]
    received_client = byte_address[1]
    received_json = json.loads(received_data.decode("utf-8"))
    print("Received command ", received_data.decode('utf-8'), "from client \'", received_client, "\'")

    #process the received json

    #if it contains the join

    if received_json["command"] == "join":
        if received_client[0] == IP_ADDRESS and received_client[1] == PORT_NO:
            send_json = bytes(json.dumps({"command": "join"}), "utf-8")
            server_socket.sendto(send_json, received_client)
        else:
            send_json = bytes(json.dumps({"command":"error", "message":"Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number."}), "utf-8")
            server_socket.sendto(send_json, received_client)

    # if it contains the leave
    elif received_json["command"] == "leave":
        #remove registered user from the dict of clients
        username = client_conns[received_client]
        print("User ", username, " left the message board")
        del client_conns[received_client]
        command = bytes(json.dumps({"command": "leave"}), "utf-8")
        server_socket.sendto(command, received_client)
    
    #if it contains the register

    elif received_json["command"] == "register":
       
        
        alias = received_json["handle"]
         #double check if handle is already taken
        client_alias = client_conns.values()
        if alias in client_alias:
             command = bytes(json.dumps({"command":"error", "message":"Error: Registration failed. Handle or alias already exists."}), "utf-8")
             print("The handle ", alias, " is already in use")
        else:
            client_conns[received_client] = alias
            #print(client_conns) #testing
            command = bytes(json.dumps({"command": "register", "handle": client_conns[received_client]}), "utf-8")
            server_socket.sendto(command, received_client)
    elif received_json["command"] == "all":
        #find the sender's name by searching the dictionary
        sender = client_conns[received_client]
        fullline = sender + ": " + received_json["message"]
        
        #send to all clients in dictionary
        all_client_address = client_conns.keys()
        for x in all_client_address:
            #make sure that message is not sent to the sender
            if received_client != x:
                server_socket.sendto(bytes(json.dumps({"command": "all", "message": fullline}), "utf-8"), (x))