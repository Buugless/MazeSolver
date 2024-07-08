from tkinter import Tk,BOTH, Canvas

def main():
    win = Window(800,600)
    p1 = Point()
    p1.x = 50
    p1.y = 50

    p2 = Point()
    p2.x = 150
    p2.y = 50

    p3 = Point()
    p3.x = 100
    p3.y = 100

    line1 = Line(p1, p2)
    line2 = Line(p2, p3)

    win.draw_line(line1, "black")
    win.draw_line(line2, "red")
    win.wait_for_close()

class Window():
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title("Maze  solver")
        self.canvas = Canvas(self.__root, width=self.width, height=self.height)
        self.canvas.pack()
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
    def __init__(self):
        self.x = 0
        self.y = 0

class Line():
    def __init__(self,point1,point2) :
        self.point1 = point1
        self.point2 = point2
    def draw(self,canvas,fill_color):
        canvas.create_line(self.point1.x,self.point1.y,self.point2.x,self.point2.y,fill=fill_color,width = 2)
main()