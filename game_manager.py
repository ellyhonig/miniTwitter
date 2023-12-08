import csv
import random
import string

class GameManager:
    def __init__(self, games_file='games.csv', login_manager=None):
        self.games_file = games_file
        self.login_manager = login_manager

    def new_game(self, opponent_username):
        game_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        current_user = self.login_manager.current_user['username']
        initial_board = '.' * 9  # 9 dots representing an empty 3x3 board
        with open(self.games_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([game_id, current_user, opponent_username, initial_board, current_user, ''])
        return game_id

    def add_move(self, game_id, row, col):
        updated_games = []
        move_made = False
        current_user = self.login_manager.current_user['username']
        with open(self.games_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for game in reader:
                if game['game_ID'] == game_id and game['current_turn'] == current_user:
                    board = list(game['board_state'])
                    index = row * 3 + col
                    if board[index] == '.':
                        board[index] = 'X' if current_user == game['player1'] else 'O'
                        game['board_state'] = ''.join(board)
                        game['current_turn'] = game['player2'] if current_user == game['player1'] else game['player1']
                        move_made = True
                updated_games.append(game)

        if move_made:
            with open(self.games_file, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
                writer.writeheader()
                writer.writerows(updated_games)

    def win_check(self, game_id):
        with open(self.games_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            games = list(reader)

        winner = None
        for game in games:
            if game['game_ID'] == game_id:
                board = game['board_state']
                lines = [board[i:i+3] for i in range(0, 9, 3)] + \
                        [board[i::3] for i in range(3)] + \
                        [board[0::4], board[2:8:2]]
                if 'XXX' in lines:
                    winner = game['player1']
                elif 'OOO' in lines:
                    winner = game['player2']
                break

        if winner:
            # Update the winner in the CSV file
            with open(self.games_file, 'w', newline='') as file:
                fieldnames = ['game_ID', 'player1', 'player2', 'board_state', 'current_turn', 'winner']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for game in games:
                    if game['game_ID'] == game_id:
                        game['winner'] = winner
                    writer.writerow(game)

        return winner
    def get_games_for_user(self, username):
        games = []
        with open(self.games_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['player1'] == username or row['player2'] == username:
                    games.append(row)
        return games