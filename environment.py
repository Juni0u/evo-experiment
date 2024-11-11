from config import Parameters
import pygame, random, uuid

class Environment():
    def __init__(self) -> None:
        self.parameter = Parameters()
        self.standart_energy = self.parameter.sun_energy
        self.size = self.parameter.resolution
        self.regions = []

    def create_new_region(self,x0:int,y0:int,w:int,h:int,given_energy:float):
        new_region = Region(x0,y0,w,h,given_energy)
        self.regions.append(new_region)
        return new_region

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
        else: food = self.standart_energy
        return food

class Region():
    def __init__(self,x0:int,y0:int,w:int,h:int,given_energy: float) -> None:
        self.rect = pygame.Rect(x0,y0,w,h)
        self.id = f"region-{uuid.uuid4()}"
        self.x=x0
        self.y=y0
        self.w=w
        self.h=h
        self.food_available = given_energy 

    def __hash__(self) -> int:
        return hash(self.id)
    
    def __eq__(self, value: "Region") -> bool:
        return (self.id==value.id)