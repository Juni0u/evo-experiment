import pygame, random
from typing import Optional
from global_vars import FOOD_STANDARD_COLOR

class FoodSpawner():
    def __init__(self,x:int,y:int,capacity:int,spawn_radius:int,food_max_energy:int,food_spawn_chance:float) -> None:
        self.x = x
        self.y = y
        self.color = (0,125,0) #dark green
        self.capacity = capacity
        self.spawn_radius = spawn_radius
        self.food_max_energy = food_max_energy
        self.food_spawn_chance = food_spawn_chance

    def draw(self, canvas) -> None:
        canvas.set_at((int(self.x),int(self.y)), self.color) 
        for ix in range(-1,2):
            for iy in range(-1,2):
                canvas.set_at((int(self.x+ix),int(self.y+iy)), self.color) 

    def spawnFood(self,canvas) -> Optional["Food"]:
        pos=(self.x+random.randint(-self.spawn_radius,self.spawn_radius),self.y+random.randint(-self.spawn_radius,self.spawn_radius))
        if (self.capacity > 0) and (random.random() <= self.food_spawn_chance) and not (self.is_pixel_food(canvas,pos)):
            F = Food(x=pos[0],y=pos[1],energy=self.food_max_energy)
            self.capacity -= 1
            return F
        return None
    
    def is_pixel_food(self,canvas,pos):
        pixel_color = canvas.get_at(pos)
        if pixel_color==FOOD_STANDARD_COLOR: return True
        else: return False

    def update(self,Foods,canvas) -> list:
        F = self.spawnFood(canvas)
        if F: Foods.append(F)
        return Foods


class Food():
    def __init__(self,x:int,y:int,energy:int) -> None:
        self.x = x
        self.y = y
        self.color = FOOD_STANDARD_COLOR
        self.body = pygame.Rect(x,y,1,1)
        self.energy = energy

    def draw(self, canvas) -> None:
        canvas.set_at((int(self.x),int(self.y)), self.color) 
