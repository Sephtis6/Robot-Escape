#imports a librarie to be used in the project
import inspect
import pickle
import random
import turtle
import argparse
bag = turtle.Turtle()
#function in order to draw the bag that will be used in the project that the robot has to escape
#this is done by creating a shape for the turtle and then creating a pen to draw the bag around the turtle shape
def draw_bag():
    bag.shape('turtle')
    bag.pen(pencolor='brown', pensize=5)
    bag.penup()
    bag.goto(-35, 35)
    bag.pendown()
    bag.right(90)
    bag.forward(70)
    bag.left(90)
    bag.forward(70)
    bag.left(90)
    bag.forward(70)
    bag.hideturtle()
#funtion to check whether the turtle has escaped the confines of the bag
def escaped(position):
    x = int(position[0])
    y = int(position[1])
    return x < -35 or x > 35 or y < -35 or y > 35
#funtion that has the turtle move in a line and draws the line while checking if the turtle has escaped
def draw_line():
    angle = 0
    step = 5
    t = turtle.Turtle()
    while not escaped(t.position()):
        t.left(angle)
        t.forward(step)
#has the turtle move/draw in a square and stores the data in a variable
def draw_square(t, size):
    L = []
    for i in range(4):
        t.forward(size)
        t.left(90)
        store_position_data(L, t)
        return L
#function to store all the positional data about where the turtle has been
def store_position_data(L, t):
    position = t.position()
    L.append([position[0], position[1], escaped(position)])
#funtion that takes a number and then runs the draw square function that draws a square that increases in size/number of squares till it hits the input number
def draw_squares(number):
    t = turtle.Turtle()
    L = []
    for i in range(1, number + 1):
        t.penup()
        t.goto(-i, -i)
        t.pendown()
        L.extend(draw_square(t, i*2))
        return L
#takes the draw squares functions and runs it till the turtle has escaped the bag then opens a file and logs all the data collected
def draw_squares_until_escaped(n):
    t = turtle.Turtle()
    L = draw_squares(n)
    with open("data_square", "wb") as f:
        pickle.dump(L, f)
#has the turtle move/draw in a triangle that that increases in size till it hits the inputted number for wanted triangles
def draw_triangles(number):
    t = turtle.Turtle()
    for i in range(1, number):
        t.forward(i*10)
        t.right(120)
#funtion that takes the turtle and draws in a random spiral pattern till the turtle has escaped the bag
#it does this by picking a randon point in the center of the bag and then has it turn randomly and move forward while storing the data
#and checking to see if the turtle has escaped
def draw_spirals_until_escaped():
    t = turtle.Turtle()
    t.penup()
    t.left(random.randint(0, 360))
    t.pendown()

    i = 0
    turn = 360/random.randint(1, 10)
    L=[]
    store_position_data(L, t)
    while not escaped(t.position()):
        i += 1
        t.forward(i*5)
        t.right(turn)
        store_position_data(L, t)
    return L
#function that calls the draw spirals function and runs it till it escaped and then dumps the data collected into a file
def draw_random_spirangles():
    L = []
    for i in range(10):
        L.extend(draw_spirals_until_escaped())
    with open ("data_rand", "wb") as f:
        pickle.dump(L, f)
#function that creates the gui used and then gives the option of what function to run depending on what is input
#then it runs the called function in order to draw the bag and then run the function
#if it can not find what is being called it throws in an error and then has the program print for help and what the probelm is
if __name__ == '__main__':
    fns = {"line":draw_line, "squares": draw_squares_until_escaped, "triangles": draw_triangles,
           "spirangles": draw_random_spirangles}
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--function", choices = fns, help = "One of " + ', '.join(fns.keys()))
    args = parser.parse_args()
    try:
        f = fns[args.function]
        turtle.setworldcoordinates(-70., -70., 70., 70.)
        draw_bag()
        turtle.hideturtle()
        if len(inspect.getargspec(f).args) == 1:
            f(args.number)
        else:
            f()
        turtle.mainloop()
    except KeyError:
        parser.print_help()