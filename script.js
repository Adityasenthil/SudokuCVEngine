
const grid = document.querySelector('.SudokuGrid');
const panel = document.querySelector('.ButtonRow')
let puzzleInts = [1,2,3,4,5,6,7,8,9];
  

for (let i = 0; i < 81; i++) {
  const cell = document.createElement('input');
  cell.type = 'text';
  cell.maxLength = 1;
  cell.classList.add("cell");
  grid.appendChild(cell);
}


const scanButton = document.querySelector(".btn-scan");
const startButton = document.querySelector(".btn-start");
const cells = document.querySelectorAll('.cell');



startButton.addEventListener('click' , () => {
  scanButton.remove();
  startButton.remove();

  const hintButton = document.createElement('button');
  hintButton.textContent = "Hint"; 
  panel.appendChild(hintButton);
  

  const checkButton = document.createElement('button');
  checkButton.textContent = "Check"; 
  panel.appendChild(checkButton);
  
  const currGrid = [];

  for (let i = 0; i < 9; i++){
    const row = [];
    for (let j = 0; j < 9; j++){
      const val = cells[i * 9 + j].value;
      row.push(val === "" ? 0 : parseInt(val, 10));
    }
    currGrid.push(row);
  }

  fetch('http://localhost:8000/save', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ puzzle: currGrid })
  })

  hintButton.addEventListener('click', async () => {
    const response = await fetch('http://localhost:8000/hint');
    const hint = await response.json();
    cells[hint.row * 9 + hint.col].style.border = '2px solid gold';
    
    setTimeout(() => {
      cells.style.border = "1px solid black";
    }, 1000);
      
    return;
  });

  



  checkButton.addEventListener('click', async() => {
    const response = await fetch('http://localhost:8000/solve');
    const solved = await response.json();
    checkPuzzle(solved.solution);
    return;
  });


});



scanButton.addEventListener('click', async () => {
  console.log('Starting scan...');

  const scanResponse = await fetch('http://localhost:8000/scan');
  if (!scanResponse.ok) {
    console.error('Scan request failed:', scanResponse.status);
    return;
  }
  console.log('Scanned Successfully');

  for (let attempt = 1; attempt <= 10; attempt++) {
    console.log(`Polling for result, attempt ${attempt}...`);
    const resultResponse = await fetch('http://localhost:8000/result');

    if (!resultResponse.ok) {
      console.error('Result request failed:', resultResponse.status);
    } else {
      const puzzle = await resultResponse.json();
      if (puzzle.status !== "No puzzle scanned yet. Please call /scan first.") {
        populatePuzzle(puzzle.puzzle);
        puzzleInts = puzzle.puzzle.map(row => row.map(cell => parseInt(cell, 10)));
        return;

      }
  }

    await new Promise(res => setTimeout(res, 4000)); // wait 2 seconds before next attempt
  }

  console.error('Polling timeout: result not ready');
});


function checkPuzzle(puzzle){
  for (let i = 0; i < 9; i++){
    for (let j = 0; j < 9; j++){
      const val = cells[i * 9 + j].value;
      if (val != "" && puzzle[i][j] != val){
        cells[i * 9 + j].style.color = 'red'; 
      }
      if (val != "" && puzzle[i][j] == val){
        cells[i * 9 + j].style.color = 'black'; 
      }
    }
  }
}



function populatePuzzle(puzzle){
  for (let i = 0; i < 9; i++){
    for (let j = 0; j < 9; j++){
        if (puzzle[i][j] == 0)
          cells[i * 9 + j].value = "";
        else
          cells[i * 9 + j].value = puzzle[i][j];
    }
  }
}


