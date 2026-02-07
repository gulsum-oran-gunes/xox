import React, { useMemo, useState } from "react";
import Header from "./components/Header";
import GameBoard from "./components/GameBoard";
import "./App.css";

const emptyBoard = Array.from({ length: 9 }, () => "");

const API_BASE = "http://127.0.0.1:5000";

const apiBoardToArray = (apiBoard) => {
  if (!apiBoard) {
    return [...emptyBoard];
  }

  return Array.from({ length: 9 }, (_, index) => {
    const value = apiBoard[index + 1] ?? apiBoard[String(index + 1)];
    return value === " " ? "" : value || "";
  });
};

function App() {
  const [board, setBoard] = useState(emptyBoard);
  const [gameId, setGameId] = useState(null);
  const [username, setUsername] = useState("");
  const [playerSymbol, setPlayerSymbol] = useState("X");
  const [computerSymbol, setComputerSymbol] = useState("O");
  const [status, setStatus] = useState("Choose a symbol and start a new game.");
  const [resultText, setResultText] = useState("Not started");
  const [isLoading, setIsLoading] = useState(false);
  const [gameOver, setGameOver] = useState(false);

  const isStartDisabled = useMemo(
    () => !username.trim() || isLoading,
    [username, isLoading]
  );

  const startGame = async () => {
    if (isStartDisabled) {
      return;
    }

    setIsLoading(true);
    setStatus("Starting game...");
    setResultText("Starting...");
    setGameOver(false);

    try {
      const response = await fetch(`${API_BASE}/start_game`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: username.trim(),
          player_symbol: playerSymbol,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        setStatus(data?.error || "Failed to start game.");
        setResultText("Error");
        return;
      }

      setGameId(data.game_id);
      setComputerSymbol(data.computer_symbol);

      const nextBoard = [...emptyBoard];
      if (data.computer_move) {
        const moveIndex = Number(data.computer_move) - 1;
        if (moveIndex >= 0 && moveIndex < nextBoard.length) {
          nextBoard[moveIndex] = data.computer_symbol;
        }
      }

      setBoard(nextBoard);
      setStatus("Click a square to make a move.");
      setResultText("In progress");
    } catch (error) {
      setStatus("Network error. Is the backend running?");
      setResultText("Error");
    } finally {
      setIsLoading(false);
    }
  };

  const handleMove = async (index) => {
    if (isLoading || gameOver || !gameId) {
      return;
    }

    if (board[index]) {
      return;
    }

    setIsLoading(true);

    try {
      const response = await fetch(`${API_BASE}/make_move`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          game_id: gameId,
          move: index + 1,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        setStatus(data?.error || "Move failed.");
        setResultText("Error");
        return;
      }

      const nextBoard = apiBoardToArray(data.board);

      const message = data.message || "";
      const normalized = message.toLowerCase();
      const isDraw = normalized.includes("draw");
      const isPlayerWin =
        normalized.includes("player") && normalized.includes("wins");
      const isComputerWin =
        normalized.includes("computer") && normalized.includes("wins");
      const isBoardFull = nextBoard.every((cell) => cell);

      if (data.game_over || isDraw || isPlayerWin || isComputerWin || isBoardFull) {
        setBoard(nextBoard);
        setGameOver(true);
        setStatus("");
        if (isDraw || (isBoardFull && !isPlayerWin && !isComputerWin)) {
          setResultText("Draw !!!");
        } else if (isPlayerWin) {
          setResultText(`Player  wins !!!`);
        } else if (isComputerWin) {
          setResultText(`Computer  wins !!!`);
        } else {
          setResultText("Finished");
        }
        setIsLoading(false);
      } else {
        const playerBoard = [...board];
        playerBoard[index] = playerSymbol;
        setBoard(playerBoard);
        setStatus("Computer is thinking...");
        setResultText("In progress");

        if (data.computer_move) {
          setTimeout(() => {
            setBoard(nextBoard);
            setStatus(message || "Next move.");
            setIsLoading(false);
          }, 700);
        } else {
          setBoard(nextBoard);
          setStatus(message || "Next move.");
          setIsLoading(false);
        }
      }
    } catch (error) {
      setStatus("Network error. Is the backend running?");
      setResultText("Error");
      setIsLoading(false);
    }
  };

  const resetGame = () => {
    setBoard(emptyBoard);
    setGameId(null);
    setComputerSymbol("O");
    setStatus("Choose a symbol and start a new game.");
    setResultText("Not started");
    setGameOver(false);
  };

  return (
    <div className="app">
      <Header />
      <div className="info-bar">
        <div>
          <span className="info-label">Result:</span>{" "}
          <span className="info-value info-value-inline">{resultText}</span>
        </div>
      </div>
      {!gameId && (
        <div className="controls">
          <input
            className="input"
            type="text"
            placeholder="Username"
            value={username}
            onChange={(event) => setUsername(event.target.value)}
          />
          <div className="symbol-select">
            <button
              className={playerSymbol === "X" ? "pill active" : "pill"}
              type="button"
              onClick={() => setPlayerSymbol("X")}
            >
              Play X
            </button>
            <button
              className={playerSymbol === "O" ? "pill active" : "pill"}
              type="button"
              onClick={() => setPlayerSymbol("O")}
            >
              Play O
            </button>
          </div>
          <button
            className="primary-button"
            type="button"
            onClick={startGame}
            disabled={isStartDisabled}
          >
            Start Game
          </button>
        </div>
      )}
      {gameOver && (
        <button
          className="primary-button restart-button"
          type="button"
          onClick={resetGame}
        >
          Restart Game
        </button>
      )}
      <div className="board-row">
        <div className="side-info left">
          <span className="info-label">
            {gameId && username ? username : "Your"} symbol:
          </span>{" "}
          <span className="info-value">{gameId ? playerSymbol : "-"}</span>
        </div>
        <GameBoard
          board={board}
          onCellClick={handleMove}
          disabled={isLoading || !gameId || gameOver}
        />
        <div className="side-info right">
          <span className="info-label">Computer symbol:</span>{" "}
          <span className="info-value">{gameId ? computerSymbol : "-"}</span>
        </div>
      </div>
    </div>
  );
}

export default App;
