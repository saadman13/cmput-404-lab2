import socket
from threading import Thread 

#proxy server accepts request and relays it to some other server (proxy target) and then relays the resposne from the proxy target back to 
#the server(proxy client) that actually made that request 
BYTES_TO_READ = 4096
PROXY_SERVER_HOST = "127.0.0.1"
PROXY_SERVER_PORT = 8080

def send_request(host, port, request_data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        
        #sending data to host
        client_socket.connect((host, port))
        client_socket.send(request_data)
        client_socket.shutdown(socket.SHUT_WR) # shut down socket but not entirely ( so we are not going to 
        #send anything back to google. Everything we wanted to send we already did)

        #getting response from host
      
        data = client_socket.recv(BYTES_TO_READ)
        result = b'' + data
        while(len(data) > 0):
            data = client_socket.recv(BYTES_TO_READ)
            result += data
            
        return result

def handle_connection(conn, addr):
    with conn:
        print(f"Connected by {addr}")
        request = b""
        while True:
            data = conn.recv(BYTES_TO_READ)
            if not data:
                break
            
            print(data)
            request += data

        response = send_request(PROXY_SERVER_HOST, PROXY_SERVER_PORT, data)
        conn.sendall(reponse)

def start_server():
     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))

        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.listen(2) # parameter tells our program how many queue we can have. 

        conn, addr = server_socket.accept() # conn is connection(socket directly to the client) that was made to us and addr is the address that we connected to
        handle_connection(conn, addr)

def start_threaded_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))

        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.listen(2) # parameter tells our program how many queue we can have. 

        while True:
            conn, addr = server_socket.accept()
            thread = Thread(target=handle_connection, args=(conn, addr))
            thread.run()



#start_server()
start_threaded_server()