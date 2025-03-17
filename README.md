# FiguresPlease

An educational game designed to help students learn and practice identifying rhetorical figures through an interactive interface.

## Features

- Interactive game interface for practicing rhetorical figure identification
- Scoring system using sigmoid functions for adaptive difficulty
- Player statistics and leaderboard tracking
- Configurable settings for customizing the learning experience

## Getting Started

1. Launch the application by running `main.py`
2. Navigate using the three main tabs at the top:
   - 🖊 Game: Practice identifying rhetorical figures
   - 📖 Leaderboard: View player rankings and statistics
   - ⚙ Settings: Configure game parameters

## How to Play

1. Go to the Settings tab (⚙) and enter "Classe" in the text field
2. Click "Update" and select your list file ("list.txt") and play file ("play.txt") from the dropdown menus
3. Navigate to the Game tab (🖊) and click the "#" button
4. Select a player and the rhetorical figure of interest in the lower section of the screen
5. Press "V" for valid or "F" for invalid to indicate whether the player has correctly identified the rhetorical figure

## Requirements

- Python 3.x
- Tkinter (usually comes with Python)

## File Structure

- `main.py`: Main application code
- `path.txt`: Base path configuration
- `/pl/list.txt`: Rhetorical figures and scores
- `/gm/stats.txt`: Player statistics
- `output.txt`: Current turn data

## Contributing

Feel free to submit issues and enhancement requests!
