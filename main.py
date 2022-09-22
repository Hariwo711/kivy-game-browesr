import kivy 
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget

import random
from kivy.app import App
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty, BooleanProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Rectangle

from kivy.core.audio import SoundLoader

# kv = Builder.load_file("screen.kv")
kv = Builder.load_file("screen.kv")

#Setsup The menu screen from .kv file
class Menu(Screen):
    pass

class game_over(Screen):

    pass

class winning(Screen):
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





SnakeGamePoints = 1

Height = 400
Width = 400

Current_Button_press=0

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
class SnakeTail(Widget):

    def move(self, new_pos):
        self.pos = new_pos

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
        global Current_Button_press
        cur_x = self.hero.pos[0]
        cur_y = self.hero.pos[1]
        step =  self.score * 0.75
        if self.score < 20 :
            step =  self.score * 0.75
        elif self.score > 20:
            step =  20 * 0.75
        if 'w' in self.pressed_keys:
            # cur_y += step
            Current_Button_press= 'w'
        elif 's' in self.pressed_keys:
            # cur_y -= step
            Current_Button_press= 's'
        elif 'a' in self.pressed_keys:
            # cur_x -= step
            Current_Button_press= 'a'
        elif 'd' in self.pressed_keys:
            # cur_x += step
            Current_Button_press= 'd'

        print(Current_Button_press)
        
        def check_Button_and_move(button,cur_x,cur_y,step):
            if button == 'w':
                cur_y += step
            elif button == 's':
                cur_y -= step
            elif button == 'a':
                cur_x -= step
            elif button == 'd':
                cur_x += step
            
            
            return cur_x,cur_y

        
        
        self.hero.pos = (check_Button_and_move(Current_Button_press,cur_x,cur_y,step))   
        
        self.tail.pos = (int(self.hero.pos[0])-42,int(self.hero.pos[1]))
        
        if Current_Button_press =='w':
            self.tail.pos = (int(self.hero.pos[0]),int(self.hero.pos[1])-42)
        elif Current_Button_press == 's':
            self.tail.pos = (int(self.hero.pos[0]),int(self.hero.pos[1])+42)
        elif Current_Button_press == 'a':
            self.tail.pos = (int(self.hero.pos[0])+42,int(self.hero.pos[1]))
        elif Current_Button_press == 'd':
            self.tail.pos = (int(self.hero.pos[0])-42,int(self.hero.pos[1]))
        
        if collides((self.hero.pos,self.hero.size),(self.enemy.pos,self.enemy.size)):
            print("colliding!")
            
            
            self.sound = SoundLoader.load('assets/eating_sound.wav')
            self.sound.play()
            
            self.enemy.pos = (random.randint(50,400), random.randint(50,400))
            self.score += 1
            print(self.score)
        # else:
            # print("not colliding!")
        # if self.score += 1 
        if self.score > 30:
            screen_manager.current = 'winning_screen'

    def on_enter(self, **kwargs):

        self._keyboard = Window.request_keyboard(
             self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)

        self.pressed_keys = set()
        Clock.schedule_interval(self.move_step, 0)
        
        with self.canvas:
            self.hero = Rectangle (pos=(200,100 ), size=(40, 40))
            def tail_build(name_of_tail ,pos_Of_tail, number_of_tail):
                self.name_of_tail.pos = (pos_Of_tail)
                return True
            
            self.tail = Rectangle (pos = (int(self.hero.pos[0])-0,int(self.hero.pos[1])), size=(40,40))
            self.enemy = Rectangle( pos=(random.randint(50,750), random.randint(50,560)), size=(40, 40))
        print(self.hero.pos[1])


        self.sound = SoundLoader.load('assets/relaxing_music.mp3')
        self.sound.play()

    def on_leave(self, *args):
        self.sound.stop()


def update_posandscore(hero_posandsize,enemy_posandsize,score,goodorbad):
    enemy_posandsize = (random.randint(50,750), random.randint(50,560))
    
    if goodorbad == 'good':
        score += 1
    elif goodorbad == 'bad':
        score -= 1
    elif goodorbad == 'super_good':
        score += 2 
    elif goodorbad == 'super_bad':
        score -= 3
    return enemy_posandsize,score
#Uses Colision Function

food_choice = 0

enemy4_Type = 1

PokenmonGamePoints = 0


class PokemonFoodPicker(Screen):
    score = NumericProperty(PokenmonGamePoints)
    food_choice = StringProperty(food_choice)
    
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
        global food_choice
        
        cur_x = self.hero.pos[0]
        cur_y = self.hero.pos[1]

        step = 500 * dt

        #check if good or bad
        def checkgoodorbad(enemy_type, food_choice_fn):
            
            if enemy_type == food_choice_fn:
                return 'good'
            else:
                return 'bad'

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
            self.enemy.pos,self.score = update_posandscore((self.hero.pos,self.hero.size),(self.enemy.pos,self.enemy.size),self.score, checkgoodorbad('Orange',self.food_choice))
        
        elif collides((self.hero.pos,self.hero.size),(self.enemy2.pos,self.enemy2.size)):
            self.enemy2.pos,self.score = update_posandscore((self.hero.pos,self.hero.size),(self.enemy2.pos,self.enemy2.size),self.score, checkgoodorbad('Apple',self.food_choice))
        
        elif collides((self.hero.pos,self.hero.size),(self.enemy3.pos,self.enemy3.size)):
            self.enemy3.pos,self.score = update_posandscore((self.hero.pos,self.hero.size),(self.enemy3.pos,self.enemy3.size),self.score, checkgoodorbad('Pineapple',self.food_choice))
        
        elif collides((self.hero.pos,self.hero.size),(self.enemy4.pos,self.enemy4.size)):
            if enemy4_Type == 1:
                print('test if true')
                self.enemy4.pos, self.score = update_posandscore((self.hero.pos,self.hero.size),(self.enemy4.pos,self.enemy4.size),self.score,'super_bad')
            
            elif enemy4_Type == 0:
                self.enemy4.pos, self.score = update_posandscore((self.hero.pos,self.hero.size),(self.enemy4.pos,self.enemy4.size),self.score,'super_good')
        
        elif collides((self.hero.pos,self.hero.size),(self.enemy5.pos,self.enemy5.size)):
            self.enemy5.pos,self.score = update_posandscore((self.hero.pos,self.hero.size),(self.enemy5.pos,self.enemy5.size),self.score,checkgoodorbad('Pizza',self.food_choice))
        
        elif collides((self.hero.pos,self.hero.size),(self.enemy6.pos,self.enemy6.size)):
            self.enemy6.pos, self.score = update_posandscore((self.hero.pos,self.hero.size),(self.enemy6.pos,self.enemy6.size),self.score,'super_bad')
        
        elif collides((self.hero.pos,self.hero.size),(self.enemy7.pos,self.enemy7.size)):
            self.enemy7.pos, self.score = update_posandscore((self.hero.pos,self.hero.size),(self.enemy7.pos,self.enemy7.size),self.score,'super_bad')
        
        #things to do when getting a point
        if self.score != check_score:
            my_random = random.randrange(0,6)
            
            food_types = ["Orange","Apple","Pineapple","Pizza"]
            #chocing Food Type you need to eat
            self.food_choice = random.choice(food_types)
            print(self.food_choice)
            if my_random<1: 
                self.enemy4.source = ('assets/powerup.png')
                enemy4_Type = 0
            else:
                self.enemy4.source = ('assets/toxic_mushroom.png')
                enemy4_Type = 1
                
                       
            print('Your random number is',my_random)
                
         
        if self.score < 0:
            screen_manager.current = 'game_over_screen'
        elif self.score > 2:
            screen_manager.current = 'winning_screen'
    
    def on_enter(self, **kwargs):
        global food_choice
        
        food_types = ["Orange","Apple","Pineapple","Pizza"]
        
        #chocing Food Type you need to eat
        self.food_choice = random.choice(food_types)
        
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

            self.enemy6 = Rectangle(source='assets/toxic_mushroom.png',pos=(random.randint(50,750), random.randint(50,560)), size=(50,50))            
            
            self.enemy7 = Rectangle(source='assets/toxic_mushroom.png',pos=(random.randint(50,750), random.randint(50,560)), size=(50,50))
    
    def on_leave(self, *args):
        
        if self.score < 0:
            self.sound = SoundLoader.load('assets/mario_OH_no.mp3')
        elif self.score > 2:
            self.sound = SoundLoader.load('assets/pika_pika.mp3')
        self.sound.play()














screen_manager = ScreenManager()
screen_manager.add_widget(Menu(name ="screen_one"))
screen_manager.add_widget(soccerscreen(name = 'football_game'))
screen_manager.add_widget(SnakeGame(name ="Snake_game"))
screen_manager.add_widget(PokemonFoodPicker(name = 'food_picker'))
screen_manager.add_widget(game_over(name = 'game_over_screen'))
screen_manager.add_widget(winning(name = 'winning_screen'))
# screen_manager.add_widget(ScreenFour(name ="screen_four"))
# screen_manager.add_widget(ScreenFive(name ="screen_five"))
# screen_manager.current = 'winning_screen'

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