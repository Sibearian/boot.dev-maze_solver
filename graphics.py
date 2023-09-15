from basic_types import *
from window import Window
from time import sleep
import random

class Cell:
    def __init__(self, top: Point, bottom: Point, win : Window):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.left_wall = Line(Point(top.x, top.y), Point(top.x, bottom.y))
        self.right_wall = Line(Point(bottom.x, bottom.y), Point(bottom.x, top.y))
        self.top_wall = Line(Point(top.x, top.y), Point(bottom.x, top.y))
        self.bottom_wall = Line(Point(top.x, bottom.y), Point(bottom.x, bottom.y))
        self._x1 = top.x
        self._x2 = bottom.x
        self._y1 = top.y
        self._y2 = bottom.y
        self._win = win
        self.visited = False

    def get_center_point(self) -> Point:
        x = (self._x1 + self._x2) / 2
        y = (self._y1 + self._y2) / 2
        return Point(x, y)

    def draw(self) -> None:
        if self.has_bottom_wall:
            self.bottom_wall.draw(self._win.canva, "black")
        else:
            self.bottom_wall.draw(self._win.canva, "#F0F0F0")

        if self.has_top_wall:
            self.top_wall.draw(self._win.canva, "black")
        else:
            self.top_wall.draw(self._win.canva, "#F0F0F0")

        if self.has_left_wall:
            self.left_wall.draw(self._win.canva, "black")
        else:
            self.left_wall.draw(self._win.canva, "#F0F0F0")

        if self.has_right_wall:
            self.right_wall.draw(self._win.canva, "black")
        else:
            self.right_wall.draw(self._win.canva, "#F0F0F0")

    def draw_move(self, to_cell, undo=False) -> None:
        color = "grey" if undo else "red"
        Line(self.get_center_point(), to_cell.get_center_point()).draw(
            self._win.canva, color
        )


class Maze:
    def __init__(
        self,
        x1 : int,
        y1 : int,
        num_rows : int,
        num_cols : int,
        cell_size_x : int,
        cell_size_y : int,
        win : Window,
        seed = None
    ):
        (
            self.x,
            self.y,
            self.num_rows,
            self.num_cols,
            self.cell_size_x,
            self.cell_size_y,
            self.win,
        ) = (x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win)
        self._cells : list[list[Cell]] = []
        if seed != None:
            random.seed(seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0,0)
        self._reset_cells_visited()

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_bottom_wall = False
        self._cells[0][0].has_top_wall = False
        self._cells[0][0].has_left_wall = False
        self._cells[0][0].has_right_wall = False
        self._cells[0][0].draw()

        self._cells[self.num_cols -1][self.num_rows -1].has_bottom_wall = False
        self._cells[self.num_cols -1][self.num_rows -1].has_top_wall = False
        self._cells[self.num_cols -1][self.num_rows -1].has_left_wall = False
        self._cells[self.num_cols -1][self.num_rows -1].has_right_wall = False
        self._cells[self.num_cols -1][self.num_rows -1].draw()


    def _create_cells(self) -> None:
        for i in range(self.num_cols):
            temp = []
            for j in range(self.num_rows):
                temp.append(
                    Cell(
                        Point(
                            self.x + (i * self.cell_size_x),
                            self.y + (j * self.cell_size_y)
                        ), 
                        Point(
                            self.x + ((i + 1) * self.cell_size_x),
                            self.y + ((j + 1) * self.cell_size_y)
                        ), self.win)
                )
            self._cells.append(temp)
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._draw_cell(i, j)
        
    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            next_index_list = []

            possible_direction_indexes = 0

            # determine which cell(s) to visit next
            # left
            if i > 0 and not self._cells[i - 1][j].visited:
                next_index_list.append((i - 1, j))
                possible_direction_indexes += 1
            # right
            if i < self.num_cols - 1 and not self._cells[i + 1][j].visited:
                next_index_list.append((i + 1, j))
                possible_direction_indexes += 1
            # up
            if j > 0 and not self._cells[i][j - 1].visited:
                next_index_list.append((i, j - 1))
                possible_direction_indexes += 1
            # down
            if j < self.num_rows - 1 and not self._cells[i][j + 1].visited:
                next_index_list.append((i, j + 1))
                possible_direction_indexes += 1

            # if there is nowhere to go from here
            # just break out
            if possible_direction_indexes == 0:
                self._draw_cell(i, j)
                return

            # randomly choose the next direction to go
            direction_index = random.randrange(possible_direction_indexes)
            next_index = next_index_list[direction_index]

            # knock out walls between this cell and the next cell(s)
            # right
            if next_index[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
            # left
            if next_index[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
            # down
            if next_index[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False
            # up
            if next_index[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False

            # recursively visit the next cell
            self._break_walls_r(next_index[0], next_index[1])

    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False

    def _draw_cell(self, i: int, j: int) -> None:
        self._cells[i][j].draw()
        self._animate()
    
    def _animate(self) -> None:
        self.win.redraw()
        sleep(0.05)
    
    def solve(self):
        return self._solve_r()

    def _solve_r(self, i = 0, j = 0):
        self._animate()
        self._cells[i][j].visited = True

        if i == self.num_cols - 1 and j == self.num_rows - 1:
            return True

        if (
            i > 0
            and not self._cells[i][j].has_left_wall
            and not self._cells[i - 1][j].visited
        ):
            self._cells[i][j].draw_move(self._cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i - 1][j], True)

        # move right if there is no wall and it hasn't been visited
        if (
            i < self.num_cols - 1
            and not self._cells[i][j].has_right_wall
            and not self._cells[i + 1][j].visited
        ):
            self._cells[i][j].draw_move(self._cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i + 1][j], True)

        # move up if there is no wall and it hasn't been visited
        if (
            j > 0
            and not self._cells[i][j].has_top_wall
            and not self._cells[i][j - 1].visited
        ):
            self._cells[i][j].draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j - 1], True)

        # move down if there is no wall and it hasn't been visited
        if (
            j < self.num_rows - 1
            and not self._cells[i][j].has_bottom_wall
            and not self._cells[i][j + 1].visited
        ):
            self._cells[i][j].draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j + 1], True)

        # we went the wrong way let the previous cell know by returning False
        return False
