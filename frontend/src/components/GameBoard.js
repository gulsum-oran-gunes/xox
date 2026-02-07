import React from "react";

const emptyBoard = Array.from({ length: 9 }, () => "");

function GameBoard({ board = emptyBoard, onCellClick, disabled }) {
  return (
    <div className="board">
      {board.map((cell, index) => {
        const symbolClass =
          cell === "X" ? "symbol x" : cell === "O" ? "symbol o" : "symbol";

        return (
          <button
            className={cell ? "cell filled" : "cell"}
            key={index}
            type="button"
            onClick={() => onCellClick?.(index)}
            disabled={disabled || Boolean(cell)}
            aria-label={`Cell ${index + 1}`}
          >
            <span className={symbolClass} aria-hidden="true" />
          </button>
        );
      })}
    </div>
  );
}

export default GameBoard;
