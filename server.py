import socket, ssl, threading, sys


class Server(object):
    def __init__(self, host, port):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind((host, port))
        self._socket.listen(5)
        self._clients = []
        self._threads = []
        self._messages = {}


    def listen(self):
        """
            Start the server listening to new connections and 
            handle message input from stdin.
        """
        # handle client connections on another thread.
        client_handler_thread = threading.Thread(
            target=self._client_handler_loop
        )
        client_handler_thread.start()
        self._stdin_loop()
    

    def _handle_client(self, client_socket):
        """
            Handles new client connections.
        """
        connstream = ssl.wrap_socket(
            sock=client_socket,
            server_side=True,
            certfile="cert.pem",
            keyfile="key.pem"
        )
        self._clients.append(connstream)
        thread = threading.Thread(
            target=self._client_run_loop, 
            args=((connstream, ))
        )
        self._threads.append(thread)
        thread.start()


    def _client_handler_loop(self):
        """
            Loops waiting for client connections.
        """
        while True:
            client_socket, addr = self._socket.accept()
            print("New connection from: %s:%s" % (addr[0], addr[1]))
            self._handle_client(client_socket)
        

    def _client_run_loop(self, connstream):
        """
            SSL connetion loop for each client, which waits for messages.
        """
        while True:
            try:
                message = self._messages.pop(threading.current_thread().name)
                connstream.write(bytes(message, "UTF-8"))
            except KeyError:
                pass
            except BrokenPipeError:
                self._clients.remove(connstream) # remove client ref
                self._threads.remove(threading.current_thread()) # remove thread ref
                break # break from this loop so thread stops running
            


    def _stdin_loop(self):
        """
            Loops waiting for messages from stdin.
        """
        while True:
            message = input("Send message to clients:")
            # add message to key for each client connection
            for thread in self._threads:
                self._messages[thread.name] = message



if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage: python server.py [-p, --port [0..65536]] ")
        sys.exit(1)

    port_args = sys.argv[1:3]
    if '-p' not in port_args and '--port' not in port_args:
        print("Usage: python server.py [-p, --port [0..65536]] ")
        sys.exit(1)

    server = Server(host="localhost", port=6566)
    server.listen()