from global_vars import SUN_ENERGY, RESOLUTION
import pygame, random

class Environment():
    def __init__(self) -> None:
        self.standart_energy = SUN_ENERGY
        self.size = RESOLUTION
        self.regions = []

    def create_new_region(self,x0:int,y0:int,w:int,h:int,given_energy:float):
        self.regions.append(Region(x0,y0,w,h,given_energy))

    def energy_given(self,rect:"pygame.Rect"):
        """Checks collision to all existing regions and return the energy earned based on it.
        If there is collision between 2 regions, chose one value randomly"""
        regions_collided = []
        for region in self.regions:
            if rect.colliderect(region):
                regions_collided.append(region)
        if len(regions_collided) > 0: 
            chosen = random.choice(regions_collided)
            food = chosen.food_available
        else: food = SUN_ENERGY
        return food

class Region():
    def __init__(self,x0:int,y0:int,w:int,h:int,given_energy: float) -> None:
        self.rect = pygame.Rect(x0,y0,w,h)
        self.food_available = given_energy
    
        
