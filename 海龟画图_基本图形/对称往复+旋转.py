from turtle import *
Screen().colormode(255)
pencolor((100,20,70))
speed(0)
i=0
hideturtle()
pensize(2)

while i<100:
    forward(500)
    backward(500)
    left(6)
    i+=1
done()