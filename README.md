# aind-projects
Renier Botha's project submissions for Udacity's AI Nanodegree program

### Overview

This repo is a parent container for all my submissions (and attempts) to the projects in the [AIND](https://www.udacity.com/ai) program. 


### Project 1: Sudoku
TODOs:

* Add an image
* Write up the starting process - how to run the project
    * Sort out the gui
    

The objective was to write an AI agent to solve the game of `diagonal sudoku`. 


### Project 2: Isolation

TODOs:
* add links to description
* Write up the starting process

The goal of this project was to write an adversarial search agent to play the game of Isolation. The agent was written using the [MiniMax](link) algorithm combined with the [AlphaBeta](link) pruning algorithm for reducing the game tree search space. 

The student's needed to implement the MiniMax and AlphaBeta algorithms and additionally come up with three custom heuristics to evaluate game positions. 

Furthermore, this project includes a research review of Deep Mind's AlphaGO paper. 



### LAB 1: Pacman

Note that this project requires a python version of 2.7. Thus, it is recommended to create a new python environment using anaconda's cli tool: `conda`. Alternatively, activate your own python 2.7 env.


``` 
cd search
conda create -n conda2.7 python=2.7
source activate conda2.7 // or activate your own env
python pacman.py
```
