from tkinter import Tk,BOTH, Canvas
import random
import time
import sys
def main():

    num_rows = 12
    num_cols = 16
    margin = 50
    screen_x = 800
    screen_y = 600
    cell_size_x = (screen_x - 2 * margin) / num_cols
    cell_size_y = (screen_y - 2 * margin) / num_rows
    
    sys.setrecursionlimit(1000)
    win = Window(screen_x, screen_y)

    maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win)
    is_solveable = maze.solve()
    if is_solveable:
        print("Maze solved!")
    else:
        print("Maze cannot be solved!")
    win.wait_for_close()

class Window():
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title("Maze  solver")
        self.canvas = Canvas(self.__root, bg = "white",width=self.width, height=self.height)
        self.canvas.pack(fill=BOTH, expand=1)
        self.run = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
    
    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    
    def wait_for_close(self):
        self.run = True
        while self.run:
            self.redraw()
    def close(self):
        self.run = False
    def draw_line(self,line,fill_color="black"):
        line.draw(self.canvas,fill_color)



class Point():
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Line():
    def __init__(self,point1,point2) :
        self.point1 = point1
        self.point2 = point2
    def draw(self,canvas,fill_color="black"):
        canvas.create_line(self.point1.x,self.point1.y,self.point2.x,self.point2.y,fill=fill_color,width = 2)

class Cell():
    def __init__ (self,win=None):
        self.has_left_wall=True
        self.has_right_wall=True
        self.has_top_wall=True
        self.has_bottom_wall=True
        self._x1 = None
        self._x2 = None
        self._y1 = None 
        self._y2 = None
        self._win = win
        self.visited = False
    def draw(self,x1,y1,x2,y2):
        if self._win is None:
            return
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        if self.has_left_wall:
            line = Line(Point(x1, y1), Point(x1, y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(x1, y1), Point(x1, y2))
            self._win.draw_line(line, "white")
        if self.has_top_wall:
            line = Line(Point(x1, y1), Point(x2, y1))
            self._win.draw_line(line)
        else:
            line = Line(Point(x1, y1), Point(x2, y1))
            self._win.draw_line(line, "white")
        if self.has_right_wall:
            line = Line(Point(x2, y1), Point(x2, y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(x2, y1), Point(x2, y2))
            self._win.draw_line(line, "white")
        if self.has_bottom_wall:
            line = Line(Point(x1, y2), Point(x2, y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(x1, y2), Point(x2, y2))
            self._win.draw_line(line, "white")
    
    def draw_move(self,to_cell,undo=False):
        center_x = (self._x1 + self._x2) / 2
        center_y = (self._y1 + self._y2) / 2
        center_x2 = (to_cell._x1 + to_cell._x2) /2 
        center_y2 = (to_cell._y1 + to_cell._y2) / 2
        fill_color = "red"
        if undo:
            fill_color = "gray"
        line = Line(Point(center_x,center_y),Point(center_x2,center_y2))
        self._win.draw_line(line,fill_color)
    
    


class Maze():
    
    def __init__(self,x1,y1,num_rows,num_cols,cell_size_x,cell_size_y,win=None,seed=None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        if seed != None:
            random.seed(seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0,0)
        self._reset_cells_visited()
    def _create_cells(self):
        for cols in range(self.num_cols):
            self.inner = []
            for rows in range(self.num_rows):
                cells = Cell(self._win)
                self.inner.append(cells)
                
            self._cells.append(self.inner)
        for cols in range(self.num_cols):
            for rows in range(self.num_rows):
                self._draw_cell(cols,rows)    
    def _draw_cell(self,i,j):
        x_position = self.x1 + i * self.cell_size_x
        y_position = self.y1 + j * self.cell_size_y
        x2 = x_position + self.cell_size_x
        y2 = y_position + self.cell_size_y
        cell = self._cells[i][j]
        cell.draw(x_position,y_position,x2,y2)
        self._animate()
    
    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        cell = self._cells[0][0]
        cell.has_top_wall = False
        self._draw_cell(0,0)
        cell2 = self._cells[self.num_cols-1][self.num_rows-1]
        cell2.has_bottom_wall = False
        self._draw_cell(self.num_cols-1,self.num_rows-1)

    def _break_walls_r(self,i,j):
        self._cells[i][j].visited = True
        while True:
            next_index_list = []

            # determine which cell(s) to visit next
            # left
            if i > 0 and not self._cells[i - 1][j].visited:
                next_index_list.append((i - 1, j))
            # right
            if i < self.num_cols - 1 and not self._cells[i + 1][j].visited:
                next_index_list.append((i + 1, j))
            # up
            if j > 0 and not self._cells[i][j - 1].visited:
                next_index_list.append((i, j - 1))
            # down
            if j < self.num_rows - 1 and not self._cells[i][j + 1].visited:
                next_index_list.append((i, j + 1))

            # if there is nowhere to go from here
            # just break out
            if len(next_index_list) == 0:
                self._draw_cell(i, j)
                return
            # randomly choose the next direction to go
            direction_index = random.randrange(len(next_index_list))
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

            self._break_walls_r(next_index[0], next_index[1])
    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False        
            
    
    
    def _solve_r(self,i,j):
        self._animate()
        self._cells[i][j].visited = True
        if i == self.num_cols - 1 and j == self.num_rows - 1:
            return True
        
        # move left if there is no wall and it hasn't been visited
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
    
    def solve(self):
        return self._solve_r(0,0)
if __name__ == "__main__":
    main()