import copy as c
import random as r
import os
import matplotlib.pyplot as plt


def all_equal(list):
    return len(set(list)) <= 1


def convert_board_proper(string):
    list_var = string.split(',')
    for j in range(len(list_var)):
        list_var[j] = list_var[j].split('.')


def generate_board(size):
    return [[' ' for i in range(size)] for j in range(size)]


def print_board(board):
    board_size = len(board)
    for i in range(board_size):
        print board_size * '+---+'
        print board_size * '| %s |' % (tuple([board[i][j] for j in range(board_size)]))
    print board_size * '+---+'


def check_move(board, move):
    try:
        if board[move[0]][move[1]] == ' ':
            return True
        else:
            return False
    except IndexError:
        return False


def test_board(board):
    """
    This function will check the score of the match.
    :param board: Board is the current game
    :return: (True,False), {team,location}
    """
    board_size = len(board)  # used for range lengths
    """
        Rows are checked for size n using indexing.
    """
    for row in range(board_size):
        if all_equal(board[row]) == True and ' ' not in board[row]:
            return True, {'Team': board[row][0], 'Row': row + 1}
        else:
            pass
    """
        Columns are checked for size n using indexing.
    """
    for column in range(board_size):
        testing_column = [board[i][column] for i in range(board_size)]
        if all_equal(testing_column) == True and ' ' not in testing_column:
            return True, {'Team': board[0][column], 'Column': column + 1}
        else:
            pass
    """
        Testing for diagonals
    """
    left_diagonal = [board[j][j] for j in range(board_size)]
    right_diagonal = [board[j][-1 - j] for j in range(board_size)]
    if all_equal(left_diagonal) == True and ' ' not in left_diagonal:
        return True, {'Team': board[0][0], 'Diagonal': 'Left'}
    elif all_equal((right_diagonal)) == True and ' ' not in right_diagonal:
        return True, {'Team': board[0][-1], 'Diagonal': 'Right'}
    else:
        return False


def get_learning_data(size):
    """
    This fetches file data for the machine learning.
    :param size: The size of the board
    :return: False if a random move must be made due to failed size, [data] if not.
    """
    known_sizes = open('C:\\Users\\User\\Desktop\\Machine Learning\\known_sizes.txt', 'r')
    known_sizes.seek(0)
    temp_file_data = known_sizes.read().split(',')[:-1]
    temp_file_data = [int(temp_file_data[i]) for i in range(len(temp_file_data))]
    # If the size is a known size
    if (size in temp_file_data):
        """
            Changing data format to usable form.
        """
        data_file = open(str(size) + '.txt', 'r')
        data_file.seek(0)
        data = data_file.read().split('+')[:-1]
        data_file.close()
        for entry in range(len(data)):
            data[entry] = data[entry].split(':')
            data[entry][1] = data[entry][1].split(';')
            for element in range(len(data[entry][1])):
                data[entry][1][element] = int(data[entry][1][element])
        return {data[n][0]: data[n][1] for n in range(len(data))}
    else:
        known_sizes = open('C:\\Users\\User\\Desktop\\Machine Learning\\known_sizes.txt', 'a')
        known_sizes.seek(2)
        known_sizes.write(str(size) + ',\n')
        known_sizes.close()
        data_file = open(str(size) + '.txt', 'w+')
        data_file.close()
        return False


def make_move(board):
    """
    Allows the machine to make an educated move
    :param board: The current board.
    :return: The best known move.
    """
    board_length = len(board)
    master_board = c.deepcopy(board)
    knowledge = get_learning_data(board_length)
    """

    Creates a random move because the knowledge base doesnt have a conceivable move.

    """
    if knowledge == False:
        legal_loop = False
        while legal_loop is False:
            legal_loop = True
            play_points = r.randint(0, board_length - 1), r.randint(0, board_length - 1)
            if board[play_points[0]][play_points[1]] == ' ':
                master_board[play_points[0]][play_points[1]] = 'X'
                return [master_board, play_points]
            else:
                legal_loop = False
    else:
        stringed_board = str(board).replace("' '", " ").replace("  ", " ")
        if (stringed_board in knowledge.keys()) == True:
            legal_loop = False
            while legal_loop is False:
                legal_loop = True
                points = knowledge[stringed_board]
                if board[points[0]][points[1]] == ' ':
                    master_board[points[0]][points[1]] = 'X'
                    return [master_board, points]
                else:
                    print "Knowledge showed move not eligible"
                    break
        else:
            """
            No known move in data
            """
            legal_loop = False
            while legal_loop is False:
                legal_loop = True
                play_points = r.randint(0, board_length - 1), r.randint(0, board_length - 1)
                if board[play_points[0]][play_points[1]] == ' ':
                    master_board[play_points[0]][play_points[1]] = 'X'
                    return [master_board, play_points]
                else:
                    legal_loop = False


def write_data(size, board, position):
    temp_file = open(str(size) + '.txt', 'a')
    stringed_board = str(board).replace("' '", " ").replace("  ", " ")
    temp_file.write(stringed_board + ':' + str(position[0]) + ';' + str(position[1]) + '+')
    temp_file.close()
    return True


def play_game(size):
    """
    This allows a full game to be played
    :param size: The size of the game
    :return: The winner/looser
    """
    game = generate_board(size)  # creates game board of the proper size
    os.system('cls')  # clears the screen
    move_storage = {}
    available_moves = size ** 2  # this is the number of possible moves
    winner = False  # True if a winner has been found
    while winner == False and available_moves > 0:
        os.system('cls')
        print "It is the machines turn, there are %s moves left." % (str(available_moves))
        print_board(game)  # prints the graphical board
        ai_move = make_move(game)  # This is the AI machines move
        move_storage[str(ai_move[0]).replace("' '", " ").replace("  ", " ")] = ai_move[1]
        available_moves -= 1  # reduce the number of moves by 1
        print "The machine made the move %s, %s." % (str(ai_move[1][0] + 1), str(ai_move[1][1] + 1))
        game = c.deepcopy(ai_move[0])  # updates the game board with the new move.
        if test_board(game) == False and available_moves > 0:
            """
                It is the players turn
            """
            print "It is the player's turn, there are %s moves left." % (str(available_moves))
            print_board(game)
            """
                        Player move checking loop
            """
            player_legal_move = False
            while player_legal_move is False:
                try:
                    player_legal_move = True
                    player_move = [int(j) - 1 for j in
                                   raw_input("What move would you like to move, <1-n>,<1-n>: ").split(',')]
                    if check_move(game, player_move) == False:
                        player_legal_move = False
                        print 'That move has already been made.'
                    else:
                        """
                            This means that the move is legal
                        """
                        pass
                except TypeError():
                    print " Input failed, must be an integer entry."
                except IndexError():
                    print "That move is invalid, the inputs must be less that %s." % (str(size))
            game[player_move[0]][player_move[1]] = 'O'  # Player Makes Move
            available_moves -= 1
            print "The player made the move %s,%s." % (tuple([str(i + 1) for i in player_move]))
            print_board(game)
        elif available_moves <= 0 and test_board(game) == False:
            """
                There is a tie
            """
            """
            Writing loop
            """
            for element in move_storage:
                write_data(size, str(element).replace("' '", " ").replace("  ", " "), move_storage[element])
            print "The game is tied."
            winner = True
            return 'Tie'
        else:
            """
                The AI won
            """
            winner = True
            """
            Writing loop
            """
            for element in move_storage:
                write_data(size, str(element).replace("' '", " ").replace("  ", " "), move_storage[element])
            return 'machine'
        if test_board(game) != False:
            """
                Player Won
            """
            winner = True
            return 'player'
        else:
            pass


def main():
    play_game_loop = False
    while play_game_loop is False:
        try:
            play_game(int(raw_input('What size of game do you want to play? ')))
            exit_var = int(raw_input('Leave(1) or stay(2)? '))
            if exit_var != 2:
                play_game_loop = False
            else:
                exit()
        except ValueError:
            print 'input must be integer.'


os.chdir('C:\\Users\\User\\Desktop\\Machine Learning')
main()
