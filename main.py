from tkinter import Tk, BOTH, Canvas
import time
import random

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, Point1, Point2):
        self.point1 = Point1
        self.point2 = Point2

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill=fill_color, width=2
        )

class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title("Maze Solver Window")
        self.__canvas = Canvas(self.__root)
        self.__canvas.configure(width=width, height=height)
        self.__canvas.pack(fill=BOTH)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False

class Cell:
    def __init__(self, point1, point2, window=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False
        self.__x1 = point1.x
        self.__y1 = point1.y
        self.__x2 = point2.x
        self.__y2 = point2.y
        self.__win = window

    def draw(self):
        if self.__win is None:
            return
        top_left_x = min(self.__x1, self.__x2)
        top_left_y = min(self.__y1, self.__y2)
        bot_right_x = max(self.__x1, self.__x2)
        bot_right_y = max(self.__y1, self.__y2)

    # Draw the left wall
        lpoint1 = Point(top_left_x, top_left_y)
        lpoint2 = Point(top_left_x, bot_right_y)
        left_line = Line(lpoint1, lpoint2)
        lcolor = "black" if self.has_left_wall else "#d9d9d9"
        self.__win.draw_line(left_line, lcolor)

        rpoint1 = Point(bot_right_x, top_left_y)
        rpoint2 = Point(bot_right_x, bot_right_y)
        right_line = Line(rpoint1, rpoint2)
        rcolor = "black" if self.has_right_wall else "#d9d9d9"
        self.__win.draw_line(right_line, rcolor)

        tpoint1 = Point(top_left_x, top_left_y)
        tpoint2 = Point(bot_right_x, top_left_y)
        top_line = Line(tpoint1, tpoint2)
        tcolor = "black" if self.has_top_wall else "#d9d9d9"
        self.__win.draw_line(top_line, tcolor)

        bpoint1 = Point(top_left_x, bot_right_y)
        bpoint2 = Point(bot_right_x, bot_right_y)
        bottom_line = Line(bpoint1, bpoint2)
        bcolor = "black" if self.has_bottom_wall else "#d9d9d9"
        self.__win.draw_line(bottom_line, bcolor)

    def centerpoint(self):
        return(Point((self.__x1 + self.__x2)/2, (self.__y1 + self.__y2)/2))

    def draw_move(self, to_cell, undo=False):
        print(f"Drawing {'undo' if undo else 'forward'} move")
        point1 = self.centerpoint()
        point2 = to_cell.centerpoint()
        line = Line(point1, point2)
        color = "gray50" if undo else "red"
        time.sleep(0.2)  # Longer pause and before drawing
        self.__win.draw_line(line, color)
        self.__win.redraw()


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None,
    ):
        if seed is not None:
            random.seed(seed)
        MAX_DIMENSION = 100  # or whatever maximum you think is reasonable
        if num_rows > MAX_DIMENSION or num_cols > MAX_DIMENSION:
            raise ValueError(f"Maze dimensions cannot exceed {MAX_DIMENSION}")
        if num_rows < 1 or num_cols < 1:
            raise ValueError("Maze dimensions must be at least 1")
        if cell_size_x <= 0 or cell_size_y <= 0:
            raise ValueError("Cell sizes must be positive")
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._create_cells()
        self._break_entrance_and_exit()

    def _create_cells(self):
        self._cells = []
        for i in range(0, self.num_cols):
            column_list = []
            for j in range(0, self.num_rows):
                point1 = Point((self.x1 +(self.cell_size_x * i)), (self.y1 +(self.cell_size_y * j)))
                point2 = Point((point1.x + self.cell_size_x), (point1.y + self.cell_size_y))
                cell = Cell(point1, point2, self.win)
                column_list.append(cell)
            self._cells.append(column_list)
        for i in range(0, self.num_cols):
            for j in range(0, self.num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self.win is not None:
            self._cells[i][j].draw()
            self._animate()

    def _neighbor_check(self, i, j):
        to_visit = []
        if i + 1 < self.num_cols and not self._cells[i + 1][j].visited:
            to_visit.append((i + 1, j))
        if i - 1 >= 0 and not self._cells[i - 1][j].visited:
            to_visit.append((i - 1, j))
        if j + 1 < self.num_rows and not self._cells[i][j + 1].visited:
            to_visit.append((i, j + 1))
        if j - 1 >= 0 and not self._cells[i][j - 1].visited:
            to_visit.append((i, j - 1))
        return to_visit

    def _break_walls_r(self, i, j):
        print(f"\nVisiting cell ({i}, {j})")
        self._cells[i][j].visited = True
        to_visit = self._neighbor_check(i, j)
        if len(to_visit) == 0:
            self._draw_cell(i, j)
            return
        while to_visit:
            next_i, next_j = random.choice(to_visit)
            to_visit.remove((next_i, next_j))
            if next_i > i:
                 self._cells[i][j].has_right_wall = False
                 self._cells[next_i][next_j].has_left_wall = False
            if next_i < i:
                 self._cells[i][j].has_left_wall = False
                 self._cells[next_i][next_j].has_right_wall = False
            if next_j < j:
                 self._cells[i][j].has_top_wall = False
                 self._cells[next_i][next_j].has_bottom_wall = False
            if next_j > j:
                 self._cells[i][j].has_bottom_wall = False
                 self._cells[next_i][next_j].has_top_wall = False
            self._draw_cell(i, j)
            self._draw_cell(next_i, next_j)
            self._break_walls_r(next_i, next_j)
            to_visit = self._neighbor_check(i, j)

    def _reset_cells_visited(self):
        for i in range(0, self.num_cols):
            for j in range(0, self.num_rows):
                self._cells[i][j].visited = False

    def _break_entrance_and_exit(self):
        entrance_cell = self._cells[0][0]
        entrance_cell.has_top_wall = False
        self._draw_cell(0, 0)
        exit_cell = self._cells[self.num_cols-1][self.num_rows-1]
        exit_cell.has_bottom_wall = False
        self._draw_cell(self.num_cols-1, self.num_rows-1)

    def _animate(self):
        if self.win is None:
            return
        self.win.redraw()
        time.sleep(0.05)

    def _get_valid_moves(self, i, j):
        valid_moves = []
        # Right
        if (i + 1 < self.num_cols and 
            not self._cells[i][j].has_right_wall and 
            not self._cells[i + 1][j].visited):
            valid_moves.append((i + 1, j))
        # Left
        if (i - 1 >= 0 and 
            not self._cells[i][j].has_left_wall and
            not self._cells[i - 1][j].visited):
            valid_moves.append((i - 1, j))
        # Down
        if (j + 1 < self.num_rows and 
            not self._cells[i][j].has_bottom_wall and
            not self._cells[i][j + 1].visited):
            valid_moves.append((i, j + 1))
        # Up
        if (j - 1 >= 0 and
            not self._cells[i][j].has_top_wall and
            not self._cells[i][j - 1].visited):
            valid_moves.append((i, j - 1))
        return valid_moves

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        print(f"Entering _solve_r at ({i},{j})")
        self._animate()
        self._cells[i][j].visited = True
        if self._cells[i][j] == self._cells[self.num_cols-1][self.num_rows-1]:
            print("Found end!")
            return True
        valid_moves = self._get_valid_moves(i, j)
        print(f"Valid moves at ({i},{j}): {valid_moves}")
        for (next_i, next_j) in valid_moves:
            print(f"Trying move to ({next_i},{next_j})")
            self._cells[i][j].draw_move(self._cells[next_i][next_j])
            result = self._solve_r(next_i, next_j)  # store result to inspect
            print(f"Result of move to ({next_i},{next_j}) was: {result}")
            if result:
                return True
            print(f"Path failed at ({i},{j}), backtracking")
            self._cells[i][j].draw_move(self._cells[next_i][next_j], undo=True)
        print(f"No valid moves worked at ({i},{j})")
        return False

def main():
    win = Window(800, 600)
    maze = Maze(50, 50, 10, 10, 40, 40, win)
    maze._break_walls_r(0, 0)
    maze._reset_cells_visited()
    maze.solve()
    win.wait_for_close()

if __name__ == "__main__":
    main()
