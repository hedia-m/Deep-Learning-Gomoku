#!/usr/bin/env python3

import numpy as np
from reinforcement import game
from network import Network
import protocol
import threading
import os

class Thread(threading.Thread):
    def __init__(self, protocol):
        threading.Thread.__init__(self)
        self.protocol = protocol

    def run(self):
        while protocol.running[0]:
            self.protocol.nextCmd()

def piskvork_game():
    """
    play gomoku game using trained model and piskvork interface
    """
    board = np.zeros((3, 19, 19), np.int8)
    running = [1]
    protocol = protocol.Protocol(board, running)
    thread = Thread(protocol)

    thread.start()
    while running[0]:
        args = protocol.pullCmd();
        cmd = args[0].lower()
        del args[0]
        if cmd == "none":
            pass
        elif cmd == "start":
            print("OK")
        elif cmd == "turn":
            try:
                pos = args[0].split(',')
                board[0][int(pos[1])][int(pos[0])] = '2'
            except:
                print("ERROR")
            print("DEBUG", "Calculating the next move")
            # ADD OWN TURN CALCULATION
            # print(x + "," + y)
        elif cmd == "begin":
            print("DEBUG", "Calculating the next move")
            # ADD OWN TURN CALCULATION
            # print(x + "," + y)
            pass
        else:
            print("ERROR")
    thread.join()

def load_nparray(filename):
    if os.path.exists(filename):
        array = np.load(filename)
        os.remove(filename)
        return array

def train_from_file(filename, network):
    if os.path.exists(filename):
        array = np.load(filename)
        network.train(array['boards'], array['p'], array['z'])
        os.remove(filename)

def reinforcement():
    """
    train model against itself
    """

    # parameters
    number_of_games = 1
    player_1 = Network(-1)
    player_2 = Network(-1)

    for num_game in range(number_of_games):
        # play a game until the end
        game(player_1, player_2, "save.npz")

        # trainning all 3 games (for example)
        if num_game % 1 == 0:
            # train network
            train_from_file("save.npz", player_2)

if __name__ == '__main__':
    # training
    reinforcement()

    # real game
    #piskvork_game()
