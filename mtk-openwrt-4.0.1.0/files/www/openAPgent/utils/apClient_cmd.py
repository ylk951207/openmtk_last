import sys
import socket
import time

APCLIENT_CMD_PORT=8010

method=sys.argv[1]

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('localhost', APCLIENT_CMD_PORT))
clientsocket.send(method + ' test body')
time.sleep(1)
clientsocket.close
