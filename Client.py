import json
import socket
import threading
import time

server_IP = ""
PORT_NO = 0
connected =  False
registered = False
join_command = {"command": "join"}
leave_command = {"command": "leave"}
register_command = {"command": "register", "handle": "handle"}
all_message_command = {"command": "all", "message": "message"}
direct_message_command = {"command": "msg", "handle": "handle", "message": "message"}
error_command = {"command": "error", "message": "message"}


client_socket= socket.socket(family=socket.AF_INET, type = socket.SOCK_DGRAM)
client_socket.settimeout(1)

def get_from_server():
    global connected, registered
    while True:
         try:
             byte_address = client_socket.recvfrom(1024)
             received_data = byte_address[0]
             received_server = byte_address[1]
             received_json = json.loads(received_data.decode("utf-8"))
         except:  #when nothing is received just continue
              continue
         else:
              if received_json["command"] == "register":
                   print("Welcome, ", received_json["handle"], "!")
                   registered = True
              if received_json["command"] == "all":
                   print(received_json["message"])
def main():
    global connected, registered
    while True:
        while connected == False: # not yet connected to server
            client_input = input()
            command = client_input[1:] # remove slash
            
            if command == "?": # help command
                 print("COMMAND LIST:")
                 print("Connect to the server application: /join <server_ip_add> <port>\nDisconnect to the server application: /leave\nRegister a unique handle or alias: /register <handle>\nSend message to all: /all <message>\nSend direct message to a single handle: /msg <handle> <message>\nRequest command help to output all Input Syntax commands for references: /?")
                 continue
           
            firstword = command.split(" ", 1)

            try:
                if firstword[0] == "join":
                    
                        fullcommand = command.split(" ")
                        server_IP= fullcommand[1]
                        PORT_NO = fullcommand[2]
                            
                        client_socket.sendto(bytes(json.dumps(join_command), "utf-8"), ( server_IP, int(PORT_NO)))
                        data, server = client_socket.recvfrom(1024)
                        data = data.decode("utf-8")
                        json_data = json.loads(data)
                        connected = True
                        print("Connection to the Message Board Server is successful!")
            except:
                print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
            
        while connected == True:
            multi_thread = threading.Thread(target=get_from_server, args=(()))
            multi_thread.start()  #continue listening for incoming message and at the same time execute codes below in case user enters a command
            input_on_chat = input()
            line = input_on_chat[1:]#remove slash
            #leave 
            if line == "leave":
                if registered == True:
                    client_socket.sendto(bytes(json.dumps(leave_command), "utf-8"), (server_IP,int(PORT_NO)))
                    time.sleep(0.2)
              
                else:
                    print("Connection closed. Thank you!")
                    connected = False
                continue

            firstline = line.split(" ", 1)
            if firstline[0] == "register":
                  alias = firstline[1]
                  register_command["handle"] = alias
                  client_socket.sendto(bytes(json.dumps(register_command), "utf-8"),(server_IP,int(PORT_NO)))
            elif firstline[0] == "all":
                 if registered == True:
                      message = firstline[1]
                      all_message_command["message"] = message
                      client_socket.sendto(bytes(json.dumps(all_message_command), "utf-8"), (server_IP,int(PORT_NO)))
                      time.sleep(0.2)
                 else:
                      print("User is not yet registered")
        client_socket.close()
              
            
                        
                    
               

if __name__ == '__main__':
    main()