import socket
import constants as C
import time as t
from contextlib import contextmanager
import os

@contextmanager
def create_server_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, C.SENDBUF)
    server_socket.bind((C.HOST, C.PORT))
    server_socket.listen(1)
    yield server_socket
    server_socket.close()



class Socket_Sender_Host:
    _server_socket = None
    _conn = None
    _client_addr = None
    _ctr = 0
    # def __init__(self):
    #     self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #allow reuse of local addrs
    #     self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1) #keepalive
    #     self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, C.SENDBUF) #set sendbuf size
    #     self._server_socket.bind((C.HOST, C.PORT))
    #     if (C.SOCKET_DEBUG): print(f"{C.HOST}, {C.PORT}: Listening")
    #     listen_start = t.perf_counter()
    #     self._server_socket.listen(1) #restrict to 1 connection
    #     self._conn, self._client_addr = self._server_socket.accept()
    #     if (C.SOCKET_DEBUG): print(f"Client({self._client_addr}) Connected to Host ({t.perf_counter() - listen_start}s)")


    def __init__(self):
            waitForSockets()
            with create_server_socket() as self._server_socket:
                if C.SOCKET_DEBUG:
                    print(f"{C.HOST}, {C.PORT}: Listening")
                listen_start = t.perf_counter()
                self._conn, self._client_addr = self._server_socket.accept()
                if C.SOCKET_DEBUG:
                    print(f"Client({self._client_addr}) Connected to Host ({t.perf_counter() - listen_start}s)")



    def send_robot_rel_tag_data(self, data_dict):
        if self._conn is not None:
            data_string = f"^0,{data_dict['ID']},{data_dict['x']:.3f},{data_dict['z']:.3f},0,{(t.perf_counter()-data_dict['capture_time'])*1000:.0f},{self._ctr}$"
            self._ctr+=1
            if (C.SOCKET_DEBUG): print(data_string)
            data_bytes = bytes(data_string, 'utf-8')
            try:#camid,tagid,x,y,0,age,uniqeid
                self._conn.sendall(data_bytes)
                return True
            except Exception as e:
                self._server_socket.close()
                print(f"SOCKET SEND ERR: {e}")
        return False

        


def waitForSockets():
    while(os.system("ping -c 1 " + C.RIOHOST) != 0):
        print("cant ping rio, retrying")
        t.sleep(1)



