# Welcome to Tic-Tac-Terminal! # 

# Tic-Tac-Toe AI Simulation Project

This project is a configurable Tic-Tac-Toe styled board game engine with support for:
- Human vs Human
- Human vs Computer
- Computer vs Computer
- Headless simulation for AI training
- Reinforcement Learning (RL) and offline experience collection

It is structured to support experimentation with different rules, boards, pieces for gameplay
And it also supports experimentation with various ML models (with policies/agents being untied), reward schemes, and state encodings.

---

## Features

- Configurable board size
- Randomized or fixed starting player
- Multiple AI policies and agents
- Online and offline reinforcement learning
- CLI and headless modes
- Experience dataset generation for RL
- Reward and state encoding registries for modularity

---

## How to use

All configuration is done through the config file.  If you build your version of anything tied to a registry,
follow that registries format and name your build, this name will then be usable through config.
(See config for more config details and explanations)

## Installation

Requires Python 3.12 or later.
Requires Numpy (suggested use is to place the project within a Virtual Environment)

## Usage
Run with python3 main.py from project root

## General Project Structure
main.py - Entry point
config.py - Game configuration

game_engine/ - Basic Game logic and creation
game_types/ - Rule definitions and registries
players/ - Human and computer player logic

core/ - Game state and move handling
simulation/ - Engine, training, encoding, rewards

runtime/cli_runtime.py - CLI gameplay interface
renderers/cli_renderer.py - CLI visual output


## Notes
If you want to use the rendered version to either watch simulated games or play yourself,
You MUST use a terminal that support curses and basic colors.
If you run with TERM=dumb or and equivalant terminal, it will break and it is your fault.

Some great puns which essentially inspired this whole project
Tic-Tac Terminated, tty1 - tic tac your terminal