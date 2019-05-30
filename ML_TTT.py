import random
import pickle
win_reward = 1
lose_reward = -1
illegal_move_reward = -2
draw_reward = 0
gamma = 0.01

def main():
    board = " " * 9
    my_piece = 'X'
    opp_piece = 'O'
    machine_brain = open("machinebrain.pickle", "ab+")
    try:
        exp_reward_dict = pickle.load(machine_brain)
    except:
        exp_reward_dict = {}
    print (exp_reward_dict)
    i = 0
    while (i < 10000):
        prev_board = board
        if random.randint(0, 99) < 90:
            rewards, max_reward, move = find_max_reward(board, exp_reward_dict)
            print (rewards)
            print ("Rewards taken: ", max_reward)
        else:
            rewards, max_reward, move = find_max_reward(board, exp_reward_dict)
            move = random.randint(0, 8)
            print (rewards)
            print ("Random!!")
        exp_reward = get_expected_reward(board, move, exp_reward_dict)
        board = make_move(board, move, my_piece)
        if (illegal_move(prev_board, move)):
            print ("Illegal move!!")
            rewards, max_reward,max_move = find_max_reward(board, exp_reward_dict)
            exp_reward_dict[(board, move)] = (exp_reward + illegal_move_reward + gamma * max_reward)/2
            continue
        if win(board, my_piece) or draw(board):
            max_reward = 0  ##because no possible moves
            print_board(board)
            if draw(board):
                print ("Draw!!")
                exp_reward_dict[(prev_board, move)] = (exp_reward + draw_reward + gamma * max_reward)/ 2
            else:
                print ("Computer Wins!!")
                exp_reward_dict[(prev_board, move)] = (exp_reward + win_reward + gamma * max_reward)/2
            board = " " * 9
            i += 1
            continue
        print_board(board)
        while (1):    #opponent's input
            opp_move = int(input("Enter the move: "))#random.randint(0, 8)#
            if (opp_move == -1):
                break
            if (illegal_move(board, opp_move)): 
                continue
            else:
                break
        if (opp_move == -1):
            break
        board = make_move(board, opp_move, opp_piece)
        print_board(board)
        if (win(board, opp_piece)):
            max_reward = 0 #no possible moves
            exp_reward_dict[(prev_board, move)] = (exp_reward + lose_reward + gamma * max_reward)/2
            print ("Human Wins!")
            board = " " * 9
            i += 1
            continue
        else:
            rewards, max_reward, max_move = find_max_reward(board, exp_reward_dict)#find the maximum out of all possible states in this move
            exp_reward_dict[(prev_board, move)] = (exp_reward + draw_reward + gamma * max_reward)/2
    pickle.dump(exp_reward_dict, machine_brain)
    machine_brain.close()

def print_board(board):
    for j in range(3):
        print ("|-+-+-|")
        for i in range(3):
            print('|', end=board[j * 3 + i])
        print ('|')
    print ("|-+-+-|")    

def get_expected_reward(board, move, exp_reward_dict):
    if (board, move) not in exp_reward_dict:
        exp_reward_dict[(board, move)] = 0
    return exp_reward_dict[(board, move)]

def make_move(board, move, piece):
    if (board[move] != " "):
        return board
    return board[:move] + piece + board[move + 1:]

def illegal_move(board, move):
    return (move < 0 or move > 8 or board[move] != " ")

def win(board, piece):
    for i in range(3):    #col check
        has_piece = True
        for j in range(3):
            if (board[i * 3 + j] != piece):
                has_piece = False
                break
        if (has_piece):
            return True
        continue

    for i in range(3):   #row check
        has_piece = True
        for j in range(0, 7, 3):
            if (board[i + j] != piece):
                has_piece = False
                break
        if (has_piece):
            return True
        continue    

    has_piece = True
    for i in range(3):
        if (board[4 * i] != piece):
            has_piece = False
            break
    if (has_piece):
        return True

    j = 2
    has_piece = True
    for i in range(3):
        if (board[2 * (i + 1)] != piece):
            has_piece = False
            break
        j -= 1
    if (has_piece):
        return True    
    return False    


def draw(board):
    for i in range(9):
        if (board[i] == " "):
            return False
        
    if not win(board, 'X') and not win(board, 'O'):
        return True
    return False

def find_max_reward(board, exp_reward_dict):
    rewards = []
    for i in range(9):
        if (board, i) not in exp_reward_dict:
            exp_reward_dict[(board, i)] = 0
        rewards.append(exp_reward_dict[(board, i)])                
    max_move = 0
    max_reward = rewards[0]
    for i in range(1, 9):
        if rewards[i] > max_reward:
            max_reward = rewards[i]
            max_move = i
    return rewards, max_reward, max_move


main()            
        



