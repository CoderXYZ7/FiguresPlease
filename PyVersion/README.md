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

## Game Rules

### Setup

1. Each student (player) is assigned an ID number from the play.txt file
2. The game focuses on identifying rhetorical figures listed in the list.txt file
3. Each rhetorical figure has an associated difficulty score (initially set to 15.0)

### Rounds

1. During a game session, students take turns identifying rhetorical figures in texts
2. The teacher or game moderator loads or types the text sample in the main text area
3. When a student attempts to identify a rhetorical figure, the moderator:
   - Selects the student from the player dropdown
   - Selects the rhetorical figure from the figure dropdown
   - Clicks "V" if the identification is correct or "F" if incorrect

### Scoring System

1. The game tracks each student's performance with specific rhetorical figures
2. Scores are recorded in the stats.txt file and displayed on the Leaderboard tab
3. Correct identifications (V) increase a student's proficiency with that figure
4. Incorrect identifications (F) decrease proficiency
5. The difficulty score for each figure adjusts dynamically based on student performance
6. Use "Fine Round" button to end the current round and update all statistics

### Leaderboard

1. The Leaderboard tab displays student performance across all rhetorical figures
2. Statistics are formatted as rows with student IDs and columns with score values
3. Click "Update" to refresh the leaderboard with the latest data

### File Management

- Use "Salva" (Save) to save the current text to a file
- Use "Carica" (Load) to load existing text examples

## Requirements

- Python 3.x
- Tkinter (usually comes with Python)

## File Structure

- `main.py`: Main application code
- `path.txt`: Base path configuration
- `/pl/list.txt`: Rhetorical figures and scores
- `/gm/stats.txt`: Player statistics
- `/gm/play.txt`: Player list with IDs
- `output.txt`: Current turn data

## Tips for Teachers

1. Prepare a variety of text examples featuring different rhetorical figures
2. Organize competitive rounds to increase student engagement
3. Use the leaderboard to identify which figures students struggle with most
4. Adjust game difficulty by modifying the values in list.txt
5. End each session with "Fine Round" to ensure all statistics are properly saved

## Contributing

Feel free to submit issues and enhancement requests!
