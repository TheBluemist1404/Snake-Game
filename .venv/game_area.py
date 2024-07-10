import random
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty
from kivy.graphics import Color,Rectangle
from kivy.properties import ListProperty

class Unit(AnchorLayout):
    bg = ListProperty([.5,1,.5,1])

    def __init__(self, **kwargs):
        super(Unit, self).__init__(**kwargs)
        self.label = Label()
        self.label.color = 0,0,0,1
        self.add_widget(self.label)


        self.init_bg = []
        self.bind(bg = self.update_un, pos = self.update_un, size = self.update_un)


    def update_un(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            self.rect_color = Color(*self.bg)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class GamePanel(BoxLayout):
    speed = NumericProperty(1)
    point = NumericProperty(0)

    def speed_up(self, *args):
        if self.speed < 10:
            self.speed += 1

    def speed_down(self, *args):
        if self.speed > 1:
            self.speed -= 1

class GameArea(GridLayout):
    def __init__(self, **kwargs):
        super(GameArea, self).__init__(**kwargs)
        self.cols = 16
        self.rows = 16
        self.food_pos = None
        self.units = []  # Store units in a list for direct access
        self.game_panel = GamePanel()

        for _ in range(8):
            for _ in range(8):
                un = Unit()
                un.init_bg = [.5, 1, .5, 1]
                un.bg = un.init_bg
                self.add_widget(un)
                self.units.append(un)  # Add each unit to the list

                un = Unit()
                un.init_bg = [.5, 1, .5, .8]
                un.bg = un.init_bg
                self.add_widget(un)
                self.units.append(un)  # Add each unit to the list

            for _ in range(8):
                un = Unit()
                un.init_bg = [.5, 1, .5, .8]
                un.bg = un.init_bg
                self.add_widget(un)
                self.units.append(un)  # Add each unit to the list

                un = Unit()
                un.init_bg = [.5, 1, .5, 1]
                un.bg = un.init_bg
                self.add_widget(un)
                self.units.append(un)  # Add each unit to the list

        # Initialize the snake here
        self.snake = Snake(self)
        self.food()
        self.snake.start_game()

    def food(self):
        while True:
            r = random.randint(0, 255)
            if r not in self.snake.body:
                self.food_pos = r
                break

    def update_area(self):
        for i, un in enumerate(self.units):
            if i in self.snake.body:
                un.bg = [1,0,0,1]    # body part
            elif i == self.food_pos:
                un.bg = [0,0,1,1]    # food
            else:
                un.bg = un.init_bg   # ground

from collections import deque

class Snake:
    def __init__(self, game_area):
        self.dir_queue = deque()       # This way we store and manage directions for effectively, avoid 'neck break' movement
        self.dir_queue.append('right') # Initialize
        self.max_length = 2
        self.body = [0, 1]
        self.head = 1
        self.game_area = game_area

        Window.bind(on_key_down=self.on_key_down)

    def start_game(self):
        self.update_body(0)  # Start the game immediately

    def on_key_down(self, window, key, scancode, codepoint, modifiers):
        if key == 273 and self.dir_queue[-1] not in ['up','down']:  # Up arrow key
            self.dir_queue.append('up')
        elif key == 274 and self.dir_queue[-1] not in ['down','up']:  # Down arrow key
            self.dir_queue.append('down')
        elif key == 275 and self.dir_queue[-1] not in ['right','left']:  # Right arrow key
            self.dir_queue.append('right')
        elif key == 276 and self.dir_queue[-1] not in ['left','right']:  # Left arrow key
            self.dir_queue.append('left')

    def update_body(self, dt, *args):
        new_head = self.head
        self.direction = self.dir_queue[0]

        if self.direction == 'right':
            new_head += 1
            if new_head % 16 == 0:
                new_head -= 16
        elif self.direction == 'left':
            new_head -= 1
            if new_head % 16 == 15:
                new_head += 16
        elif self.direction == 'up':
            new_head -= 16
            if new_head < 0:
                new_head += 256
        elif self.direction == 'down':
            new_head += 16
            if new_head >= 256:
                new_head -= 256

        if new_head in self.body:
            # Game Over: Snake has run into itself
            print("Game Over")
            return

        self.body.append(new_head)
        self.head = new_head

        if self.head == self.game_area.food_pos:
            self.max_length += 1
            self.game_area.game_panel.point += 1
            self.game_area.food()

        if len(self.body) > self.max_length:
            self.body.pop(0)

        self.game_area.update_area()
        if len(self.dir_queue) > 1:
            self.dir_queue.popleft()
        Clock.schedule_once(self.update_body, 0.5/self.game_area.game_panel.speed )
