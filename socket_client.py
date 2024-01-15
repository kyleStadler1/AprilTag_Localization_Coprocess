import socket
import constants as C

def main():
    # Server address and port
    server_address = ('stadlerpi.local', C.PORT)

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect(server_address)
        print(f"Connected to {server_address}")

        while True:
            # Receive data from the server
            data = client_socket.recv(1024)

            # Check if the connection is closed by the server
            if not data:
                print("Connection closed by the server.")
                break

            # Decode the received byte string
            message = data.decode('utf-8')
            poses = message.split('$')
            for pose in poses:
                if len(pose) > 0:
                    print(pose[1:])

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the socket
        client_socket.close()
        print("Socket closed.")

if __name__ == "__main__":
    main()