from tkinter import Tk,BOTH, Canvas

def main():
    win = Window(800,600)
    l = Line(Point(50,50),Point(400,400))
    win.draw_line(l, "black")
    cell = Cell()
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
    def draw_line(self,line,fill_color):
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
    def __init__ (self,_x1,_x2,_y1,_y2,win,has_left_wall=True,has_right_wall=True,has_top_wall=True,has_bottom_wall=True):
        self._x1 = _x1
        self._x2 = _x2
        self._y1 = _y1 
        self._y2 = _y2
        self.win = win
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall

    def draw(self):
        if self.has_left_wall:
            self.win.create_line(self._x1,self._y1,self._x1,self._y2)
        if self.has_top_wall:
            self.win.create_line(self._x1,self._y1,self._x2,self._y1)
        if self.has_right_wall:
            self.win.create_line(self._x2,self._y1,self._x2,self._y2)
        if self.has_bottom_wall:
            self.win.create_line(self._x1,self._y2,self._x2,self._y2)
        
main()