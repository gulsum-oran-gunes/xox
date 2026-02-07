import unittest
import json
from app import create_app, db  # create_app() fonksiyonunu içe aktar

class TestRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()

        with cls.app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()
        cls.app_context.pop()

    def test_start_game_existing_user(self):
        # İlk kullanıcıyı oluştur
        with self.app.app_context():
            from app.models import User  # Modülleri bağlam içinde içe aktar
            user = User(username="test_user")
            db.session.add(user)
            db.session.commit()

        response = self.client.post('/start_game', json={"username": "test_user", "player_symbol": "X"})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn("game_id", data)

    def test_start_game_missing_username(self):
        response = self.client.post('/start_game', json={"player_symbol": "X"})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", data)

    def test_make_move_invalid_game_id(self):
        response = self.client.post('/make_move', json={"game_id": 999, "move": 1})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertIn("error", data)

    def test_make_move_invalid_position(self):
        start_response = self.client.post('/start_game', json={"username": "test_user", "player_symbol": "X"})
        game_data = json.loads(start_response.data)
        game_id = game_data["game_id"]

        move_response = self.client.post('/make_move', json={"game_id": game_id, "move": 10})
        move_data = json.loads(move_response.data)

        self.assertEqual(move_response.status_code, 400)
        self.assertIn("error", move_data)

    def test_player_win_condition(self):
        start_response = self.client.post('/start_game', json={"username": "test_user", "player_symbol": "X"})
        game_data = json.loads(start_response.data)
        game_id = game_data["game_id"]

        # Oyuncunun kazandığı durumu simüle et
        with self.app.app_context():
            from app.models import Game
            game = Game.query.filter_by(game_id=game_id).first()
            game.board = {1: "X", 2: "X", 3: " ", 4: " ", 5: " ", 6: " ", 7: " ", 8: " ", 9: " "}
            db.session.commit()

        move_response = self.client.post('/make_move', json={"game_id": game_id, "move": 3})
        move_data = json.loads(move_response.data)

        self.assertEqual(move_response.status_code, 200)
        self.assertIn("game_over", move_data)
        self.assertTrue(move_data["game_over"])

