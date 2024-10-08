import pygame, random
from typing import Optional
from global_vars import FOOD_STANDARD_COLOR, RESOLUTION

class FoodSpawner():
    def __init__(self,x:int,y:int,capacity:int,spawn_radius:int,food_max_energy:int,food_spawn_chance:float,rest_time:int) -> None:
        self.x = x
        self.y = y
        self.color = (0,125,0) #dark green
        self.capacity = capacity
        self.max_capacity = capacity
        self.spawn_radius = spawn_radius
        self.food_max_energy = food_max_energy
        self.food_spawn_chance = food_spawn_chance
        self.rest_time = rest_time
        self.state="spawning" #spawning \ resting

    def draw(self, canvas) -> None:
        canvas.set_at((int(self.x),int(self.y)), self.color) 
        for ix in range(-1,2):
            for iy in range(-1,2):
                canvas.set_at((int(self.x+ix),int(self.y+iy)), self.color) 

    def spawnFood(self,canvas) -> Optional["Food"]:
        pos=[self.x+random.randint(-self.spawn_radius,self.spawn_radius),self.y+random.randint(-self.spawn_radius,self.spawn_radius)]
        if pos[0] > RESOLUTION[0]-1: pos[0] = RESOLUTION[0]-1
        elif pos[0] < 0: pos[0] = 0
        if pos[1] > RESOLUTION[1]-1: pos[1] = RESOLUTION[1]-1
        elif pos[1] < 0: pos[1] = 0
        
        if (self.capacity > 0) and (random.random() <= self.food_spawn_chance) and not (self.is_pixel_food(canvas,pos)):
            F = Food(x=pos[0],y=pos[1],energy=self.food_max_energy)
            self.capacity -= 1
            return F
        if (self.capacity <= 0): 
            self.state="resting"
        return None
    
    def is_pixel_food(self,canvas,pos):
        pixel_color = canvas.get_at(pos)
        if pixel_color==FOOD_STANDARD_COLOR: return True
        else: return False

    def update(self,Foods,canvas) -> list:
        if self.state=="spawning":
            F = self.spawnFood(canvas)
            if F: Foods.append(F)
        elif self.state=="resting":
            self.capacity += self.max_capacity/self.rest_time
            if self.capacity>=self.max_capacity:
                self.state="spawning"
        return Foods

class Food():
    def __init__(self,x:int,y:int,energy:int) -> None:
        self.x = x
        self.y = y
        self.color = FOOD_STANDARD_COLOR
        self.rect = pygame.Rect(x,y,1,1)
        self.energy = energy

    def draw(self, canvas) -> None:
        canvas.set_at((int(self.x),int(self.y)), self.color) 
