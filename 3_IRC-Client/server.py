import numpy as np
import threading
import socket
import numpy
import sys
import pickle


HOST = "localhost"
PORT = 5551
MAX_AMOUNT = 50


class Server:

    def __init__(self, *args, **kwargs):
        try:
            if len(sys.argv[1:]) == 2:
                self.args = [int(x) for x in sys.argv[1:]]
            else:
                raise ValueError
        except ValueError:
            print('Usage: server.py number_of_clients seconds_for_timeout')
            return
        self.kwargs = kwargs
        self.s = socket.socket()
        self.s.bind((HOST, PORT))
        print(f'Server hostname: {HOST}:{PORT}')
        self.s.listen()
        self.initAThread()

    def initAThread(self):
        try:
            threads = []
            self.s.settimeout(self.args[1])
            for i in range(self.args[0]):
                (conn, addr) = self.s.accept()
                t = threading.Thread(target=self.findRequest, args=(conn,))
                threads.append(t)
            for t in threads:
                t.start()
            for t in threads:
                t.join()
        except socket.timeout:
            print(f'Connection timed out after {self.args[1]} seconds')
            return

    def findRequest(self, conn):
        while True:
            try:
                fromClient = pickle.loads(conn.recv(1024))
                k, lst = *fromClient, list(fromClient.values())[0]
                print(k, lst)
                if k == 'q':
                    conn.close()
                    break
                elif k == 'p':
                    info = pickle.dumps(self.getPowerGraph(lst))
                    conn.send(info)
                elif k == 's':
                    info = pickle.dumps(self.getSineGraph(lst))
                    conn.send(info)
            except ConnectionResetError:
                return
            except EOFError:
                break

    def p(self, f):
        def wrapper(*args, **kwargs):
            result = f(*args, **kwargs)
            print(np.min(result), np.max(result))
            return result
        return wrapper

    @p
    def getPowerGraph(self, x_lst):
        x = np.arange(x_lst[1], x_lst[2])
        y = MAX_AMOUNT * (np.power(x, x_lst[0]))
        info = [x, y]
        return info

    @p
    def getSineGraph(self, lst):
        x = np.arange(0, 1, 1 / MAX_AMOUNT)
        y = np.sin(x * lst * np.pi)
        info = [x, y]
        return info


if __name__ == "__main__":
    Server()
