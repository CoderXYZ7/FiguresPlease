// script.js
let players = [];
let figures = [];
let story = [];
let scores = {};

// Sigmoid function for dynamic difficulty adjustment
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
    figures.push({ name: figureName, difficulty: 0.5 }); // Start with medium difficulty
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

// Update score and difficulty
function updateScore(player, figure, isCorrect) {
  const figureObj = figures.find(f => f.name === figure);
  if (figureObj) {
    // Adjust difficulty based on correctness
    const delta = isCorrect ? -0.1 : 0.1; // Adjust this value for faster/slower learning
    figureObj.difficulty = sigmoid(figureObj.difficulty + delta);

    // Ensure difficulty stays within bounds (0 to 1)
    figureObj.difficulty = Math.max(0, Math.min(1, figureObj.difficulty));

    // Update player score: value = difficulty
    scores[player] += figureObj.difficulty;

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
    `<li>${figure.name} (Difficulty: ${figure.difficulty.toFixed(2)}, Value: ${figure.difficulty.toFixed(2)})</li>`
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