from socket import socket,AF_INET,SOCK_STREAM,SOL_SOCKET,SO_REUSEADDR
from io import StringIO
from typing import Dict,Callable,Tuple
from json import loads
from traceback import format_exc,print_exc
from os import system

CONTENT_LENGTH='Content-Length'
HTTP_CODES={200:'OK',404:'NOT_FOUND',500:'SERVER_ERROR'}

def run(port:int,commands:Dict[Tuple[str,str],Callable]):
    server = socket(AF_INET, SOCK_STREAM)
    try:
        server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        try:
            server.bind(('0.0.0.0', port))
        except OSError:
            print_exc()
            system('echo "maker" | sudo -S fuser -k 55555/tcp')
            server.bind(('0.0.0.0', port))
        server.listen(1)
        while True:
            client, address = server.accept()
            data = client.recv(1024).decode()
            stream = StringIO(data)
            line = stream.readline()
            method = line.split(' ')[0]
            path = line.split(' ')[1]
            print(method,path)
            headers = {}
            extra = {}
            while True:
                line = stream.readline().strip()
                if line == '':
                    break
                headers[line.split(' ')[0][:-1]] = line.split(' ')[1]
            if CONTENT_LENGTH in headers:
                length = int(headers[CONTENT_LENGTH])
                extra=stream.read()
                while len(extra)<length:
                    buff_size=min(length-len(extra),1024)
                    extra+=client.recv(buff_size).decode()
                print(extra)
                print('RECEIVED:',len(extra),'/',length)
                extra = loads(extra)
            try:
                result = commands[(path, method)](**extra)
                code = 200
            except KeyError:
                result = 'Command {} not found'.format((path, method))
                code = 404
            except HttpCode as e:
                result=str(e)
                code=e.code
            except Exception:
                result = format_exc()
                print_exc()
                code = 500
            pieces = ['HTTP/1.0 {} {}'.format(code, HTTP_CODES[code]),
                      'Content-Type: text/html; charset=utf-8',
                      'Content-Length: {}'.format(len(result)),
                      '',
                      result]
            send = ''
            first = True
            for piece in pieces:
                if first:
                    first = False
                else:
                    send += '\r\n'
                print(piece)
                send += piece
            client.send(send.encode())
    except (KeyboardInterrupt,OSError):
        print_exc()
        server.close()

class HttpCode(Exception):
    def __init__(self,code:int,message:str):
        super(HttpCode, self).__init__(message)
        self.code=code
