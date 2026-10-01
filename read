# Smart Circuit & PCB Trace Short-Circuit Finder

A Python-based project that uses a Stack (LIFO - Last In, First Out) to detect short circuits in a PCB trace grid.

## Problem Statement
In PCB design, even a small accidental connection between a copper trace and a power or ground rail can create a short circuit. Manual trace inspection is time-consuming and error-prone, especially in dense boards. This project automates the process by representing the PCB as a 2D grid and traversing it using a stack-based depth-first search.

## PCB Grid Representation
- 0 = Empty fiberglass
- 1 = Valid copper trace
- 2 = Short-circuit node

## Stack Logic
We use a stack to simulate DFS:
1. Push the starting coordinate
2. Pop the top coordinate
3. Check if the cell is a short-circuit node
4. Visit neighbors if the cell is a valid trace
5. Push unvisited valid neighbors onto the stack
6. Repeat until the short is found or the stack becomes empty

## Project Structure
- `stack_engine.py` — Stack implementation and DFS logic
- `main.py` — Tkinter GUI visualizer
- `test_boards/` — Safe and faulty PCB test cases
- `README.md` — Project documentation

## How to Run
1. Clone the repo:
   ```bash
   git clone https://github.com/your-username/smart-circuit-pcb-finder.git
   cd smart-circuit-pcb-finder
