
import pygame as pg
import sys


class Event:
    def __init__(self,clock) -> None:
        self.destroy = False
        self.delete = False
        self.troop = None
        self.changing_pos = False
        self.clock = clock
        self.timer = 0
        self.get_move_resource = False
        self.get_resource = False
        self.resource_available = True
        self.dt = clock.tick(30)/1000
        self.game_time = Game_time()
    #capture the events
    def events(self):
        for event in pg.event.get():
            #Exit the game by clicking the red cross
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            #Exit game by pressing escape (Echap in fr)  button on the keyboard
            if event.type == pg.KEYDOWN:
                
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

                if event.key == pg.K_DELETE:
                    self.destroy = True
                    self.timer = 0.0001

                if event.key == pg.K_RETURN:
                    print("Enter function here")



    def set_destroy(self):
        self.destroy = True
        self.update_destroy()


    def remise(self):
        self.destroy = False

    def get_destroy(self):
        return self.destroy

    def update_destroy(self):
        if (self.timer != 0):
            if (self.timer > 0.5):
                #print("too late")
                self.timer = 0
                self.destroy = False
            else:
                self.timer += self.dt
        return self.destroy

    def update_delete(self):
        if (self.timer != 0):
            if (self.timer > 0.5):
                #print("too late")
                self.timer = 0
                self.delete = False
            else:
                self.timer += self.dt
        return self.delete

    def create_troop(self, troop):
        self.troop = str(troop)

    def get_troop(self):
        return self.troop

    def remise_troop(self):
        self.troop = None

    def change_unit_pos(self):
        self.changing_pos = True

    def remise_moving_troop(self):
        self.changing_pos = False

    def get_grid_pos_unit(self):
        return self.changing_pos

    def getting_resource(self):
        self.get_resource = True




class Game_time:
    def __init__(self):
        #self.hour = 0
        self.minute = 0
        self.second = 0
    def get_time(self):
        return self.minute,self.second
    def update(self):
        if (self.second >= 60):
            self.minute += 1
            self.second = 0
        # if (self.minute >= 60):
        #     self.hour += 1
        #     self.minute = 0 
