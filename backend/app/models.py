from app import db



# Users Tablosu
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)

    # İlişkiler
    games = db.relationship('Game', backref='user', lazy= 'dynamic')
  

# Results Tablosu
class Result(db.Model):
    __tablename__ = 'results'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50), nullable=False)
    
    # İlişkiler
    games = db.relationship('Game', backref='result', lazy= 'dynamic')

# Games Tablosu
class Game(db.Model):
    __tablename__ = 'games'
    game_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    result_id = db.Column(db.Integer, db.ForeignKey('results.id'), nullable=True)
    player_symbol = db.Column(db.String(1), nullable=False)
    board = db.Column(db.JSON, nullable=True, default=lambda: {str(i): " " for i in range(1, 10)})

