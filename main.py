from tkinter import Tk, BOTH, Canvas
from time import sleep
from basic_types import *
from window import Window
from graphics import Maze

win = Window(1000, 1000, "hello")
maze = Maze(30, 30, 5, 5, 30, 30, win)
maze.solve()
win.wait_for_close()
