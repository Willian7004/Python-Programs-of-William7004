from turtle import *
Screen().colormode(255)
pencolor((70,120,140))
speed(0)
i=0
penup()
left(200)
forward(600)
right(200)
pendown()
hideturtle()
pensize(2)

while i<100:
    forward(800)
    left(151)
#    backward(800)
#    left(8)
    i+=1
done()