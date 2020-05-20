#!/usr/bin/python3
# coding: utf-8
import random
import numpy as np


def initialize():
    '''
    This function initializes the computers strategy vector
    '''
    strategy=[[] for _ in range(754)]
    for i in range(754):
        board_position = str(i).zfill(3)
        if(int(board_position[0]) in range(8) and int(board_position[1]) in range(6) and int(board_position[2]) in range(4)):
            move = []
            for pile in range(3):
                for piece in range(int(board_position[pile])):
                    move.append([pile+1,piece+1,50])
                strategy[i] = move

    return strategy

def player(n,position):
    '''
    This is the function that runs for a human player to make a move.
    Its input is the player number, and the position of the game.
    It should not return a value; instead it will change the value
    of "position".
    At the end, if the position is [0,0,0], it should announce the winner.
    '''
    move = raw_input("Player %s what move would you like to make?"%n)
    int_move = np.fromstring(move,sep=' ',dtype=int)

    while checkmove(position,int_move[0],int_move[1]) != True:
        move = raw_input("Player %s , what move would you like to make?"%n)
        int_move = np.fromstring(move,sep=' ',dtype=int)

    if checkmove(position,int_move[0],int_move[1]) == True:
        position[int_move[0]-1] = position[int_move[0]-1] - int_move[1]

    if position==[0,0,0]:
        print("Player %s wins!  Congratulations!"%n)

    return 5


def computer(n,position,moves,strategy):
    '''
    This function runs when the computer makes a move.
    Just as when a player makes a move, it should not return a value.
    It should append the move that it makes to the variable "moves",
    and adjust the value of "position" accordingly.
    If the game is over after the move is made, it should announce the winner.
    '''
    pos = int(str(position[0]) + str(position[1]) + str(position[2]))
    mx = strategy[pos][0][2]
    for i in range(len(strategy[pos])):
        if strategy[pos][i][2] > mx:
            mx = strategy[pos][i][2]
    bestmoves = []
    for i in range(len(strategy[pos])):
        if strategy[pos][i][2] == mx:
            bestmoves.append(i)

    #randomly choose a move, execute it, and add it to move[n-1]
    m = bestmoves[random.randint(0,len(bestmoves)-1)]
    move = strategy[pos][m]
    position[move[0]-1] = position[move[0]-1] - move[1]
    print("Computer player {} takes {} objects from pile {}".format(n,move[1],move[0]))
    moves[n-1].append([pos,m])

    if position==[0,0,0]:
        print("Computer Player %s wins!"%n)
        pass

def computertrainer(n,position,moves,strategy):
    '''
    This should be a copy of "computer", without the print statements.
    It is used to train the computer, without lots of printing.
    '''
    pos = int(str(position[0]) + str(position[1]) + str(position[2]))
    mx = strategy[pos][0][2]
    for i in range(len(strategy[pos])):
        if strategy[pos][i][2] > mx:
            mx = strategy[pos][i][2]
    bestmoves = []
    for i in range(len(strategy[pos])):
        if strategy[pos][i][2] > mx - 90:
            bestmoves.append(i)

    #randomly choose a move, execute it, and add it to move[n-1]
    m = bestmoves[random.randint(0,len(bestmoves)-1)]
    move = strategy[pos][m]
    position[move[0]-1] = position[move[0]-1] - move[1]
    moves[n-1].append([pos,m])


    pass


def playgame(strategy):
    '''
    This is the function that coordinates the game playing.
    It determines which of players one and two are human,
    and which are computers.
    It should continue to run until the user answers no to the
    question "Would you like to play a game? (Y/N) "
    If two computer players are selected, it should ask how many games
    the computer players should play.
    It does not need to return a value.
    '''
    YN = raw_input("Would you like to play a game? (Y/N) ")
    while YN=="Y" or YN=="y":

        P1 = ''
        P2 = ''
        valid_answer = ["C","H"]
        while P1 not in valid_answer and P2 not in valid_answer:
            P1 = raw_input("Player 1: Computer (C) or Human (H)? (C/H)")
            P2 = raw_input("Player 2: Computer (C) or Human (H)? (C/H)")
        if P1 == "C" and P2 == "C":
            num_games = input("How many games?")
            for i in range(num_games):
                print("-Beginning Game {}—".format(i+1))
                position = [7,5,3]
                while position != [0,0,0]:
                    print ("The piles have {}, {}, {}, objects".format(position[0],position[1],position[2]))
                    if P1 == "C":
                        computer(1,position,[[],[]],strategy)
                    elif P1 == "H":
                        player(1,position)
                    print ("The piles have {}, {}, {}, objects".format(position[0],position[1],position[2]))
                    if P2 == "C":
                        computer(2,position,[[],[]],strategy)
                    elif P2 == "H":
                        player(2,position)

        elif P1 == "H" or P2 == "H":
            position = [7,5,3]
            while position != [0,0,0]:
                print ("The piles have {}, {}, {}, objects".format(position[0],position[1],position[2]))
                if P1 == "C":
                    computer(1,position,[[],[]],strategy)
                elif P1 == "H":
                    player(1,position)
                print ("The piles have {}, {}, {}, objects".format(position[0],position[1],position[2]))
                if position != [0,0,0]:
                    if P2 == "C":
                        computer(2,position,[[],[]],strategy)
                    elif P2 == "H":
                        player(2,position)
        YN = raw_input("Would you like to play again? (Y/N)")
        if YN == "Y" or YN == "y":
            playgame(strategy)



def traincomputer2(strategy):
    '''
    This function trains the computer by having it play 15,000 games against
    itself adjusting weights on the moves played after each game
    '''
    for _ in range(15000):
        position = [7,5,3]
        playernumber = 2
        moves = [[],[]]
        #computer plays a game against itself
        while position != [0,0,0]:
            playernumber = 1 if playernumber == 2 else 2
            computertrainer(playernumber,position,moves,strategy)

        winner = playernumber
        loser = 1 if winner == 2 else 2

        #adjusts weights for winner's moves
        for i in range(len(moves[winner-1])):
            pos = moves[winner-1][i][0]
            move = moves[winner-1][i][1]
            if i == len(moves[winner-1]) - 1:
                strategy[pos][move][2] = 1000
            else:
                strategy[pos][move][2] += 29
                if strategy[pos][move][2] > 100:
                    strategy[pos][move][2] = 100

        #adjusts weights for loser's moves
        for i in range(len(moves[loser-1])):
            pos = moves[loser-1][i][0]
            move = moves[loser-1][i][1]
            if i == len(moves[loser-1]) - 1:
                strategy[pos][move][2] = -1000
            else:
                strategy[pos][move][2] -= 11
                if strategy[pos][move][2] < 0:
                    strategy[pos][move][2] = 0


def checkmove(position,pile,remove):
    '''
    This function takes in a list of position, indicating the number of pieces
    on each pile, along with a pile number and a positive integer remove that specifies
    how many pieces to remove.
    Returns True if the move is valid and False otherwise
    '''
    if position[pile-1] >= remove:
        return True
    return False

if __name__ == '__main__':
    strategy = initialize()
    traincomputer2(strategy)
    playgame(strategy)
