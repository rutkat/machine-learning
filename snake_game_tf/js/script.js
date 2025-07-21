const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const ONE = 1;
const SCALE = 40; 
const ROWS = 20;
const COLUMNS = 20;
const totalCells = ROWS * COLUMNS;
const bitMask = new Uint32Array(Math.ceil(totalCells / 32));
canvas.width = COLUMNS * SCALE;
canvas.height = ROWS * SCALE;

let snake;
let fruit;
let gameInterval;
let gameMode = 'manual';
let model;
let score = 0;
let speedDifficulty = 60;
let posX = 20;
let posY = 20;
let gameSize = 20;
let velocityX = 0;
let velocityY = 0;
let path = [];
let length = ONE;
let movementLog = [];
let currGen = 0;
let gameRunning = true;
let direction = ['left', 'forward', 'right'];
let xApple = Math.floor(Math.random() * gameSize);
let yApple = Math.floor(Math.random() * gameSize);
let loopsSinceApple = 0;

let startBtn = document.getElementById('startGame');
let modeBtn = document.getElementById('mode');
let restartBtn = document.getElementById('restartGame');
let elmScore = document.getElementById('score');

modeBtn.addEventListener('change', function() {
    gameMode = this.value;
});

startBtn.addEventListener('click', function() {
    if (gameMode === 'model') {
        gameSpeed = setInterval(game, speedDifficulty);
    } else {
        startGame();
    }
});

restartBtn.addEventListener('click', function() {
    resetGame();
});

function startGame() {
    score = 0;
    elmScore.innerText = score;
    startBtn.style.display = 'none';
    restartBtn.style.display = 'inline';
    setup();
}

function setup() {
    snake = [{ x: 5, y: 5 }];
    direction = { x: 1, y: 0 };
    clearBoard();
    setBit(snake[0].x, snake[0].y);
    placeFood();

    if (gameMode === 'model') {
        gameInterval = setInterval(gameLoopAI, 100);
    } else {
        gameInterval = setInterval(gameLoopManual, 100);
        window.addEventListener('keydown', changeDirection);
    }
}

function placeFood() {
    let x, y;
    do {
        x = Math.floor(Math.random() * COLUMNS);
        y = Math.floor(Math.random() * ROWS);
    } while (getBit(x, y));
    fruit = { x, y };
}

function gameLoopManual() {
    const head = { x: snake[0].x + direction.x, y: snake[0].y + direction.y };

    
    if (head.x < 0 || head.x >= COLUMNS || head.y < 0 || head.y >= ROWS) {
        gameOver();
        return;
    }

    if (checkCollision(head)) {
        gameOver();
        return;
    }

    snake.unshift(head);
    setBit(head.x, head.y);

    if (head.x === fruit.x && head.y === fruit.y) {
        score++;
        elmScore.innerText = score;
        placeFood();
    } else {
        const tail = snake.pop();
        clearBit(tail.x, tail.y);
    }
    
    draw();
}

function checkCollision(head) {
    return getBit(head.x, head.y) && !(head.x === snake[1]?.x && head.y === snake[1]?.y);
}

function changeDirection(event) {
    const { keyCode } = event;
    if (keyCode === 37 && direction.x === 0) {
        direction = { x: -1, y: 0 };
    } else if (keyCode === 38 && direction.y === 0) {
        direction = { x: 0, y: -1 };
    } else if (keyCode === 39 && direction.x === 0) {
        direction = { x: 1, y: 0 };
    } else if (keyCode === 40 && direction.y === 0) {
        direction = { x: 0, y: 1 };
    }
}

function reloadGame(event) {
    if (event.keyCode === 13) { 
        window.removeEventListener('keydown', reloadGame);
        setup();
    }
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    /* Snake color */
    ctx.fillStyle = 'white';
    snake.forEach(segment => {
        ctx.fillRect(segment.x * SCALE, segment.y * SCALE, SCALE, SCALE);
    });
    /* Feed color */
    ctx.fillStyle = '#EE6EFF';
    ctx.fillRect(fruit.x * SCALE, fruit.y * SCALE, SCALE, SCALE);
}

function setBit(x, y) {
    const index = y * COLUMNS + x;
    const arrayIndex = Math.floor(index / 32);
    const bitIndex = index % 32;
    bitMask[arrayIndex] |= 1 << bitIndex;
}

function clearBit(x, y) {
    const index = y * COLUMNS + x;
    const arrayIndex = Math.floor(index / 32);
    const bitIndex = index % 32;
    bitMask[arrayIndex] &= ~(1 << bitIndex);
}

function getBit(x, y) {
    const index = y * COLUMNS + x;
    const arrayIndex = Math.floor(index / 32);
    const bitIndex = index % 32;
    return (bitMask[arrayIndex] & (1 << bitIndex)) !== 0;
}

function clearBoard() {
    bitMask.fill(0);
}

function gameOver() {
    clearInterval(gameInterval);
    window.removeEventListener('keydown', changeDirection);
    alert('Game Over!');
}

function resetGame() {
    clearInterval(gameInterval);
    snake = [];
    direction = {};
    startBtn.style.display = 'inline';
    restartBtn.style.display = 'none';
}

function game() {
  /* AI Mode */
  posX += velocityX;
  posY += velocityY;

  if (velocityX !== 0 || velocityY !== 0) {
      gameRunning = true;
  }
  /* canvas background */
  ctx.fillStyle = "rgba(255, 255, 255, 0.5)";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.fillStyle = "#0C0";
  ctx.shadowBlur = 10;

  path.forEach(segment => {
      ctx.fillRect(segment.x * SCALE, segment.y * SCALE, SCALE - 2, SCALE - 2);
      if (gameRunning && segment.x === posX && segment.y === posY) {
          restartGame();
          return;
      }
  });

  path.push({ x: posX, y: posY });
  while (path.length > length) {
      path.shift();
  }

  movementLog.push(getPositionArray());
  processInput(computePrediction(getPositionArray()));

  if (posX < 0 || posX >= COLUMNS || posY < 0 || posY >= ROWS) {
      restartGame();
      return;
  }

  if (loopsSinceApple >= 75) {
      restartGame();
      return;
  }

  if (xApple === posX && yApple === posY) {
      loopsSinceApple = 0;
      length++;
      score++;
      placeApple();
  }

  ctx.fillStyle = "red"; /* #FF5733 */
  ctx.fillRect(xApple * SCALE, yApple * SCALE, SCALE - 2, SCALE - 2);

  elmScore.innerText = score;

  loopsSinceApple++;
}

function placeApple() {
  xApple = Math.floor(Math.random() * COLUMNS);
  yApple = Math.floor(Math.random() * ROWS);
}

function processInput(input) {

    if ( input == 'left') {
      if (velocityY == -1) { 
        velocityX = -1;
        velocityY = 0;
      } else if ( velocityY == 1) {
        velocityX = 1;
        velocityY = 0;
      } else if ( velocityX == -1) {
        velocityX = 0;
        velocityY = 1;
      } else {
        velocityX = 0;
        velocityY = -1;
      }

    } else if ( input == 'right'){
      if (velocityY == -1) { 
        velocityX = 1;
        velocityY = 0;
      } else if ( velocityY == 1) {
        velocityX = -1;
        velocityY = 0;
      } else if ( velocityX == -1) {
        velocityX = 0;
        velocityY = -1;
      } else {
        velocityX = 0;
        velocityY = 1;
      }
    } else if ( input == 'forward'){
      if ( velocityY == 0 && velocityX == 0) {
        velocityY = -1;
      }
    }
}
function restartGame() {
   gameRunning = false;
   length = ONE;
   score = 0;
   velocityX = 0;
   velocityY = 0;
   posX = 10;
   posY = 10;
   currGen++;
   trainNeuralNet(movementLog);
   loopsSinceApple = 0;
   movementLog = [];
}

function getPositionArray() {
  var arr = [0,0,0];
  var relApple = [0,0];
  if ( velocityY == -1 ) {

    if ( xApple < posX) {
      relApple[0] = -1;
    } else if (xApple == posX) {
      relApple[0] = 0;
    } else {
      relApple[0] = 1;
    }

    if ( yApple < posY) {
      relApple[1] = 1;
    } else if ( yApple == posY) {
      relApple[1] = 0;
    } else {
      relApple[1] = -1;
    }

    if ( posX == 0) {
      arr[0] = 1;
    }
    if ( posY == 0) {
      arr[1] = 1;

    }
    if ( posX == gameSize - 1) {
      arr[2] = 1;
    }
    for ( var i = 0; i < path.length; i++) {
      if ( path[i].x == posX - 1 && path[i].y == posY) {
        arr[0] = 1;
      }
      if ( path[i].x == posX && path[i].y == posY - 1) {
        arr[1] = 1;
      }
      if ( path[i].x == posX + 1 && path[i].y == posY) {
        arr[2] = 1;
      }
    }

  } else if ( velocityY == 1) {
    if ( xApple < posX) {
      relApple[0] = 1;
    } else if (xApple == posX) {
      relApple[0] = 0;
    } else {
      relApple[0] = -1;
    }

    if ( yApple < posY) {
      relApple[1] = -1;
    } else if ( yApple == posY) {
      relApple[1] = 0;
    } else {
      relApple[1] = 1;
    }

    if ( posX == gameSize - 1) {
      arr[0] = 1;
    }
    if ( posY == gameSize - 1) {
      arr[1] = 1;
    }
    if ( posX == 0) {
      arr[2] = 1;
    }
    for ( var i = 0; i < path.length; i++) {

      if ( path[i].x == posX + 1 && path[i].y == posY) {
        arr[0] = 1;
      }
      if ( path[i].x == posX && path[i].y == posY + 1) {
        arr[1] = 1;
      }

      if ( path[i].x == posX - 1 && path[i].y == posY) {
        arr[2] = 1;
      }
    }

  } else if ( velocityX == -1) {

    if ( xApple < posX) {
      relApple[1] = -1;
    } else if (xApple == posX) {
      relApple[1] = 0;
    } else {
      relApple[1] = 1;
    }

    if ( yApple < posY) {
      relApple[0] = 1;
    } else if ( yApple == posY) {
      relApple[0] = 0;
    } else {
      relApple[0] = -1;
    }

    if ( posY == gameSize - 1) {
      arr[0] = 1;
    }
    if ( posX == 0) {
      arr[1] = 1;
    }
    if ( posY == 0) {
      arr[2] = 1;
    }
    for ( var i = 0; i < path.length; i++) {

      if ( path[i].x == posX && path[i].y == posY + 1) {
        arr[0] = 1;
      }

      if ( path[i].x == posX - 1 && path[i].y == posY) {
        arr[1] = 1;
      }

      if ( path[i].x == posX && path[i].y == posY - 1) {
        arr[2] = 1;
      }
    }
  } else if ( velocityX == 1){

    if ( xApple < posX) {
      relApple[1] = 1;
    } else if (xApple == posX) {
      relApple[1] = 0;
    } else {
      relApple[1] = -1;
    }

    if ( yApple < posY) {
      relApple[0] = -1;
    } else if ( yApple == posY) {
      relApple[0] = 0;
    } else {
      relApple[0] = 1;
    }

    if ( posY == 0) {
      arr[0] = 1;
    }
    if ( posX == gameSize - 1) {
      arr[1] = 1;
    }
    if ( posY == gameSize - 1) {
      arr[2] = 1;
    }


    for ( var i = 0; i < path.length; i++) {
      if ( path[i].x == posX && path[i].y == posY - 1) {
        arr[0] = 1;
      }
      if ( path[i].x == posX + 1 && path[i].y == posY) {
        arr[1] = 1;
      }
      if ( path[i].x == posX && path[i].y == posY + 1) {
        arr[2] = 1;
      }
    }
  } else {
    
    if ( xApple < posX) {
      relApple[0] = -1;
    } else if (xApple == posX) {
      relApple[0] = 0;
    } else {
      relApple[0] = 1;
    }

    if ( yApple < posY) {
      relApple[1] = -1;
    } else if ( yApple == posY) {
      relApple[1] = 0;
    } else {
      relApple[1] = 1;
    }
  }

  arr.push(relApple[0]);
  arr.push(relApple[1]);
  
  
  return arr;
}

function deriveExpectedMove(arr) {
  const [left, forward, right, appleX, appleY] = arr;
  
  // Priority: avoid collisions first
  if (left && forward) return 2; // right
  if (left && right) return 1;   // forward  
  if (forward && right) return 0; // left
  
  // Single obstacle cases
  if (left) return appleX === 1 ? 2 : (appleY === -1 ? 2 : 1);
  if (forward) return appleX === 1 ? 2 : 0;
  if (right) return appleX === -1 ? 0 : (appleY === -1 ? 0 : 1);
  
  // No obstacles - follow apple
  return appleX === -1 ? 0 : (appleX === 0 ? (appleY === -1 ? 0 : 1) : 2);
}
