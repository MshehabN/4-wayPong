# 4-Way Pong

A 4-way pong game where two players control paddles on all four sides of the screen.

## Features

- 2-player gameplay
- 4 paddles (top, bottom, left, right)
- Lives system (3 lives per player)
- Menu screen with instructions

## Controls

**Player 1:**
- Top Paddle: `A` / `D` keys
- Left Paddle: `W` / `S` keys

**Player 2:**
- Bottom Paddle: `Left Arrow` / `Right Arrow` keys
- Right Paddle: `Up Arrow` / `Down Arrow` keys

## Installation

1. Install Python 3.6 or higher
2. Install pygame:
   ```
   pip install -r requirements.txt
   ```

## How to Run

```
python main.py
```

## How to Play

- Press `SPACE` to start the game
- Each player starts with 3 lives
- You lose a life when the ball goes out of bounds on your side
- Game ends when a player runs out of lives
- Press `ESC` to return to menu during gameplay
