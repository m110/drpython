# drpython

Open source clone of Dr. Mario game for NES, written in Python with Pygame

This is a side-project written for fun, but aiming to provide readable and an easy to grasp example of writing a game from scratch, along with documentation and unit tests.

## Draft

The game board is a 8x16 rectangle. Each cell can hold a half of medical capsule or a virus. Either way, it can be red, blue, yellow or clear. Instead of handling the falling pill, the board simply manages each cell, setting its color and so on.

## TODO
- [ ] Add viruses
- [ ] Check for matches when blocks fall down
- [ ] Complete unit tests
- [ ] Speed up as time passes
- [ ] Proper game over handling
- [ ] Look & Feel (sounds, actual graphics)
- [ ] Scoring system
- [ ] Multiple difficulties
