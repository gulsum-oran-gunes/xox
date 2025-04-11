FOR MİGRATİON
flask db migrate -m "Add player_symbol column to Game model"
flask db upgrade




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
