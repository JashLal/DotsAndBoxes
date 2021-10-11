# Dots and Boxes

Dots and Boxes is a simple, two-person game that starts with a grid of dots. Players take turns filling edges between adjacent dots. If a player fills in the fourth edge of a 1x1 box, they obtain a point and get to move again. The winner is the player with the most points.

This is a Python program that implements Dots and Boxes bot. Users can play against the bot on a Linux terminal. Currently, the bot uses a deterministic search algorithm; however, a bot trained with reinforcment learning is in progress.

## Setup
The program uses curses to display the board in a terminal. This comes standard with the Linux distrubution of Python3, but not the Windows version.
### Install curses in Windows
Enter the command below to install curses in Windows.
```
pip install windows-curses
```

## Usage
To run the project with default settings (4x5 board in singleplayer mode), run the following command in the root directory.
```
python3 -m  src
```
Specify the number of rows and columns with the optional flags shown below.
```
python3 -m src --rows 3 --cols 3
```
Provide the -m flag for multiplayer mode (to play against another person). Omitting the flag defaults the game to singleplayer mode.
```
python3 -m src -m
```
## Credits
The GUI was adapted from Stephen Roller's implementation of the game. Check it out at https://gist.github.com/stephenroller/3163995.
