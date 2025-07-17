Sudoku Engine

This project uses Computer Vision to scan Sudoku puzzles, replicate grid on screen, and can: 
a) check current progress
b) provide complete solution
c) hints at the next square to be filled (currently using naked singles)

Features
Live Puzzle capture with inactivity-based scanning (registers image with ~3 seconds of inactivity)
Uses Backtracking to solve puzzle
Custom keras model to detect numbers

Tech Stack
OpenCV
NumPy
FastAPI
Python
HTML/CSS/JS 
