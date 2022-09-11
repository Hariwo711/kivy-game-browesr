import kivy 
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget


kv = Builder.load_file("screen.kv")


class ScreenOne(Screen):
    pass
  
class ScreenTwo(Screen):
    pass
 
class ScreenThree(Screen):
    pass
 
class ScreenFour(Screen):
    pass
 
class ScreenFive(Screen):
    pass



screen_manager = ScreenManager()
screen_manager.add_widget(ScreenOne(name ="screen_one"))
screen_manager.add_widget(ScreenTwo(name ="screen_two"))
screen_manager.add_widget(ScreenThree(name ="screen_three"))
screen_manager.add_widget(ScreenFour(name ="screen_four"))
screen_manager.add_widget(ScreenFive(name ="screen_five"))


# Create the App class
# Create the App class
class ScreenApp(App):
    def build(self):
        return screen_manager

if __name__ == "__main__":
    ScreenApp().run()