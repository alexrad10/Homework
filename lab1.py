from tkinter import Tk, Canvas
import random

# Global values
# Size of window
WIDTH = 1200
HEIGHT = 600
# Size of one segment
SEG_SIZE = 20
# Flag of the game
IN_GAME = True


# Make apple to be eaten
def create_block():
    global BLOCK
    pos_x = SEG_SIZE * random.randint(1, (WIDTH - SEG_SIZE) / SEG_SIZE)
    pos_y = SEG_SIZE * random.randint(1, (HEIGHT - SEG_SIZE) / SEG_SIZE)
    BLOCK = c.create_oval(pos_x, pos_y,
                          pos_x + SEG_SIZE, pos_y + SEG_SIZE,
                          fill="red")


# Handle game to be in process
def main():
    global IN_GAME
    if IN_GAME:
        s.move()
        head_coords = c.coords(s.segments[-1].instance)
        x1, y1, x2, y2 = head_coords
        # Check if it is gamefield edges
        if x2 > WIDTH or x1 < 0 or y1 < 0 or y2 > HEIGHT:
            IN_GAME = False
        # Eating
        elif head_coords == c.coords(BLOCK):
            s.add_segment()
            c.delete(BLOCK)
            create_block()
        # Self-eating
        else:
            for index in range(len(s.segments) - 1):
                if head_coords == c.coords(s.segments[index].instance):
                    IN_GAME = False
        root.after(100, main)
    # Stop game
    else:
        set_state(restart_text, 'normal')
        set_state(game_over_text, 'normal')


# One snake segment
class Segment(object):
    def __init__(self, x, y, head=False):
        if head:
            self.instance = c.create_rectangle(x, y,
                                               x + SEG_SIZE, y + SEG_SIZE,
                                               fill="red")
        else:
            self.instance = c.create_rectangle(x, y,
                                               x + SEG_SIZE, y + SEG_SIZE,
                                               fill="white")


class Snake(object):

    def __init__(self, segments):
        self.segments = segments
        # possible moves
        self.mapping = {"Down": (0, 1), "Right": (1, 0),
                        "Up": (0, -1), "Left": (-1, 0)}
        # initial movement direction
        self.vector = self.mapping["Right"]

    def move(self):
        for index in range(len(self.segments) - 1):
            segment = self.segments[index].instance
            x1, y1, x2, y2 = c.coords(self.segments[index + 1].instance)
            c.coords(segment, x1, y1, x2, y2)

        x1, y1, x2, y2 = c.coords(self.segments[-2].instance)
        c.coords(self.segments[-1].instance,
                 x1 + self.vector[0] * SEG_SIZE, y1 + self.vector[1] * SEG_SIZE,
                 x2 + self.vector[0] * SEG_SIZE, y2 + self.vector[1] * SEG_SIZE)

    def add_segment(self):
        last_seg = c.coords(self.segments[0].instance)
        x = last_seg[2] - SEG_SIZE
        y = last_seg[3] - SEG_SIZE
        self.segments.insert(0, Segment(x, y))

    def change_direction(self, event):
        if event.keysym in self.mapping:
            self.vector = self.mapping[event.keysym]

    def reset_snake(self):
        for segment in self.segments:
            c.delete(segment.instance)


def set_state(item, state):
    c.itemconfigure(item, state=state)


def clicked(event):
    global IN_GAME
    s.reset_snake()
    IN_GAME = True
    c.delete(BLOCK)
    c.itemconfigure(restart_text, state='hidden')
    c.itemconfigure(game_over_text, state='hidden')
    start_game()


# Some useful functions
def start_game():
    global s
    create_block()
    s = create_snake()
    c.bind("<KeyPress>", s.change_direction)
    main()


# Create snake
def create_snake():
    start_x = random.randint(0, int(WIDTH / 2))
    start_y = random.randint(0, HEIGHT - 25)
    segments = [Segment(start_x + SEG_SIZE, start_y + SEG_SIZE),
                Segment(start_x + SEG_SIZE * 2, start_y + SEG_SIZE, head=True)]
    return Snake(segments)


root = Tk()
root.title("MySnake")

c = Canvas(root, width=WIDTH, height=HEIGHT, bg="green")
c.grid()

c.focus_set()
game_over_text = c.create_text(WIDTH / 2, HEIGHT / 2, text="GAME OVER!",
                               fill='red',
                               state='hidden')
restart_text = c.create_text(WIDTH / 2, HEIGHT - HEIGHT / 3,
                             fill='white',
                             text="Click here to restart",
                             state='hidden')
c.tag_bind(restart_text, "<Button-1>", clicked)
start_game()
root.mainloop()
