import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder

from game_area import GameArea, GamePanel
Builder.load_file('snake_game.kv')

class SnakeGame(BoxLayout):
    pass

class SnakeGameApp(App):
    def build(self):
        return SnakeGame()

if __name__=='__main__':
    SnakeGameApp().run()