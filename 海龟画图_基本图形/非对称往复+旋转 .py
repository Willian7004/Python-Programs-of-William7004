from turtle import *
Screen().colormode(255)
pencolor((155,120,50))
speed(0)
i=0
hideturtle()
pensize(2)
penup()
forward(300)
pendown()

while i<100:
    forward(300)
    backward(320)
    left(6)
    i+=1
done()