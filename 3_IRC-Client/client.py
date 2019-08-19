import matplotlib.pyplot as plt
import numpy as np
import threading
import socket
import sys
import pickle


HOST = '127.0.0.1'
PORT = 5551


class Client:

    def __init__(self):
        self.s = socket.socket()
        try:
            self.s.connect((HOST, PORT))
            print(f'Client connected to: {HOST}:{PORT}')
            self.initRequestInfo()
        except ConnectionRefusedError:
            print(f'Client connection to {HOST}:{PORT} refused by server.')

    def initRequestInfo(self):
        self.choices = '''
        Please select a choice:
        p: power function
        s: sin function
        q: quit'''
        self.msg = 0
        while self.msg != 'q':
            self.msg = input(f"{self.choices}\nEnter message to send or q to quit: ")
            if self.msg not in ['p', 's', 'q']:
                print('Please select p (power function), s (sin function), or q (quit)')
            elif self.msg == 'q':
                break
            else:
                self.sendInfo()
        self.s.close()
        return

    def sendInfo(self):
        if self.msg == 'p':
            check = False
            while not check:
                numbers = input('Enter exponent, min-x, max-x: ')
                try:
                    info = [int(x.strip()) for x in numbers.split(',')]
                    b = pickle.dumps({'p': info})
                    check = True
                except ValueError:
                    print('Please enter numbers for the exponent, minimum and maximum x')
            self.s.send(b)
            fromServer = pickle.loads(self.s.recv(1024))
            plt.xlabel('x')
            plt.ylabel('y', rotation='horizontal')
            plt.plot(fromServer[0], fromServer[1])
            plt.subplots_adjust(bottom=0.15)
            plt.title(f"x^{info[0]} for x= {info[1]} to {info[2]}")
            plt.grid()
            plt.show()
        elif self.msg == 's':
            check = False
            while not check:
                freq = input('Enter frequency: ')
                try:
                    b = pickle.dumps({'s': int(freq)})
                    check = True
                except ValueError:
                    print('Please enter an integer as the frequency')
            self.s.send(b)
            fromServer = pickle.loads(self.s.recv(1024))
            plt.xlabel('x')
            plt.ylabel('y', rotation='horizontal')
            plt.plot(fromServer[0], fromServer[1])
            plt.subplots_adjust(bottom=0.15)
            plt.title(f"sine {freq}x")
            plt.grid()
            plt.show()


if __name__ == "__main__":
    Client()
