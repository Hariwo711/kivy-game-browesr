import kivy 
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget

import random
from kivy.app import App
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Rectangle

# kv = Builder.load_file("screen.kv")
kv = Builder.load_file("screen.kv")

#Setsup The menu screen from .kv file
class Menu(Screen):
    pass

class game_over(Screen):
    pass

#setting up soccer player
class SoccerPlayer(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset
            
class SoccerBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
    spd = 20

#setting up soccer Game
class SoccerGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    def start(self, *args):
        self.keybord = Window.request_keyboard(self._on_keyboard_closed, self)
        self.keybord.bind(on_key_down=self._on_key_down)
        self.keybord.bind(on_key_up=self._on_key_up)
        self.pressed_keys = set()
        Clock.schedule_interval(self.move_step, 0)
        self.serve_ball()
        self.update(self, *args)
        Clock.schedule_interval(self.update,1/ 60)
    
    def __init__(self, **kwargs):
        super(SoccerGame, self).__init__(**kwargs)

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
            cur_x = self.center_x+100
            cur_y = self.center_y-90
            cur2_x = self.center_x-250
            cur2_y = self.center_y-90
            self.player1.score = 0
            self.player2.score = 0
        if 'x' in self.pressed_keys:
            cur_x = self.center_x+100
            cur_y = self.center_y-90
            cur2_x = self.center_x-250
            cur2_y = self.center_y-90
            randomlist = ["1", "-1"]
            direction_ball = int(random.choice(randomlist))
            self.ball.center = self.center
            self.ball.velocity = (4 * direction_ball, 0)
        if 'c' in self.pressed_keys:
            randomlist = ["1", "-1"]
            direction_ball = int(random.choice(randomlist))
            self.ball.center = self.center
            self.ball.velocity = (4 * direction_ball, 0)
        print('step, x, y', dt, cur_x, cur_y)
        self.player1.pos = (cur_x, cur_y)
        self.player2.pos = (cur2_x, cur2_y)
        print(cur_x, cur_y, cur2_x, cur2_y)
 

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        # bounce of players
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)
        randomlist = ["1", "-1"]
        direction_ball = int(random.choice(randomlist))
        
        # bounce ball off bottom or top of football field

        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        # went of to a opponents goal to score point?
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


class soccerscreen(Screen):
    game_engine = ObjectProperty(None)
    def on_enter(self):
        # we screen comes into view, start the game
        self.game_engine.start()







SnakeGamePoints = 0



#Colision detection Code
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


#Pumps Snake Game
class SnakeGame(Screen):
    score = NumericProperty(SnakeGamePoints)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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
        global SnakeGamePoints
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
            self.enemy.pos = (random.randint(50,750), random.randint(50,560))
            self.score += 1
            print(self.score)
        # else:
            # print("not colliding!")

    def on_enter(self, **kwargs):

        self._keyboard = Window.request_keyboard(
             self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)

        self.pressed_keys = set()
        Clock.schedule_interval(self.move_step, 0)
        
        with self.canvas:
            self.hero = Rectangle(source='snake_head.png', pos=(1,2 ), size=(40, 40),)
            
            self.enemy = Rectangle(source='assets/orange.png', pos=(random.randint(50,750), random.randint(50,560)), size=(50, 30))




def update_posandscore(hero_posandsize,enemy_posandsize,score,goodorbad):
    enemy_posandsize = (random.randint(50,750), random.randint(50,560))
    
    if goodorbad == 'good':
        score += 1
    elif goodorbad == 'bad':
        score = score-3

    return enemy_posandsize,score
#Uses Colision Function

enemy4_Type = 1

class PokemonFoodPicker(Screen):
    score = NumericProperty(SnakeGamePoints)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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
        global SnakeGamePoints
        global enemy4_Type
        cur_x = self.hero.pos[0]
        cur_y = self.hero.pos[1]

        step = 150 * dt

        #defining score for checking if changed
        check_score = self.score

        if 'w' in self.pressed_keys:
            cur_y += step
        if 's' in self.pressed_keys:
            cur_y -= step
        if 'a' in self.pressed_keys:
            cur_x -= step
        if 'd' in self.pressed_keys:
            cur_x += step

        self.hero.pos = (cur_x, cur_y)   
        # if collides((self.hero.pos,self.hero.size),(self.enemy.pos,self.enemy.size)):
        #     print("colliding!")
        #     self.enemy.pos = (random.randint(50,750), random.randint(50,560))
        #     self.score += 1
        #     print(self.score)
        if collides((self.hero.pos,self.hero.size),(self.enemy.pos,self.enemy.size)):
            self.enemy.pos,self.score = update_posandscore((self.hero.pos,self.hero.size),(self.enemy.pos,self.enemy.size),self.score,'good')
        
        elif collides((self.hero.pos,self.hero.size),(self.enemy2.pos,self.enemy2.size)):
            self.enemy2.pos,self.score = update_posandscore((self.hero.pos,self.hero.size),(self.enemy2.pos,self.enemy2.size),self.score,'good')
        
        elif collides((self.hero.pos,self.hero.size),(self.enemy3.pos,self.enemy3.size)):
            self.enemy3.pos,self.score = update_posandscore((self.hero.pos,self.hero.size),(self.enemy3.pos,self.enemy3.size),self.score,'good')
        
        elif collides((self.hero.pos,self.hero.size),(self.enemy4.pos,self.enemy4.size)):
            if enemy4_Type == 1:
                print('test if true')
                self.enemy4.pos, self.score = update_posandscore((self.hero.pos,self.hero.size),(self.enemy4.pos,self.enemy4.size),self.score,'bad')
            
            elif enemy4_Type == 0:
                self.enemy4.pos, self.score = update_posandscore((self.hero.pos,self.hero.size),(self.enemy4.pos,self.enemy4.size),self.score,'good')
        
        elif collides((self.hero.pos,self.hero.size),(self.enemy5.pos,self.enemy5.size)):
            self.enemy5.pos,self.score = update_posandscore((self.hero.pos,self.hero.size),(self.enemy5.pos,self.enemy5.size),self.score,'good')
        
        
        
        if self.score != check_score:
            my_random = random.randrange(0,2)
            if my_random<1: 
                self.enemy4.source = ('assets/powerup.png')
                enemy4_Type = 0
            else:
                self.enemy4.source = ('assets/toxic_mushroom.png')
                enemy4_Type = 1
                
                       
            print(my_random)
                
         
        if self.score < -2:
            screen_manager.current = 'game_over_screen'     
    
    
    def on_enter(self, **kwargs):
        
        
        self._keyboard = Window.request_keyboard(
                self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)

        
        
        self.pressed_keys = set()
        Clock.schedule_interval(self.move_step, 0)
        
        with self.canvas:
            self.hero = Rectangle(source='assets/Pickachu_sitting.png', pos=(1,2 ), size=(100, 100),)
            
            self.enemy = Rectangle(source='assets/orange.png', pos=(random.randint(50,750), random.randint(50,560)), size=(80, 50))

            self.enemy2 = Rectangle(source='assets/apple.png', pos=(random.randint(50,750), random.randint(50,560)), size=(45,50))

            self.enemy3 = Rectangle(source='assets/pineapple.png', pos=(random.randint(50,750), random.randint(50,560)), size=(80,65) )
            
            self.enemy4 = Rectangle(source='assets/toxic_mushroom.png',pos=(random.randint(50,750), random.randint(50,560)), size=(50,50))

            self.enemy5 = Rectangle(source='assets/pizza.png',pos=(random.randint(50,750), random.randint(50,560)), size=(50,50))

            















screen_manager = ScreenManager()
screen_manager.add_widget(Menu(name ="screen_one"))
screen_manager.add_widget(soccerscreen(name = 'football_game'))
screen_manager.add_widget(SnakeGame(name ="Snake_game"))
screen_manager.add_widget(PokemonFoodPicker(name = 'food_picker'))
screen_manager.add_widget(game_over(name = 'game_over_screen'))
# screen_manager.add_widget(ScreenFour(name ="screen_four"))
# screen_manager.add_widget(ScreenFive(name ="screen_five"))
# screen_manager.current = 'game_over_screen'

# Create the App class
# Create the App class


# def restart(self):
#     self.root.clear_widgets()
#     self.stop()
#     return ScreenApp.run()
 
    
class ScreenApp(App):
    def build(self):
        return screen_manager


if __name__ == "__main__":
    ScreenApp().run()