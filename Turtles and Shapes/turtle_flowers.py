import turtle
import random

def createWindow():
    window = turtle.Screen()
    window.bgcolor("black")
    return window

def draw_square(someTurtle):
   for i in range(1,5):
        someTurtle.forward(30)
        someTurtle.right(90)
        
def createTurtle(pos):
    color = ["red", "blue", "white", "orange", "yellow", "purple", "green"]
    c = random.randint(0, len(color)-1)
    bestTurtle = turtle.Turtle();
    bestTurtle.setx(pos)
    bestTurtle.shape("turtle")
    bestTurtle.color(color[c])
    bestTurtle.speed(100)
    return bestTurtle

w = createWindow();
t = createTurtle(-150);
t2 = createTurtle(0);
t3 = createTurtle(150);

for i in range(1,37):
    draw_square(t)
    draw_square(t2)
    draw_square(t3)
    t.right(10)
    t2.right(10)
    t3.left(10)
    
t.right(90)
t.forward(100)
t2.right(90)
t2.forward(100)
t3.right(90)
t3.forward(100)

w.exitonclick()
