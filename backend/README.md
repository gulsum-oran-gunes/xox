FOR MİGRATİON
flask db migrate -m "Add player_symbol column to Game model"
flask db upgrade

for start
gulsum@192 xox % source /Users/gulsum/xox/.venv/bin/activate
cd /Users/gulsum/xox/backend
(.venv) gulsum@192 backend % python run.py


FOR POSTMAN REQUEST MAKE_MOVE
{
    "game_id": 3,
    "move": 4
}

FOR POSTMAN REQUEST START_GAME
{
    "player_symbol": "o",
    "username": "example "

}
FOR TEST START:
./.venv/bin/pytest -v -rx backend/tests/test_routes.py
./.venv/bin/pytest --log-cli-level=DEBUG