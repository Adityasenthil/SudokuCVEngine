from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import subprocess
import os
import json
from solution import iterate_puzzle
from solution import generateCandidates

app = FastAPI()

origins = [
    "http://localhost:8000",
]

# Enable CORS if frontend calls API from same origin (optional if served together)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace * with your frontend domain for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





@app.get("/scan")
def scan_sudoku():
    if os.path.exists("last_puzzle.json"):
        os.remove("last_puzzle.json")
    subprocess.Popen(["python3", "solver.py"])  # Run your solver in background
    return {"status": "Started scanning in separate process. Check your webcam window."}

@app.get("/result")
def get_result():
    if os.path.exists("last_puzzle.json"):
        with open("last_puzzle.json", "r") as f:
            puzzle = json.load(f)
            return JSONResponse(content={"puzzle": puzzle})
    else:
        return {"status": "No puzzle scanned yet. Please call /scan first."}



@app.post("/save")
async def save(request: Request):
    data = await request.json()
    puzzle = data.get('puzzle')
    with open("last_puzzle.json", "w") as f:
        json.dump(puzzle, f)  


@app.get("/hint")
async def save(request: Request):
    with open("last_puzzle.json", "r") as f:
        puzzle = json.load(f)
    
    puzzle = [[int(x) for x in row] for row in puzzle]

    i, j, value, type = generateCandidates(puzzle)

    return {"row": i, "col": j, "value": value, "type": type}



@app.get("/solve")
def solve():
    with open("last_puzzle.json", "r") as f:
        puzzle = json.load(f)

    puzzle_sol = [[int(x) for x in row] for row in puzzle]

    iterate_puzzle(puzzle_sol)

    return {"solution": puzzle_sol}


app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
