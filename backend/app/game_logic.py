import math
from flask import jsonify
import json
class GameLogic:
    def __init__(self, player_symbol, board):
        # Tahtayı JSON formatında saklayacağız.
        
        self.player = player_symbol  # Kullanıcı belirliyor
        self.computer = "O" if player_symbol == "X" else "X"  # Bilgisayarın sembolü
        self.board = {int(k): v for k, v in board.items()}
    
    def get_available_moves(self):
        return [k for k, v in self.board.items() if v == " "]

    def make_move(self, move, player):
        move = int(move)
        # Debug (uncomment if needed)
        # print(f"Gelen move degeri: {move} - Tipi: {type(move)}")
        # print(f"Mevcut board durumu: {self.board} - Tipi: {type(self.board)}")
        # print(f"Board JSON formati: {json.dumps(self.board, indent=4)}")
        if self.board[move] == " ":
            self.board[move] = player
            return True
        return False

    def undo_move(self, move):
        self.board[move] = " "

    def winning(self, player):
        win_conditions = [
            (1, 2, 3), (4, 5, 6), (7, 8, 9),  # Yatay
            (1, 4, 7), (2, 5, 8), (3, 6, 9),  # Dikey
            (1, 5, 9), (3, 5, 7)              # Çapraz
        ]
        return any(self.board[a] == self.board[b] == self.board[c] == player for a, b, c in win_conditions)

    def is_draw(self):
        return " " not in self.board.values()

    def minimax(self, depth, is_maximizing):
        if self.winning(self.computer):
            return 10 - depth
        if self.winning(self.player):
            return depth - 10
        if self.is_draw():
            return 0

        if is_maximizing:
            best_score = -math.inf
            for move in self.get_available_moves():
                self.make_move(move, self.computer)
                score = self.minimax(depth + 1, False)
                self.undo_move(move)
                best_score = max(best_score, score)
            return best_score
        else:
            best_score = math.inf
            for move in self.get_available_moves():
                self.make_move(move, self.player)
                score = self.minimax(depth + 1, True)
                self.undo_move(move)
                best_score = min(best_score, score)
            return best_score

    def best_move(self):
        best_score = -math.inf
        move_choice = None
        for move in self.get_available_moves():
            self.make_move(move, self.computer)
            score = self.minimax(0, False)
            self.undo_move(move)
            if score > best_score:
                best_score = score
                move_choice = move
        return move_choice

    def get_board(self):
        # Tahtayı JSON formatında döndürüyoruz.
        return self.board  # board'ı JSON formatına dönüştürüyoruz.


