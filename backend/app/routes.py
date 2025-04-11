from flask import Blueprint, request, jsonify
from app.game_logic import GameLogic
from .models import User, Game
from . import db

routes = Blueprint('routes', __name__)


@routes.route('/start_game', methods=['POST'])
def start_game():
    data = request.get_json()
    player_symbol = data.get('player_symbol').upper()
    username = data.get('username')
    
    if not username:
        return jsonify({"error": "Username is required."}), 400
    
    if player_symbol not in ["X", "O"]:
        return jsonify({"error": "Invalid player symbol. Choose 'X' or 'O'."}), 400
    
    existing_user = User.query.filter_by(username=username).first()
    
    if not existing_user:
        new_user = User(username=username)  # User ID otomatik oluşturulur
        db.session.add(new_user)
        db.session.commit()
        user_id = new_user.id
    else:
        user_id = existing_user.id
   

    initial_board = {i: " " for i in range(1, 10)}
    new_game = Game(user_id=user_id, player_symbol=player_symbol, board=initial_board)  # game_id otomatik olarak artacak, result_id ise 3 olacak
    db.session.add(new_game)
    db.session.commit()

    game_id = new_game.game_id


    computer_symbol = 'O' if player_symbol == 'X' else 'X'
    
    response = {
        "game_id": game_id,
        "user_id": user_id,
        "result_id" : new_game.result_id,
        "player_symbol": player_symbol,
        "computer_symbol": computer_symbol,
       
    }

    
    # Eğer kullanıcı 'O' seçtiyse, bilgisayar otomatik olarak ilk hamlesini yapmalı
    if player_symbol == "O":
        game_logic = GameLogic(player_symbol, new_game.board)
        computer_move = game_logic.best_move()
        game_logic.make_move(computer_move, computer_symbol)
        new_game.board = game_logic.board  # Veritabanını güncelliyoruz
        db.session.commit()

        # Bilgisayarın yaptığı hamleyi yanıtla ekliyoruz
        response["computer_move"] = computer_move

    return jsonify(response)

@routes.route('/make_move', methods=['POST'])
def make_move():
    data = request.get_json()
    game_id = data.get('game_id')
    move = data.get('move')
    
    # Oyun verisini veritabanından çek
    game = Game.query.filter_by(game_id=game_id).first()
    if not game:
        return jsonify({"error": "Game not found."}), 404

    # player_symbol'ı veritabanından al
    player_symbol = game.player_symbol

    # GameLogic sınıfını kullanarak hamleyi yap
    game_logic = GameLogic(player_symbol, game.board)  # board'ı veritabanından alıyoruz
    if game_logic.make_move(move, player_symbol):  # Hamleyi tahtaya uygula
        # Hamleyi veritabanına kaydet
        game.board = game_logic.get_board()  # Güncellenmiş tahta
        db.session.commit()

        # Kazanma kontrolü
        if game_logic.winning(player_symbol):
            game.result_id = 2  # 2: Player won
            db.session.commit()
            return jsonify({"board": game.board,"message": f"Player {player_symbol} wins!", "game_over": True})

        # Beraberlik kontrolü
        if game_logic.is_draw():
            game.result_id = 3  # 3: Draw
            db.session.commit()
            return jsonify({"board": game.board,"message": "It's a draw!", "game_over": True})

        # Bilgisayarın hamlesini yap
        computer_symbol = "O" if player_symbol == "X" else "X"
        computer_move = game_logic.best_move()
        game_logic.make_move(computer_move, computer_symbol)

        # Hamleyi güncelle ve veritabanına kaydet
        game.board = game_logic.get_board()
        db.session.commit()

        # Bilgisayar kazandı mı kontrol et
        if game_logic.winning(computer_symbol):
            game.result_id = 1  # 1: Computer won
            db.session.commit()
            return jsonify({"board": game.board,"message": f"Computer {computer_symbol} wins!", "game_over": True})

        return jsonify({
            "message": f"Player {player_symbol}'s move was successful.",
            "computer_move": computer_move,
            "board": game.board,
            "game_over": False
        })
    
    return jsonify({"error": "Invalid move."}), 400

