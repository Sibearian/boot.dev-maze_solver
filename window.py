from tkinter import Tk, Canvas
from basic_types import Line


class Window:
    def __init__(self, width: int, height: int, title: str) -> None:
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title(title)
        self.canva = Canvas()
        self.canva.pack()
        self.is_running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self) -> None:
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self) -> None:
        self.is_running = True
        while self.is_running:
            self.redraw()

    def draw_line(self, line: Line, fill_colour: str):
        line.draw(self.canva, fill_colour)

    def close(self):
        self.is_running = False
