from turtle import *
Screen().colormode(255)
pencolor((30,220,100))
speed(0)
i=0
penup()
right(200)
backward(300)
left(200)
pendown()
hideturtle()
pensize(2)

while i<50:
    forward(800)
    left(10)
    backward(700)
    left(10)
    i+=1
done()