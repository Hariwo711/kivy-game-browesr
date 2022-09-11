import kivy 
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.core.audio import SoundLoader
import random
from tkinter import Button
from kivy.app import App
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Rectangle
from kivy.uix.image import Image

class Manager(ScreenManager):
    pass
class Menu(Screen):
    pass


class SoccerPlayer(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset
        # if self.collide_widget(ball):
        #     vx, vy = self.player1.pos
        #     ball.velocity_x = vx


class SoccerBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
spd = 20



class Game(Screen):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        self.keybord = Window.request_keyboard(self._on_keyboard_closed, self)
        self.keybord.bind(on_key_down=self._on_key_down)
        self.keybord.bind(on_key_up=self._on_key_up)
        self.pressed_keys = set()
        
    
    def on_enter(self, *args):
        Clock.schedule_interval(self.move_step, 0)


    def _on_keyboard_closed(self):
        self.keybord.unbind(on_key_down=self._on_key_down)
        self.keybord.unbind(on_key_up=self._on_key_up)
        self.keybord = None            
   
    def _on_key_down(self, keyboard, keycode, text, modifiers):
        print('down', text)
        self.pressed_keys.add(text)
        
    def _on_key_up(self, keyboard, keycode):
        text = keycode[1]
        print('up', text)
        
        if text in self.pressed_keys:
            self.pressed_keys.remove(text)

    def move_step(self, dt):
        cur_x= self.player1.pos[0]
        cur_y= self.player1.pos[1]     
        cur2_x= self.player2.pos[0]
        cur2_y= self.player2.pos[1]
        step = 500 * dt
        
        if 'w' in self.pressed_keys:
            cur2_y += step
            
        if 'd' in self.pressed_keys:
            cur2_x += step
        if 's' in self.pressed_keys:
            cur2_y -= step
        if 'a' in self.pressed_keys:
            cur2_x -= step
        
        
        if 'u' in self.pressed_keys:
            cur_y += step
        if 'k' in self.pressed_keys:
            cur_x += step
        if 'j' in self.pressed_keys:
            cur_y -= step
        if 'h' in self.pressed_keys:
            cur_x -= step    
        
        
        if 'z' in self.pressed_keys:
            cur_x = self.player1.pos[1]
            cur_y = self.player1.pos[1]
            cur2_x = self.width*3/4
            cur2_y = self.width*3/4
            self.player1.score = 0
            self.player2.score = 0
        if 'x' in self.pressed_keys:
            cur_x = self.center_x-10
            cur_y = self.center_y-20
            cur2_x = self.center_x+20
            cur2_y = self.center_y-20
            randomlist = ["1", "-1"]
            direction_ball = int(random.choice(randomlist))
            self.ball.center = self.center
            self.ball.velocity = (4 * direction_ball, 0)
        # print('step, x, y', dt, cur_x, cur_y)
        self.player1.pos = (cur_x, cur_y)
        self.player2.pos = (cur2_x, cur2_y)
        print(cur_x, cur_y, cur2_x, cur2_y)
 

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        # bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)
        randomlist = ["1", "-1"]
        direction_ball = int(random.choice(randomlist))
        # bounce ball off bottom or top

        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        # went of to a side to score point?
        if self.ball.x < self.x:
            if (self.height*0.26 < self.ball.y) & (self.ball.y < self.height*0.74):
                self.player2.score += 1
                self.serve_ball(vel=(4*direction_ball, 0))
            else:
                self.ball.velocity_x *= -1
        if self.ball.x > self.width:
            if (self.height*0.26 < self.ball.y) & (self.ball.y < self.height*0.74):
                self.player1.score += 1
                self.serve_ball(vel=(4*direction_ball, 0))
            else:
                self.ball.velocity_x *= -1
        if self.ball.velocity_x > 5:
            self.ball.velocity_x = 4
        print(self.ball.velocity_x)
        if self.ball.velocity_y > 5:
            self.ball.velocity_y = 4
        print(self.ball.velocity_y)
    
    def start(self):
        self.update(1/ 60)

class Player(Image):
    pass

class SnakeGame(App):
    pass

SnakeGame().run()