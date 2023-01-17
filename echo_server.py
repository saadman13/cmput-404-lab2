import socket

BYTES_TO_READ = 4096

HOST = "127.0.0.1"
PORT = 8080

def handle_connection(conn, addr):
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(BYTES_TO_READ)
            if not data:
                break
            
            print(data)
            conn.sendall(data)
            #diff between sendall and send, is that send does not gurantee that al of data that has been sent
            

    

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))

        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.listen()

        conn, addr = s.accept() # conn is connection(socket directly to the client) that was made to us and addr is the address that we connected to
        handle_connection(conn, addr)

start_server()