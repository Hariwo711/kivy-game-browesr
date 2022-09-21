import random
from kivy.app import App 
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.lang import Builder

def collides(rect1,rect2):
    r1x = rect1[0][0]
    r1y = rect1[0][1]
    r2x = rect2[0][0]
    r2y = rect2[0][1]
    r1w = rect1[1][0]
    r1h = rect1[1][1]
    r2w = rect2[1][0]
    r2h = rect2[1][1]

    if(r1x < r2x + r2w and r1x + r1w > r2x and r1y < r2y + r2h and r1y +r1h > r2y):
        return True
    else:
        return False
class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.sound = SoundLoader.load('test.mp3')
        self.sound.play()

        self._keyboard = Window.request_keyboard(
            self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)

        self.pressed_keys = set()
        Clock.schedule_interval(self.move_step, 0)

        with self.canvas:
            self.hero = Rectangle(source='snake_head.png', pos=(1,2 ), size=(40, 40),)
            
            self.enemy = Rectangle(source='fruit.png', pos=(random.randint(50,450), random.randint(50,550)), size=(30, 30))
    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard.unbind(on_key_up=self._on_key_up)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifilers):
        print('down', text)
        self.pressed_keys.add(text)
    
    def _on_key_up(self, keyboard, keycode):
        text = keycode[1]
        print('up', text)

        if text in self.pressed_keys:
            self.pressed_keys.remove(text)
    
    def move_step(self, dt):
        cur_x = self.hero.pos[0]
        cur_y = self.hero.pos[1]

        step = 150 * dt

        if 'w' in self.pressed_keys:
            cur_y += step
        if 's' in self.pressed_keys:
            cur_y -= step
        if 'a' in self.pressed_keys:
            cur_x -= step
        if 'd' in self.pressed_keys:
            cur_x += step

        self.hero.pos = (cur_x, cur_y)   

        if collides((self.hero.pos,self.hero.size),(self.enemy.pos,self.enemy.size)):
            print("colliding!")
        else:
            print("not colliding!")
class MyApp(App):
    def build(self):
        return GameWidget()

if __name__ =='__main__':
    app = MyApp()
    app.run()