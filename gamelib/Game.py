import os
class Game():
    def __init__(self,name='Game',board = None, menu = []):
        self.name = name
        self.board = board
        self.menu = menu
    
    def add_menu_entry(self,shortcut,message):
        self.menu.append({'shortcut' : shortcut,'message':message})
    
    def print_menu(self):
        for k in self.menu:
            print( f"{k['shortcut']} - {k['message']}" )
    
    def clear_screen(self):
        os.system('clear')