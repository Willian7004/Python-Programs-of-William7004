from turtle import *
Screen().colormode(255)
pencolor((30,220,100))
speed(0)
i=0
penup()
pendown()
hideturtle()
pensize(2)

while i<80:
    forward(700)
    left(64)
    backward(700)
    left(54)
    i+=1
done()