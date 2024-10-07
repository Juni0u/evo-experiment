import pygame, math, random

class Creature():
    def __init__(self,id,x:int,y:int,color:tuple,born_in:int,chromosome:str):
        """Gene:
        [0,0,0,0,0|0,0,0,0,0,0|0,0,0|0,0,0,0|0,0,0,0]
        0-------4|5--------10|11-13|14---17|18---21|
        | max_sta | chance_act| spd |vis_rad|rpd_thr|"""
        self.id = id
        self.x = x
        self.y = y
        self.color = color
        self.age = 0
        self.born_in = born_in
        self.chromosome = chromosome
        if len(chromosome) != 22: raise ValueError("Chromosome does not have the right size.")

    def birth(self):
        self.max_stamina = int(self.chromosome[0:5],2)
        self.chance_to_act = int(self.chromosome[5:11],2)/100
        self.speed = int(self.chromosome[11:14],2)/100
        self.vision_radius = int(self.chromosome[14:18],2)
        self.reprodution_thresold = int(self.chromosome[18:22],2)

    def update(self,seed):
        if self.age==0: self.birth()
        if random.random() > self.chance_to_act:
            self.move(direction=[random.random(),random.random()])
            print(f"{self.id} moved to {self.x}")

    def draw(self,canvas):
        canvas.set_at((int(self.x),int(self.y)), self.color)  # red pixel)

    def direction_with_point(self,target:list):
        """Returns an unitary vector [x,y] that points to the target [x,y]"""
        vector = [target[0]-self.x, target[1]-self.y]
        lenght = math.sqrt(vector[0]**2 + vector[1]**2)
        if lenght!=0:
            direction = [self.x+vector[0]/lenght, self.y+vector[1]/lenght]
        else:
            direction = [0,0]
        return direction

    def move(self,direction):
        self.x += direction[0] * self.speed
        self.y += direction[1] * self.speed