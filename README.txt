- Python version 3.6.0

- Create cert and key using the following command:
    openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes -subj /CN=localhost

- To run server
    Usage: python server.py [-p, --port [0..65536]]
    eg. python server.py -p 8080

- To run client
    Usage: python client.py [-p, --port [0..65536]]
    eg. python client.py -p 8080