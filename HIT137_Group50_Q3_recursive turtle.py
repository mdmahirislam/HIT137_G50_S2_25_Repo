import turtle as trl

#recursive funtion to create indents into each side
def rec_draw(length, depth):
    if depth == 0:        
        t.forward(length)
    else:
        length /= 3.0
        rec_draw(length, depth - 1)
        t.right(60)
        rec_draw(length, depth - 1)
        t.left(120)
        rec_draw(length, depth - 1)
        t.right(60)
        rec_draw(length, depth - 1)

#changes the angle of the line depending on the number of sides
def side_turn(sides, length, depth):
    angle = 360 / sides
    for i in range(sides):
        rec_draw(length, depth)
        t.right(angle)

def screen():
    global t
    sides = int(input("Enter the number of sides: "))
    length = int(input("Enter the side lengths: "))
    depth = int(input("Enther the recursion depth: "))

    #creates a screen and changes turtle to "t"
    scr = trl.Screen()
    t = trl.Turtle()

    #changes screen title and background
    scr.bgcolor("black")
    scr.title("HIT137 Q3 Assessment 2")

    #fastest speed and change the colour to red
    t.speed(0)
    t.color("red")

    #centers the drawing
    t.up()
    t.goto(-length/2, length/2)
    t.down()

    #hides the turtle icon
    t.hideturtle()
    
    side_turn(sides, length, depth)

    scr.mainloop()
screen()