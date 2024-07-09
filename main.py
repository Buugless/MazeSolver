from tkinter import Tk,BOTH, Canvas

def main():
    win = Window(800, 600)

    c1 = Cell(win)
    c1.has_right_wall = False
    c1.draw(50, 50, 100, 100)

    c2 = Cell(win)
    c2.has_left_wall = False
    c2.has_bottom_wall = False
    c2.draw(100, 50, 150, 100)

    c1.draw_move(c2)

    c3 = Cell(win)
    c3.has_top_wall = False
    c3.has_right_wall = False
    c3.draw(100, 100, 150, 150)

    c2.draw_move(c3)

    c4 = Cell(win)
    c4.has_left_wall = False
    c4.draw(150, 100, 200, 150)

    c3.draw_move(c4, True)

    win.wait_for_close()

class Window():
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title("Maze  solver")
        self.canvas = Canvas(self.__root, width=self.width, height=self.height)
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
    def draw(self,canvas,fill_color):
        canvas.create_line(self.point1.x,self.point1.y,self.point2.x,self.point2.y,fill=fill_color,width = 2)

class Cell():
    def __init__ (self,win):
        self.has_left_wall=True
        self.has_right_wall=True
        self.has_top_wall=True
        self.has_bottom_wall=True
        self._x1 = None
        self._x2 = None
        self._y1 = None 
        self._y2 = None
        self._win = win
        
    def draw(self,x1,y1,x2,y2):
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        if self.has_left_wall:
            line = Line(Point(x1, y1), Point(x1, y2))
            self._win.draw_line(line)
        if self.has_top_wall:
            line = Line(Point(x1, y1), Point(x2, y1))
            self._win.draw_line(line)
        if self.has_right_wall:
            line = Line(Point(x2, y1), Point(x2, y2))
            self._win.draw_line(line)
        if self.has_bottom_wall:
            line = Line(Point(x1, y2), Point(x2, y2))
            self._win.draw_line(line)
    
    def draw_move(self,to_cell,undo=False):
        center_x = (self._x1 + self._x2) / 2
        center_y = (self._y1 + self._y2) / 2
        center_x2 = (to_cell._x1 + to_cell._x2) /2 
        center_y2 = (to_cell._y1 + to_cell._y2) / 2
        fill_color = "gray" if undo else "red"
        line = Line(Point(center_x,center_y),Point(center_x2,center_y2))
        self._win.draw_line(line,fill_color)

main()