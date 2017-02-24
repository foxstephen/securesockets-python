import socket, ssl, pprint, sys


class Client(object):
    def __init__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._ssl_socket = ssl.wrap_socket(
            sock=self._socket,
            ca_certs="cert.pem",
            cert_reqs=ssl.CERT_REQUIRED)


    def connect(self, host, port):
        self._ssl_socket.connect((host, port))

    
    def write(self, data):
        self._ssl_socket.write(data)

    
    def read(self):
        return self._ssl_socket.read()
    

    def close(self):
        self._ssl_socket.close()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage: python client.py [-p, --port [0..65536]] ")
        sys.exit(1)

    port_args = sys.argv[1:3]
    if '-p' not in port_args and '--port' not in port_args:
        print("Usage: python client.py [-p, --port [0..65536]] ")
        sys.exit(1)

    client = Client()
    client.connect(host="localhost", port=(int(port_args[1])))
    while True:
        print(client.read().decode("utf-8"))