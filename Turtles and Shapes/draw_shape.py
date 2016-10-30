import turtle

def draw_square():
    window = turtle.Screen()
    window.bgcolor("black")

    brad = turtle.Turtle()
    brad.shape("circle")
    brad.color("red")
    
    brad.forward(100)
    brad.right(90)

    brad.forward(100)
    brad.right(90)

    brad.forward(100)
    brad.right(90)

    brad.forward(100)
    brad.right(90)

    angie = turtle.Turtle()
    angie.shape("turtle")
    angie.color("white")
    angie.circle(100)


    brad = turtle.Turtle()
    brad.shape("arrow")
    brad.color("green")
    i= 0;
    while( i < 3 ):
        brad.forward(60)
        brad.left(120)
        i += 1

    window.exitonclick()
    
draw_square()
