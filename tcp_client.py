import socket, sys

SERVER_IP = "127.0.0.1"   # same PC → localhost
SERVER_PORT = 9998

def main():
    msg = " ".join(sys.argv[1:]) or input("Enter message: ")
    with socket.create_connection((SERVER_IP, SERVER_PORT)) as s:
        s.sendall(msg.encode())
        data = s.recv(4096)
        print("[TCP-CLIENT] Echoed:", data.decode(errors="ignore"))

if __name__ == "__main__":
    main()
