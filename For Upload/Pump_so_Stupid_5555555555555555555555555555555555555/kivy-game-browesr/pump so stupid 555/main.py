from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.core.window import Window

class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self._keyboard =Window.request_keyboard(
            self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        
        with self.canvas:
            self.hero = Rectangle(source='logo.png', pos=(0, 0), size=(100, 100))
            
    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None
        
    def _on_key_down(self, keyboard, keycode, text, modifiers):
        print('key down', text)
        cur_x = self.hero.pos[0]
        cur_y = self.hero.pos[1]
        if keycode[1] == 'up':
            self.hero.pos = (cur_x, cur_y - 10)
        elif text == 'w':
            cur_y += 10
        elif text == 'd':
            cur_x += 10
        elif text == 's':
            cur_y -= 10
        elif text == 'a':
            cur_x -= 10
        elif text == 'q':
            cur_x = 0
            cur_y = 0
        self.hero.pos = (cur_x, cur_y)
    def moving_snake()
class MyApp(App):
    def build(self):
        return GameWidget()

if __name__ == '__main__':
    app = MyApp()
    app.run()