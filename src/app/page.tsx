'use client';
import React, { useState, useEffect } from 'react';

export default function Home() {
  const [board, setBoard] = useState(Array(9).fill(null));
  const [isPlayerTurn, setIsPlayerTurn] = useState(true);
  const [message, setMessage] = useState("Think you can beat me? Go ahead, I'll wait... 😏");
  const [gameOver, setGameOver] = useState(false);
  const [winner, setWinner] = useState(null);

  const winPatterns = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
  ];

  const teasingMessages = [
    "Bold move! Too bad it won't save you 🎭",
    "Interesting... are you sure about that? 🤔",
    "Oh wow, didn't see that coming! Just kidding, I did 😎",
    "That's your strategy? Adorable! 💅",
    "Hmm, playing it safe? Boring! 😴",
    "Ooh, getting creative! Still gonna lose though 🎨",
    "Is that the best you got? 🥱",
    "Nice try, but I've calculated 47 ways you lose from here 🤓"
  ];

  const losingMessages = [
    "Wait... WHAT?! This can't be happening! 😱",
    "You cheated! There's no way... I NEVER LOSE! 😤",
    "This is just... I let you win. Yeah, that's it! 🙄",
    "Okay fine, you won. But I wasn't even trying! 😒",
    "Unbelievable... I need to recalibrate my circuits 🤖💔",
    "You got lucky! REMATCH! NOW! 😡",
    "I'm not crying, YOU'RE crying! 😭",
    "This is embarrassing... don't tell anyone about this 😳"
  ];

  const drawMessages = [
    "A draw? I'll take it. Could've been worse! 😅",
    "Stalemate... I guess you're not terrible 🤷",
    "We're equally matched! (But I'm still better) 😏",
    "Tie game! Want to go again and actually win? 😈"
  ];

  const checkWinner = (currentBoard: any[]) => {
    for (let pattern of winPatterns) {
      const [a, b, c] = pattern;
      if (currentBoard[a] && currentBoard[a] === currentBoard[b] && currentBoard[a] === currentBoard[c]) {
        return { winner: currentBoard[a], pattern };
      }
    }
    if (currentBoard.every(cell => cell !== null)) {
      return { winner: 'draw', pattern: [] };
    }
    return null;
  };

  const computerMove = (currentBoard: any[]) => {
    const availableMoves = currentBoard.map((cell, idx) => cell === null ? idx : null).filter(idx => idx !== null);
    
    for (let move of availableMoves) {
      const testBoard = [...currentBoard];
      testBoard[move] = 'O';
      if (checkWinner(testBoard)?.winner === 'O') return move;
    }
    
    for (let move of availableMoves) {
      const testBoard = [...currentBoard];
      testBoard[move] = 'X';
      if (checkWinner(testBoard)?.winner === 'X') return move;
    }
    
    if (availableMoves.includes(4)) return 4;
    
    const corners = [0, 2, 6, 8].filter(idx => availableMoves.includes(idx));
    if (corners.length > 0) return corners[Math.floor(Math.random() * corners.length)];
    
    return availableMoves[Math.floor(Math.random() * availableMoves.length)];
  };

  useEffect(() => {
    if (!isPlayerTurn && !gameOver) {
      const timer = setTimeout(() => {
        const newBoard = [...board];
        const move = computerMove(newBoard);
        newBoard[move] = 'O';
        setBoard(newBoard);
        
        const result = checkWinner(newBoard);
        if (result) {
          handleGameEnd(result);
        } else {
          setIsPlayerTurn(true);
        }
      }, 600);
      return () => clearTimeout(timer);
    }
  }, [isPlayerTurn, gameOver, board]);

  const handleGameEnd = (result: React.SetStateAction<null>) => {
    setGameOver(true);
    setWinner(result);
    
    if (result.winner === 'X') {
      setMessage(losingMessages[Math.floor(Math.random() * losingMessages.length)]);
    } else if (result.winner === 'O') {
      setMessage("HAHA! I WIN! Told you I'm unbeatable! 🎉👑");
    } else {
      setMessage(drawMessages[Math.floor(Math.random() * drawMessages.length)]);
    }
  };

  const handleClick = (index) => {
    if (board[index] || !isPlayerTurn || gameOver) return;
    
    const newBoard = [...board];
    newBoard[index] = 'X';
    setBoard(newBoard);
    
    const result = checkWinner(newBoard);
    if (result) {
      handleGameEnd(result);
    } else {
      setMessage(teasingMessages[Math.floor(Math.random() * teasingMessages.length)]);
      setIsPlayerTurn(false);
    }
  };

  const resetGame = () => {
    setBoard(Array(9).fill(null));
    setIsPlayerTurn(true);
    setGameOver(false);
    setWinner(null);
    setMessage("Ready for another beating? Let's go! 😈");
  };

  return (
    <>
      <div
        aria-hidden
        className="pointer-events-none fixed inset-0 z-0 overflow-hidden"
        style={{ backgroundColor: "#000D2E" }}
      >
        <div
          className="absolute left-[-25%] top-[120px] h-[180px] w-[150%] opacity-90 blur-[70px]"
          style={{
            background: "linear-gradient(90deg, rgba(111,0,255,0.8) 8%, rgba(99,255,188,0.88) 88%)",
            transform: "rotate(6deg)",
          }}
        />
        <div
          className="absolute left-[-25%] top-[560px] h-[180px] w-[150%] opacity-90 blur-[70px]"
          style={{
            background: "linear-gradient(90deg, rgba(111,0,255,0.8) 8%, rgba(99,255,188,0.88) 88%)",
            transform: "rotate(6deg)",
          }}
        />
      </div>

      <main className="relative z-10 flex min-h-screen flex-col items-center px-6 pb-20 text-center font-sans text-white">
        
        <div className="mt-10 mb-12 sm:mt-12 sm:mb-16">
          <div className="text-4xl sm:text-5xl md:text-6xl font-bold bg-gradient-to-r from-purple-400 to-teal-300 bg-clip-text text-transparent">
            HackFlix
          </div>
        </div>

        <div className="flex flex-col items-center mb-12">
          <h1 className="font-semibold tracking-tight text-[42px] sm:text-[56px] md:text-[72px]">
            Welcome to HackFlix
          </h1>
          <h2 className="mt-4 opacity-90 tracking-tight text-[28px] sm:text-[36px] md:text-[48px]">
            Coming Soon!
          </h2>
        </div>

        <div className="w-full max-w-md mx-auto mt-8">
          <div className="bg-white/5 backdrop-blur-lg rounded-3xl p-6 sm:p-8 border border-white/10 shadow-2xl">
            
            <div className="mb-6 pb-6 border-b border-white/10">
              <p className="text-base sm:text-lg text-white/80 leading-relaxed">
                🍳 <span className="text-teal-300 font-semibold">Our website is cooking in the kitchen...</span>
                <br />
                <span className="text-sm sm:text-base text-white/60">Meanwhile, try beating our AI at Tic-Tac-Toe! (Spoiler: You won't 😏)</span>
              </p>
            </div>

            <div className="mb-6 min-h-[60px] sm:min-h-[70px] flex items-center justify-center">
              <p className="text-base sm:text-lg text-white/90 px-4 leading-relaxed">
                {message}
              </p>
            </div>

            <div className="grid grid-cols-3 gap-2 sm:gap-3 mb-6 max-w-[320px] mx-auto">
              {board.map((cell, index) => (
                <button
                  key={index}
                  onClick={() => handleClick(index)}
                  disabled={!isPlayerTurn || gameOver || cell !== null}
                  className={`
                    aspect-square rounded-xl sm:rounded-2xl text-4xl sm:text-5xl font-bold
                    transition-all duration-200 transform
                    ${cell === null && isPlayerTurn && !gameOver
                      ? 'bg-white/10 hover:bg-white/20 hover:scale-105 cursor-pointer'
                      : 'bg-white/5 cursor-not-allowed'
                    }
                    ${winner?.pattern?.includes(index) ? 'bg-gradient-to-br from-purple-500/40 to-teal-500/40 animate-pulse' : ''}
                    border border-white/10 shadow-lg
                  `}
                >
                  <span className={cell === 'X' ? 'text-teal-300' : 'text-purple-400'}>
                    {cell}
                  </span>
                </button>
              ))}
            </div>

            {gameOver && (
              <button
                onClick={resetGame}
                className="w-full py-3 sm:py-4 rounded-xl sm:rounded-2xl font-bold text-base sm:text-lg
                         bg-gradient-to-r from-purple-500 to-teal-400 
                         hover:from-purple-600 hover:to-teal-500
                         transform hover:scale-105 transition-all duration-200
                         shadow-lg"
              >
                Play Again
              </button>
            )}

            {!gameOver && (
              <div className="text-center text-white/50 text-sm sm:text-base">
                {isPlayerTurn ? "Your turn (X)" : "AI is thinking... (O)"}
              </div>
            )}
          </div>
        </div>

        <div className="mt-12 text-white/40 text-xs sm:text-sm">
          Stay tuned for something epic! 🚀
        </div>
      </main>
    </>
  );
}