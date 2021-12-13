# from game.buildings import LumberMill, TownCenter
from settings import *
import pygame as pg
from .utils import draw_text
from os import path
from .button import *
from game.units import Archer, Infantryman, Villager
from game.buildings import *
from resource import *


class Gui:

    def __init__(self, resource_manager, width, height, events):

        self.resource_manager = resource_manager
        self.width = width
        self.height = height
        self.events = events
        self.gui_colour = GUI_COLOUR

        # resource gui
        self.resources_surface = pg.Surface((width, height * 0.02), pg.SRCALPHA)
        self.resources_rect = self.resources_surface.get_rect(topleft=(0, 0))
        self.resources_surface.fill(self.gui_colour)

        # building gui
        self.build_surface = pg.Surface((width * 0.15, height * 0.25), pg.SRCALPHA)
        self.build_rect = self.build_surface.get_rect(topleft=(self.width * 0.84, self.height * 0.74))
        self.build_surface.fill(self.gui_colour)

        # select gui
        self.select_surface = pg.Surface((width * 0.3, height * 0.2), pg.SRCALPHA)
        self.select_rect = self.select_surface.get_rect(topleft=(self.width * 0.35, self.height * 0.79))
        self.select_surface.fill(self.gui_colour)

        self.images = self.load_images()

        # create a new gui
        self.tiles = self.create_build_gui()

        # choose tree, rock or gold
        self.choose = None
        self.selected_tile = None
        self.examined_tile = None
        self.mining_gui = False
        self.examined_unit = None

    # afficher les batiments pour choisir et construire
    def create_build_gui(self):

        # position in the inventory
        render_pos = [self.width * 0.84 + 10, self.height * 0.74 + 10]  # 0.84 0.74
        object_width = self.build_surface.get_width() // 8

        tiles = []
        # print('create_build_gui')
        for image_name, image in self.images.items():  # ajouter l'image dans la fonction load_image()
            # print('in for create_build_gui')
            pos = render_pos.copy()
            image_tmp = image.copy()
            image_scale = self.scale_image(image_tmp, w=object_width)
            # choose the rect around the entity
            rect = image_scale.get_rect(topleft=pos)  # center

            tiles.append(
                {
                    "name": image_name,
                    "icon": image_scale,
                    "image": self.images[image_name],
                    "rect": rect,
                    "affordable": True
                    # on peut ajouter plusieurs attributs ici
                }
            )

            # position in inventory for each entity
            render_pos[0] += image_scale.get_width() + 10

        return tiles

    def update(self):
        # work in inventory
        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()
        # unselect entity
        if mouse_action[2]:
            self.selected_tile = None

        for tile in self.tiles:
            if self.resource_manager.is_affordable(tile["name"]):
                tile["affordable"] = True
            else:
                tile["affordable"] = False
            if tile["rect"].collidepoint(mouse_pos) and tile["affordable"]:
                # tile["rect"] is defined in create_build_gui()
                if mouse_action[0]:
                    self.selected_tile = tile

    def draw(self, screen):

        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()
        # resource
        screen.blit(self.resources_surface, (0, 0))
        # build gui
        screen.blit(self.build_surface, (self.width * 0.84, self.height * 0.74))
        # select gui

        button6 = Button(screen, (50, 200), '| |', 45, 'white on black')
        button6.button()
        if mouse_action[0] and button6.rect.collidepoint(mouse_pos):
            print("coucou")

        if self.examined_unit is not None:

            mouse_pos = pg.mouse.get_pos()
            mouse_action = pg.mouse.get_pressed()

            w, h = self.select_rect.width, self.select_rect.height
            screen.blit(self.select_surface, (self.width * 0.35, self.height * 0.79))
            if self.examined_unit.game_name == 'Archer':
                img = archer
                img_scale = self.scale_image(img, h=h * 0.70)
                health = format(str(self.examined_unit.health))
                health_max = format(str(self.examined_unit.health_max))
                draw_text(screen, f"Vie: {health} / {health_max}", 20, WHITE,
                          (self.width * 0.35 + 300, self.height * 0.79 + 50))
                screen.blit(img_scale, (self.width * 0.35 + 10, self.height * 0.79 + 10))
                draw_text(screen, str(self.examined_unit.game_name), 20, WHITE,
                          (self.width * 0.35 + 300, self.height * 0.79 + 20))
                if mouse_action[2]:
                    self.events.change_unit_pos()

            if self.examined_unit.game_name == 'Villageois':
                img = villager
                img_scale = self.scale_image(img, h=h * 0.70)
                health = format(str(self.examined_unit.health))
                health_max = format(str(self.examined_unit.health_max))
                draw_text(screen, f"Vie: {health} / {health_max}", 20, WHITE,
                          (self.width * 0.35 + 300, self.height * 0.79 + 50))
                screen.blit(img_scale, (self.width * 0.35 + 10, self.height * 0.79 + 10))
                draw_text(screen, str(self.examined_unit.game_name), 20, WHITE,
                          (self.width * 0.35 + 300, self.height * 0.79 + 20))
                if mouse_action[2]:
                    self.events.change_unit_pos()

            if self.examined_unit.game_name == 'Barbare':
                img = infantryman
                img_scale = self.scale_image(img, h=h * 0.70)
                health = format(str(self.examined_unit.health))
                health_max = format(str(self.examined_unit.health_max))
                draw_text(screen, f"Vie: {health} / {health_max}", 20, WHITE,
                          (self.width * 0.35 + 300, self.height * 0.79 + 50))
                draw_text(screen, str(self.examined_unit.game_name), 20, WHITE,
                          (self.width * 0.35 + 300, self.height * 0.79 + 20))
                screen.blit(img_scale, (self.width * 0.35 + 10, self.height * 0.79 + 10))
                if mouse_action[2]:
                    self.events.change_unit_pos()

        if self.choose is not None and (not self.mining_gui):
            w, h = self.select_rect.width, self.select_rect.height
            screen.blit(self.select_surface, (self.width * 0.35, self.height * 0.79))
            if self.choose["tile"] == 'Arbre':
                img = Tree_img
                img_scale = self.scale_image(img, h=h * 0.9)
                draw_text(screen, "Rest: " + str(self.choose["class"].get_rest()), 20, BLUE,
                          (self.width * 0.35 + 300, self.height * 0.79 + 50))
                screen.blit(img_scale, (self.width * 0.35 + 10, self.height * 0.79 + 10))
            if self.choose["tile"] == 'Carrière de pierre':
                img = Rock_img
                img_scale = self.scale_image(img, h=h * 0.9)
                screen.blit(img_scale, (self.width * 0.35 + 10, self.height * 0.79 + 10))
                draw_text(screen, "Rest: " + str(self.choose["class"].get_rest()), 20, BLUE,
                          (self.width * 0.35 + 300, self.height * 0.79 + 50))
            if self.choose["tile"] == "Mine d'or":
                img = Gold_img
                img_scale = self.scale_image(img, h=h * 0.9)
                screen.blit(img_scale, (self.width * 0.35 + 10, self.height * 0.79 + 10))
                draw_text(screen, "Rest: " + str(self.choose["class"].get_rest()), 20, BLUE,
                          (self.width * 0.35 + 300, self.height * 0.79 + 50))
            draw_text(screen, self.choose["tile"], 40, WHITE, (self.width * 0.35 + 300, self.height * 0.79 + 10))

        if self.examined_tile is not None:
            w, h = self.select_rect.width, self.select_rect.height
            screen.blit(self.select_surface, (self.width * 0.35, self.height * 0.79))
            img = self.examined_tile.image.copy()
            img_scale = self.scale_image(img, h=h * 0.7)
            screen.blit(img_scale, (self.width * 0.35 + 10, self.height * 0.79 + 40))
            # text in information box
            health = format(str(self.examined_tile.health))
            health_max = format(str(self.examined_tile.health_max))
            draw_text(screen, self.examined_tile.game_name, 40, WHITE, self.select_rect.topleft)
            draw_text(screen, f"Vie: {health} / {health_max}", 20, WHITE, self.select_rect.center)
            draw_text(screen, "{} team".format(self.examined_tile.team), 20, pg.Color(self.examined_tile.team),
                      (self.width * 0.35 + 290, self.height * 0.79))

            if self.examined_tile.name == "TownCenter":
                button = Button(screen, (self.width * 0.6, self.height * 0.9 + 60), 'Détruire', 15, 'white on red')
                button.button()
                mouse_action = pg.mouse.get_pressed()
                mouse_pos = pg.mouse.get_pos()
                if mouse_action[0] and button.rect.collidepoint(mouse_pos):
                    button.button("black on blue")
                    self.events.set_destroy()
                    # Code pour le bouton permettant de détruire le forum

                button2 = Button(screen, (self.width * 0.6 - 75, self.height * 0.9 + 60), 'Villageois', 15,
                                 'white on black')
                button2.button()
                mouse_pos = pg.mouse.get_pos()
                mouse_action = pg.mouse.get_pressed()
                if mouse_action[0] and button2.rect.collidepoint(mouse_pos):
                    button2.button("black on green")
                    self.events.remise()
                    self.events.create_troop('villager')
                    self.events.get_troop()  # retourne villager
                    # Code pour le bouton permettant de créer un villageois

                button3 = Button(screen, (self.width * 0.6 - 90, self.height * 0.9 + 60), 'Z', 15, 'white on black')
                button3.button()
                # mouse_pos = pg.mouse.get_pos()
                # mouse_action = pg.mouse.get_pressed()
                if mouse_action[0] and button3.rect.collidepoint(mouse_pos):
                    self.events.remise()
                    button3.button("black on green")
                    print('clicked2')

            if self.examined_tile.name == "Barracks":
                button = Button(screen, (self.width * 0.6, self.height * 0.9 + 60), 'Détruire', 15, 'white on red')
                button.button()
                mouse_pos = pg.mouse.get_pos()
                mouse_action = pg.mouse.get_pressed()
                if mouse_action[0] and button.rect.collidepoint(mouse_pos):
                    button.button("black on blue")
                    self.events.set_destroy()
                    # Code pour le bouton permettant de détruire la caserne

                button2 = Button(screen, (self.width * 0.6 - 100, self.height * 0.9 + 60), 'Barbare', 15,
                                 'white on black')
                button2.button()
                mouse_pos = pg.mouse.get_pos()
                mouse_action = pg.mouse.get_pressed()
                if mouse_action[0] and button2.rect.collidepoint(mouse_pos):
                    button2.button("black on green")
                    self.events.remise()
                    # print('Infantryman created')
                    self.events.create_troop('infantryman')
                    self.events.get_troop()
                    # Code pour le bouton permettant de créer un barbare

            if self.examined_tile.name == "Archery":
                button = Button(screen, (self.width * 0.6, self.height * 0.9 + 60), 'Détruire', 15, 'white on red')
                button.button()
                mouse_pos = pg.mouse.get_pos()
                mouse_action = pg.mouse.get_pressed()
                if mouse_action[0] and button.rect.collidepoint(mouse_pos):
                    button.button("black on blue")
                    self.events.set_destroy()
                    # Code pour le bouton permettant de détruire l'archerie

                button2 = Button(screen, (self.width * 0.6 - 60, self.height * 0.9 + 60), 'Archer', 15,
                                 'white on black')
                button2.button()
                mouse_pos = pg.mouse.get_pos()
                mouse_action = pg.mouse.get_pressed()
                if mouse_action[0] and button2.rect.collidepoint(mouse_pos):
                    button2.button("black on green")
                    self.events.remise()
                    # print('Archer created')
                    self.events.create_troop('archer')
                    self.events.get_troop()
                    # Code pour le bouton permettant de créer un archer

            if self.examined_tile.name == "LumberMill":
                button = Button(screen, (self.width * 0.6, self.height * 0.9 + 60), 'Détruire', 15, 'white on red')
                button.button()
                mouse_pos = pg.mouse.get_pos()
                mouse_action = pg.mouse.get_pressed()
                if mouse_action[0] and button.rect.collidepoint(mouse_pos):
                    button.button("black on blue")
                    self.events.set_destroy()
                    # Code pour le bouton permettant de détruire le moulin

        # icon for entity selecting
        for tile in self.tiles:
            icon = tile["icon"].copy()
            if not tile["affordable"]:
                icon.set_alpha(100)
            screen.blit(icon, tile["rect"].topleft)

        # resource
        pos = self.width - 420  # resource info position

        for resource, resource_value in self.resource_manager.starting_resources.items():
            txt = resource + ": " + str(resource_value)
            draw_text(screen, txt, 25, WHITE, (pos, 0))
            pos += 100
            """
        for resource in ["wood:{}".format(500), "stone:{}".format(250), "gold:{}".format(100),"food: {}".format(230)]:
            draw_text(screen, resource, 25, WHITE, (pos, 0))
            pos += 100
            """

    def load_images(self):
        # read images
        # all images are saved in folder assets/graphics
        # Rock_image = Rock_img
        # Tree_image = Tree_img
        TownCenter = towncenter
        LumberMill = lumbermill
        Barracks = barracks
        Archery = archery
        Archer = archer
        Infantryman = infantryman
        Villager = villager
        # tree = pg.image.load(path.join(graphics_folder,"tree.png"))
        # rock = pg.image.load(path.join(graphics_folder,"rock.png"))

        # load des images  d'unites ici
        # troop = pg.image.load(path.join(graphics_folder,"cart_E.png"))
        # troop_scale = self.scale_image(troop,self.build_surface.get_width() // 8)

        # on peut l'appeller sous le nom "image_name" comme dans la ligne 63
        images = {
            "TownCenter": TownCenter,
            "LumberMill": LumberMill,
            "Barracks": Barracks,
            "Archery": Archery,
            # "tree": Tree_img,
            # "rock": Rock_img
            # "Archer" : Archer
            # "troop": troop
            # ajouter les images d'unites ici
            # example "troop": troop;
        }
        return images

    def scale_image(self, image, w=None, h=None):

        if (w == None) and (h == None):
            pass
        elif h == None:
            scale = w / image.get_width()
            h = scale * image.get_height()
            image = pg.transform.scale(image, (int(w), int(h)))
        elif w == None:
            scale = h / image.get_height()
            w = scale * image.get_width()
            image = pg.transform.scale(image, (int(w), int(h)))
        else:
            image = pg.transform.scale(image, (int(w), int(h)))

        return image