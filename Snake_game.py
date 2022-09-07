from tkinter import *
import customtkinter
import random

GAME_HEIGHT = 700
GAME_WIDTH = 700
SPEED = 100
SPACE: int = 50
SNAKE_COLOR = "#09b734"
FOOD_COLOR = "#b72009"
BACKGROUND_COLOR = "black"
SCORE = 0
BODY_PART = 3
DIRECTION = 'down'


class Food:
    def __init__(self):
        x = random.randint(0, int(GAME_WIDTH / SPACE) - 1) * SPACE
        y = random.randint(0, int(GAME_WIDTH / SPACE) - 1) * SPACE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE, y + SPACE, fill=FOOD_COLOR, tag='food')


class Snake:
    def __init__(self):
        self.coordinates = []
        self.squares = []
        for i in range(BODY_PART):
            self.coordinates.append([0, 0])
        for x, y in self.coordinates[:]:
            self.square = canvas.create_rectangle(x, y, x + 50, y + 50, fill=SNAKE_COLOR)
            self.squares.append(self.square)


def next_turn(snake, food):
    x, y = snake.coordinates[0]
    if DIRECTION == "up":
        y -= 50
    elif DIRECTION == "down":
        y += 50
    elif DIRECTION == "left":
        x -= 50
    elif DIRECTION == "right":
        x += 50
    snake.coordinates.insert(0, [x, y])
    square = canvas.create_rectangle(x, y, x + 50, y + 50, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global SCORE
        SCORE += 1
        label.config(text="Score : {}".format(SCORE))
        canvas.delete('food')
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]
    if check_collision():
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)


def game_over():
    canvas.delete(ALL)
    canvas.create_text(350, 350, fill="red", text="Game Over")
    b = Button(master=window, text="RESTART", width=3, height=1, fg="black", background="red",font=('sans serif',7))
    b['command'] = lambda: restart(b)
    b.place(x=375, y=375)


def restart(b):
    canvas.delete(ALL)
    b.destroy()
    global snake
    global food
    global SCORE
    global DIRECTION
    snake = Snake()
    food = Food()
    SCORE = 0
    label.config(text=f"Score : {SCORE}")
    DIRECTION = "down"
    next_turn(snake, food)


def check_collision():
    x, y = snake.coordinates[0]
    if x < 0 or x > GAME_WIDTH:
        return True
    elif y > GAME_HEIGHT or y < 0:
        return True
    for x1, y1 in snake.coordinates[1:0]:
        if x1 == x and y1 == y:
            return True
    return False


def change_direction(new_direction):
    global DIRECTION
    if new_direction == "up":
        if DIRECTION != "down":
            DIRECTION = "up"
    elif new_direction == "down":
        if DIRECTION != "up":
            DIRECTION = "down"
    elif new_direction == "left":
        if DIRECTION != "right":
            DIRECTION = "left"
    elif new_direction == "right":
        if DIRECTION != "left":
            DIRECTION = "right"


window = Tk()
window.title("Snake Game By Mothilal Nehru")
window.geometry(f"{GAME_HEIGHT}x{GAME_WIDTH}")
window.bind("<Right>", lambda event: change_direction("right"))
window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))
label = Label(master=window, text="Score : {}".format(SCORE), font=('sans serif', 40), foreground='#9c9595')
label.pack()
canvas = Canvas(master=window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()
snake = Snake()
food = Food()
next_turn(snake, food)
window.mainloop()
