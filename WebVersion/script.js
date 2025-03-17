// script.js
let players = [];
let figures = [];
let story = [];
let scores = {};

// Sigmoid function for dynamic value adjustment
function sigmoid(x) {
  return 1 / (1 + Math.exp(-x));
}

// Add player
document.getElementById('add-player').addEventListener('click', () => {
  const playerName = document.getElementById('player-name').value;
  if (playerName) {
    players.push(playerName);
    scores[playerName] = 0;
    updatePlayerList();
    updatePlayerSelect();
    document.getElementById('player-name').value = '';
  }
});

// Add figure
document.getElementById('add-figure').addEventListener('click', () => {
  const figureName = document.getElementById('figure-name').value;
  if (figureName) {
    figures.push({ name: figureName, value: 0.5 }); // Start with medium value
    updateFigureList();
    updateFigureSelect();
    document.getElementById('figure-name').value = '';
  }
});

// Submit sentence
document.getElementById('submit-sentence').addEventListener('click', () => {
  const sentence = document.getElementById('sentence-input').value;
  if (sentence) {
    story.push(sentence);
    updateStoryDisplay();
    document.getElementById('sentence-input').value = '';
  }
});

// Mark correct/incorrect
document.getElementById('mark-correct').addEventListener('click', () => {
  const player = document.getElementById('player-select').value;
  const figure = document.getElementById('figure-select').value;
  updateScore(player, figure, true);
});

document.getElementById('mark-incorrect').addEventListener('click', () => {
  const player = document.getElementById('player-select').value;
  const figure = document.getElementById('figure-select').value;
  updateScore(player, figure, false);
});

// Update score and value
function updateScore(player, figure, isCorrect) {
  const figureObj = figures.find(f => f.name === figure);
  if (figureObj) {
    // Update player score
    if (isCorrect) {
      scores[player] += figureObj.value; // Add value to player's score
      figureObj.value = sigmoid(figureObj.value - 1); // Decrease value
    } else {
      scores[player] -= figureObj.value; // Subtract value from player's score
      figureObj.value = sigmoid(figureObj.value + 1); // Increase value
    }

    // Ensure value stays within bounds (0 to 1)
    figureObj.value = Math.max(0, Math.min(1, figureObj.value));

    // Update UI
    updateFigureList();
    updateScoreList();
  }
}

// Save game state
document.getElementById('save-game').addEventListener('click', () => {
  const gameState = { players, figures, story, scores };
  localStorage.setItem('gameState', JSON.stringify(gameState));
});

// Load game state
document.getElementById('load-game').addEventListener('click', () => {
  const gameState = JSON.parse(localStorage.getItem('gameState'));
  if (gameState) {
    players = gameState.players;
    figures = gameState.figures;
    story = gameState.story;
    scores = gameState.scores;
    updatePlayerList();
    updateFigureList();
    updateStoryDisplay();
    updateScoreList();
    updatePlayerSelect();
    updateFigureSelect();
  }
});

// Helper functions to update UI
function updatePlayerList() {
  const list = document.getElementById('player-list');
  list.innerHTML = players.map(player => `<li>${player}</li>`).join('');
}

function updateFigureList() {
  const list = document.getElementById('figure-list');
  list.innerHTML = figures.map(figure => 
    `<li>${figure.name} (Value: ${figure.value.toFixed(2)})</li>`
  ).join('');
}

function updateStoryDisplay() {
  const display = document.getElementById('story-display');
  display.innerHTML = story.map((sentence, index) => `<p>${index + 1}. ${sentence}</p>`).join('');
}

function updateScoreList() {
  const list = document.getElementById('score-list');
  list.innerHTML = Object.entries(scores).map(([player, score]) => 
    `<li>${player}: ${score.toFixed(2)}</li>`
  ).join('');
}

function updatePlayerSelect() {
  const select = document.getElementById('player-select');
  select.innerHTML = players.map(player => `<option value="${player}">${player}</option>`).join('');
}

function updateFigureSelect() {
  const select = document.getElementById('figure-select');
  select.innerHTML = figures.map(figure => `<option value="${figure.name}">${figure.name}</option>`).join('');
}