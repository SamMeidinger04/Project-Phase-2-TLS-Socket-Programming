import socket
import ssl

HOST = "127.0.0.1"
PORT = 4443
CERT_FILE = "server.crt"
KEY_FILE = "server.key"
BUFFER_SIZE = 1024

def handle_client(conn):
    try:
        data = conn.recv(BUFFER_SIZE)
        if not data:
            conn.sendall(b"Server: no data received.")
            return

        message = data.decode("utf-8", errors="ignore").strip()
        if not message:
            conn.sendall(b"Server: empty message rejected.")
            return

        response = f"Server received securely: {message}"
        conn.sendall(response.encode("utf-8"))

    except ssl.SSLError as e:
        print("TLS error:", e)
    finally:
        try:
            conn.shutdown(socket.SHUT_RDWR)
        except Exception:
            pass
        conn.close()

def main():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"TLS Server listening on {HOST}:{PORT}")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")

            try:
                tls_conn = context.wrap_socket(client_socket, server_side=True)
                print("TLS established using:", tls_conn.version())
                handle_client(tls_conn)
            except ssl.SSLError as e:
                print("TLS handshake failed:", e)
                client_socket.close()

if __name__ == "__main__":
    main()
