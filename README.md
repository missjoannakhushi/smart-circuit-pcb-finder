# ⚡ TraceStack: Advanced PCB Trace & Short-Circuit Fault Isolation System

> **🚀 LIVE WEB DEMO:** [Click here to test the project live in your browser!](https://smart-circuit-pcb-finder-aqyjebzpkyvbtwgraiwsapp.streamlit.app)

---

## 📌 Project Overview
**TraceStack** is a data structures project designed to solve a critical hardware engineering problem: tracing conductive copper paths on Printed Circuit Boards (PCBs) to detect and isolate unintended short-circuit faults. 

Instead of manual multimeters or visual inspections, this system utilizes a programmatic **Stack-based graph traversal (DFS)** algorithm to simulate automated circuit continuity scans.

---

## 🛠️ Data Structures & Algorithms Used
* **Stack (LIFO - Last In, First Out):** Manages the traversal frontier using Depth-First Search, allowing the algorithm to dive deep into complex circuit branches sequentially.
* **Visited Set (`O(1)` Lookups):** Keeps track of explored nodes to prevent infinite loops during traversal.
* **Dynamic 2D Matrix (Grid Representation):** Represents PCB cells where:
  * `0` = Empty / Non-conductive space (Dark background)
  * `1` = Clean Copper Trace (Green)
  * `2` = Short-Circuit Fault (Red/Purple)

---

## ✨ Key Features
* **Dynamic Random Circuit Generation:** Generates organic, unique copper trace layouts and short-circuit fault positions on the fly.
* **Multi-Fault Isolation:** Traverses the entire network to flag multiple short circuits rather than stopping blindly at the first fault.
* **Dual Presentation Options:** Fully playable as an instant web app via Streamlit or as a local desktop app via Python/Tkinter.

---

## 💻 How to Run Locally

If you wish to run the desktop application version on your machine:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/missjoannakhushi/smart-circuit-pcb-finder.git](https://github.com/missjoannakhushi/smart-circuit-pcb-finder.git)
   cd smart-circuit-pcb-finder
