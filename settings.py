from os import path





TILE_SIZE = 64
TILE_SIZE_MINI_MAP = 4

#colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
HUD_COLOUR = (198, 155, 93, 175)



#Paths definitions
#Gameplay folder
AOE_folder = path.dirname(__file__) #Path of the Project_Python_AoE foler
graphics_folder = path.join(AOE_folder,"assets/graphics") #Path for graphic