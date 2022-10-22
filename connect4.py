import os
import random

def check_move(board, turn, col, pop):
    num_rows = int(len(board)/7)

    #make sure column value is not beyond board limits
    if not (0 <= col <= 6):
        return False

    if not pop: #player wants to insert disc

        #make sure not adding to a column if column is already full

        #count number of discs in column
        count_column = 0
        for i in range(col, len(board), 7):
            if board[i] == 1 or board[i] == 2:
                count_column += 1

        if count_column == num_rows: #column already full
            return False
    elif pop:
        if board[col] != turn: #player wants to pop disc that is not his/hers
            return False

    else: #player did not indicate insert or pop
        return False


    return True

def apply_move(board, turn, col, pop):

    board_copied = board.copy()

    if pop:
        for i in range(col, len(board_copied), 7):

            if i+7 < len(board_copied): #not the top most row
                board_copied[i] = board_copied[i+7]

            else: #top most row
                board_copied[i] = 0

    elif not pop:
        for i in range(col, len(board_copied), 7):
            if board_copied[i] == 1 or board_copied[i] == 2: #disc already in the slot
                continue
            else:
                board_copied[i] = turn
                break



    # implement your function here
    return board_copied.copy()

def check_victory(board, who_played):

    who_won = []
    num_rows = int(len(board)/7)

    #check rows
    for i in range(4):
        for j in range(0+i, num_rows*7, 7):

            #both players win at the same time. So player who made move lose
            if (board[j] == board[j+1] == board[j+2] == board[j+3] == 1):
                #player 1 won
                who_won.append(1)
            if (board[j] == board[j+1] == board[j+2] == board[j+3] == 2):
                #player 2 won
                who_won.append(2)

    #check columns
    for i in range((num_rows-4+1)*7):
        if (board[i] == board[i+7] == board[i+14] == board[i+21] == 1):
            #player 1 won
            who_won.append(1)

        if (board[i] == board[i+7] == board[i+14] == board[i+21] == 2):
            #player 2 won
            who_won.append(2)


    #check upwards diagonal
    for i in range(4):
        for j in range(0+i, (num_rows - 4 + 1)*7, 7):
            if (board[j] == board[j+8] == board[j+16] == board[j+24] == 1):
                #player 1 won
                who_won.append(1)
            if (board[j] == board[j+8] == board[j+16] == board[j+24] == 2):
                #player 2 won
                who_won.append(2)

    #check downwards diagonal
    for i in range(4):
        for j in range(21+i, len(board),7):
            if (board[j] == board[j-6] == board[j-12] == board[j-18] == 1):
                #player 1 won
                who_won.append(1)
            if (board[j] == board[j-6] == board[j-12] == board[j-18] == 2):
                #player 2 won
                who_won.append(2)

    #no one wins

    if who_won == []: #nobody won
        return 0
    elif len(set(who_won)) == 1: #only 1 person won
        return who_won[0]
    elif len(set(who_won)) > 1: #more than 1 person won
        if who_played == 1:
            return 2
        elif who_played == 2:
            return 1

def computer_move(board, turn, level):

    if level == 1: #random
        column = random.randint(0,6)
        pop = random.randint(1,2) == 1
        return (column,pop)

    elif level == 2: #medium
        #check if there is a move that can make the computer win

        #win by inserting disc
        for i in range(0,7):
            if check_move(board, turn, i, False):
                board_tmp = apply_move(board, turn, i, False)
                if check_victory(board_tmp, turn) == turn: #there is a move that can make the computer win by inserting discs
                    return (i, False)

        #win by popping disc
        for i in range(0,7):
            if check_move(board, turn, i, True):
                board_tmp = apply_move(board, turn, i, True)
                if check_victory(board_tmp, turn) == turn: #there is a move that can make the computer win by popping discs
                    return (i, True)


        #no such move exists so avoid letting enemy win

        if turn == 1:
            other_player_turn = 2
        elif turn == 2:
            other_player_turn = 1

        #avoid letting enemy win by inserting disc
        for i in range(0,7):
            if check_move(board, other_player_turn, i, False):
                board_tmp = apply_move(board, other_player_turn, i, False)
                if check_victory(board_tmp, other_player_turn) == other_player_turn: #there is a move that can make the computer win by inserting discs
                    return (i, False)



        #no moves so random valid move

        column = random.randint(0,6)
        pop = random.randint(1,2) == 1
        return (column,pop)

def display_board(board):
    board_rows = int(len(board) / 7)
    board_cols = 7 # won't change

    #print the column number
    for col_num in range(board_cols):
        print(f' ({col_num}) ', end="")
    print('\n')

    #print the rest of the board
    for row_num in range(board_rows-1, -1, -1):
        print('|',end="")
        for col_num in range(0, board_cols):
            index = 7 * row_num + col_num
            if board[index] == 0:
                print(f"    |", end="")
            else:
                print(f" {board[index]}  |", end="")
        print()

def menu():
    os.system('cls')
    print('Welcome to Connect Four')
    print('-----------------------')
    print('\n')

    #getting input from user
    while True:
        try:
            board_row = int(input('How many rows do you want on your board? '))
            if not (7<= board_row <= 10):
                raise Exception

            while True:
                try:
                    human_or_computer = input("Do you want to play with a human or computer? Enter 'H' for human and 'C' for computer: ")
                    if not (human_or_computer == "C" or human_or_computer == "H"):
                        raise Exception

                    if human_or_computer == "C":

                        while True:
                            try:
                                com_level = int(input("Select the difficulty level of the computer. Enter '1' or '2': "))
                                if com_level != 1 and com_level != 2:
                                    raise Exception
                                break
                            except:
                                print('Error! Please only select 1 or 2: ')
                    break

                except:
                    print('Error! Please enter only "C" or "H": ')

            break
        except:
            print('Error! Please enter a number between 7 and 10')

    # create initial board
    board = [0 for x in range(board_row * 7)]
    display_board(board)
    gameStillPlaying = True

    if human_or_computer == "H":
        player_turn = 1 #player 1 always start
    elif human_or_computer == "C":
        player_turn = 1 #player 1 always start
        human_turn = random.randint(1,2) #decide if human is player 1 or player 2

    while gameStillPlaying:
        #human vs human
        if human_or_computer == "H":
            print(f"Player {player_turn}'s turn")
            while True:
                try:
                    col = int(input('Please select a column: '))
                    if not(0<=col<=6):
                        raise Exception
                    break
                except:
                    print("Column number have to be between 0 and 6. Try again!")
            while True:
                try:
                    pop = input('Do you want to pop from the column (T/F)? ')
                    if not(pop.lower() == "t" or  pop.lower() == "f"):
                        raise Exception
                    break
                except:
                    print('Please only enter "T" or "F" ')
            #convert pop to boolean
            pop = pop == "T" or pop == "t"
            if check_move(board, player_turn, col, pop):
                board = apply_move(board, player_turn, col, pop)
                os.system('cls')
                display_board(board)

                #check if anyone won and end game if true
                gameStillPlaying = check_victory(board, player_turn) == 0
                if not gameStillPlaying:
                    break
                else:
                    #switch player
                    player_turn = (player_turn % 2) + 1
            else: #move not valid
                print("Move not valid! Please try again!")

        elif human_or_computer == "C":

            #human start
            if human_turn == player_turn:
                print(f'You are player {human_turn}')
                while True:
                    try:
                        col = int(input('Please select a column: '))
                        if not(0<=col<=6):
                            raise Exception
                        break
                    except:
                        print("Column number have to be between 0 and 6. Try again!")
                while True:
                    try:
                        pop = input('Do you want to pop from the column (T/F)? ')
                        if not(pop.lower() == "t" or  pop.lower() == "f"):
                            raise Exception
                        break
                    except:
                        print('Please only enter "T" or "F" ')
                #convert pop to boolean
                pop = pop == "T" or pop == "t"
                if check_move(board, player_turn, col, pop):
                    board = apply_move(board, player_turn, col, pop)
                    os.system('cls')
                    display_board(board)

                    #check if anyone won and end game if true
                    gameStillPlaying = check_victory(board, player_turn) == 0
                    if not gameStillPlaying:
                        break
                    else:
                        #switch player
                        player_turn = (player_turn % 2) + 1
                else: #move not valid
                    print("Move not valid! Please try again!")
            #computer start
            elif human_turn != player_turn:
                col, pop = computer_move(board,player_turn, com_level)
                #make sure the computer move is an allowable one
                while not(check_move(board, player_turn, col, pop)):
                    col, pop = computer_move(board,player_turn, com_level)
                board = apply_move(board, player_turn, col, pop)
                os.system('cls')
                display_board(board)

                if pop:
                    print(f"The computer popped a disc from column {col}.")
                elif not(pop):
                    print(f"The computer inserted a disc into column {col}.")

                gameStillPlaying = check_victory(board, player_turn) == 0
                if not gameStillPlaying:
                    break
                else:
                    #switch player
                    player_turn = (player_turn % 2) + 1


    #while loop exited - someone won the game
    if human_or_computer == "H":
        print(f'Congratulations player {player_turn}! You won the game!')
    elif human_or_computer == "C":
        if player_turn == human_turn: #human won
            print('Congratulations, you won the computer!')
        elif player_turn != human_turn:
            print(f'Unfortunately, the computer (player {player_turn}) won. Better luck next time!')

if __name__ == "__main__":
    menu()






