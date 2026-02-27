# Night Economy Taxi Agent — Smart City AI Simulation

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🌙 Project Overview
This project implements a **Multi-Agent System (MAS)** rational AI taxi fleet designed for the London "Night Economy." Operating on a **5x5 grid-based** simulation of Central London, the agents coordinate via a centralized dispatcher to efficiently transport passengers while navigating road closures and demand hotspots.

Developed for the **Artificial Intelligence (CMP-N206-0)** module at the University of Roehampton.

## 🚀 Key Features
- **Coordination Logic:** Centralized Nearest-Neighbor Dispatch for multi-agent efficiency.
- **Search Strategies:** Informed (A*) and Uninformed (BFS) pathfinding.
- **Explainability:** Real-time reasoning logs explaining every agent decision.
- **Environment Modelling:** 5x5 London Grid with dynamic road closures and surge zones.
- **Rationality:** Goal-based agents optimizing a robust performance measure (utility function).

## 🛠️ Tech Stack
- **Language:** Python
- **Libraries:** NumPy, Matplotlib, Collections, Heapq
- **Format:** Jupyter Notebook (`.ipynb`) and Academic Report (`.md`)

## 📊 Performance Comparison (5x5 Grid)
| Metric | Single-Agent | Multi-Agent Fleet |
| :--- | :--- | :--- |
| **Parallel Steps** | 43 | **20** |
| **Efficiency Gain** | - | **~50%** |

## 📁 Repository Structure
- `Baburam_Bastola_Taxi_Agent.ipynb`: Main simulation notebook (MAS Version).
- `Baburam_Bastola_Taxi_Agent_Report.md`: Full academic case study analysis.
- `assets/`: Diagram assets (Wireframes, UML, Activity, Sequence, ERD).

## 📝 Author
**Baburam Bastola**  
BSc Computer Science  
Student ID: A00022220  

---
*This repository is for educational purposes as part of the University of Roehampton AI Assessment.*
