import socket
import ssl

HOST = "127.0.0.1"
PORT = 4443
CAFILE = "server.crt"
BUFFER_SIZE = 1024

def main():
    msg = input("Enter a message to send (TLS): ").strip()

    if not msg:
        print("Error: message cannot be empty.")
        return

    if len(msg) > BUFFER_SIZE:
        print(f"Error: message too long (max {BUFFER_SIZE} chars).")
        return

    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations(cafile=CAFILE)
    context.check_hostname = False  # fine for localhost lab
    context.verify_mode = ssl.CERT_REQUIRED

    try:
        with socket.create_connection((HOST, PORT)) as sock:
            with context.wrap_socket(sock, server_hostname=HOST) as tls_sock:
                print("TLS established using:", tls_sock.version())
                tls_sock.sendall(msg.encode("utf-8"))

                data = tls_sock.recv(BUFFER_SIZE)
                print("Reply:", data.decode("utf-8", errors="replace"))

    except (ssl.SSLError, OSError) as e:
        print("Client error:", e)

if __name__ == "__main__":
    main()
