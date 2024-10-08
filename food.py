import pygame, random
from typing import Optional

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

    def spawnFood(self) -> Optional["Food"]:
        if self.capacity > 0 and random.random() <= self.food_spawn_chance:
            F = Food(x=self.x+random.randint(-self.spawn_radius,self.spawn_radius),y=self.y+random.randint(-self.spawn_radius,self.spawn_radius),energy=self.food_max_energy)
            self.capacity -= 1
            return F
        return None
    
    def update(self,Foods) -> list:
        F = self.spawnFood()
        if F: Foods.append(F)
        return Foods


class Food():
    def __init__(self,x:int,y:int,energy:int) -> None:
        self.x = x
        self.y = y
        self.color = (0,255,0) #green
        self.energy = energy

    def draw(self, canvas) -> None:
        canvas.set_at((int(self.x),int(self.y)), self.color) 
