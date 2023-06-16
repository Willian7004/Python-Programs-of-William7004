from turtle import *
Screen().colormode(255)
pencolor((155,80,90))
speed(0)
i=0
penup()
left(200)
forward(1100)
right(200)
pendown()
hideturtle()
pensize(2)

while i<100:
    forward(300)
    left(51)
#    backward(800)
#    left(8)
    i+=1
done()