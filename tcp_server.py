import socket

SERVER_IP = "0.0.0.0"
SERVER_PORT = 9998
BUF = 4096

def handle(conn, addr):
    print(f"[TCP-SERVER] Connected: {addr}")
    try:
        while True:
            data = conn.recv(BUF)
            if not data:
                break
            print(f"[TCP-SERVER] From {addr}: {data!r}")
            conn.sendall(data)
    finally:
        conn.close()
        print(f"[TCP-SERVER] Closed {addr}")

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((SERVER_IP, SERVER_PORT))
    s.listen(5)
    print(f"[TCP-SERVER] Listening on {SERVER_IP}:{SERVER_PORT}")
    while True:
        conn, addr = s.accept()
        handle(conn, addr)

if __name__ == "__main__":
    main()
