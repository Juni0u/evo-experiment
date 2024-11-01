import pygame, random
from markov_chain import MarkovChain
from typing import Optional
from global_vars import PLANTS_COLOR,PLANT_MAX_HEALTH_DIVISIONS, PLANT_BASE_COLOR, PLANT_SPAWN_RADIUS, FOOD_STANDARD_COLOR, RESOLUTION, SUN_ENERGY, FOOD_SPROUT_CHANCE
#TODO: As frutas que evoluem para plantas n:ao tem o thresold de energia porque nunca passando por create states with health

class Plant():
    def __init__(self,x:int,y:int, gene=[0])-> None: #health_divisions:int=0, states=[0], brain=[0]) -> None:
        self.x = x
        self.y = y
        self.color = PLANT_BASE_COLOR      
        self.spawn_radius = PLANT_SPAWN_RADIUS
        self.age = 0
        self.state = "idle0" 
        self.gene = gene
        self.translation(self.gene)
        
    def draw(self, canvas) -> None:
        canvas.set_at((int(self.x),int(self.y)), self.color) 
        for ix in range(-1,2):
            for iy in range(-1,2):
                canvas.set_at((int(self.x+ix),int(self.y+iy)), self.color) 

    def update(self,Plants,Fruits,canvas):
        self.age += 1
        self.metabolize()
        self.update_state_based_on_energy()
        if (self.energy <= 0):
            Plants.remove(self)
            return Plants, Fruits
        if "eat" in self.state:
            self.eat()
        elif "reproduce" in self.state:
            F = self.spawnFood(canvas)
            if F: Fruits.append(F)
        self.state_transition()
        return Plants, Fruits

    def translation(self, gene):
        ##[self.energy_capacity,self.metabolism,self.food_spawn_thresold,self.food_spawn_chance,self.health_divisions,self.states,self.brain]
        ##[         0          ,         1     ,           2            ,         3            ,          4          ,     5     ,     6    ] 
        #self.translation(self.gene)
        if len(gene) == 1: gene = [100,5,50,0.4,random.randint(1,PLANT_MAX_HEALTH_DIVISIONS),[0],[0]]
    
        self.energy_capacity = gene[0]
        self.metabolism = gene[1]
        self.food_spawn_thresold = gene[2]
        self.food_spawn_chance = gene[3]
        self.health_divisions = gene[4]
        self.states = gene[5]
        self.brain = gene[6]
        self.energy = self.energy_capacity

        if len(self.states)==1: 
            self.states = ["idle","eat","reproduce"]
            self.create_states_with_health(self.health_divisions)
        else: 
            self.get_health_state_division(self.health_divisions)

        if not isinstance(self.brain, MarkovChain): 
            self.brain = MarkovChain(states_list=self.states)
        else: 
            self.brain = self.brain   
            self.brain.mutate_matrix() 

        self.gene = [self.energy_capacity,self.metabolism,self.food_spawn_thresold,self.food_spawn_chance,self.health_divisions,self.states,self.brain]        
        self.color_based_states()

    def color_based_states(self):
        #category_unit = (255 - PLANT_BASE_COLOR[1])/(PLANT_MAX_HEALTH_DIVISIONS*3)
        self.color = PLANTS_COLOR[self.health_divisions-1]

    def state_transition(self):
        self.state = self.brain.state_transition(current_state=self.state)

    def get_health_state_division(self, number_of_divisions) -> None:
        self.enegy_state_thresold = []
        unit_value = self.energy_capacity/number_of_divisions
        sum_thresold = 0

        for i in range(0,number_of_divisions):
            self.enegy_state_thresold.append(unit_value+sum_thresold)
            sum_thresold += unit_value

    def create_states_with_health(self, number_of_divisions:int) -> None:
        """Crete states based on % energy the plant has and combine with existing states"""
        self.enegy_state_thresold = []
        unit_value = self.energy_capacity/number_of_divisions
        sum_thresold = 0
        current_state_list = list(self.states)
        new_state_list = []

        for i in range(0,number_of_divisions):
            self.enegy_state_thresold.append(unit_value+sum_thresold)
            sum_thresold += unit_value
            for state in current_state_list:
                new_state_list.append(f"{state}{i}")
        self.states = new_state_list

    def update_state_based_on_energy(self):
        for i,thresold in enumerate(self.enegy_state_thresold):
            if self.energy <= thresold:
                self.state = self.state[:-1]+str(i)
                break         

    def eat(self, energy: float=SUN_ENERGY) -> None:
        self.energy += energy

    def metabolize(self) -> None:
        self.energy -= self.metabolism
    
    def spawnFood(self,canvas) -> Optional["Fruit"]:
        pos=[self.x+random.randint(-self.spawn_radius,self.spawn_radius),self.y+random.randint(-self.spawn_radius,self.spawn_radius)]
        if pos[0] > RESOLUTION[0]-1: pos[0] = RESOLUTION[0]-1
        elif pos[0] < 0: pos[0] = 0
        if pos[1] > RESOLUTION[1]-1: pos[1] = RESOLUTION[1]-1
        elif pos[1] < 0: pos[1] = 0
        
        if (self.energy > self.food_spawn_thresold) and (random.random() <= self.food_spawn_chance) and not (self.is_pixel_food(canvas,pos)):
            F = Fruit(x=pos[0],y=pos[1],gene=self.gene) 
            self.energy -= self.food_spawn_thresold
            return F
        return None
    
    def is_pixel_food(self,canvas,pos):
        pixel_color = canvas.get_at(pos)
        if pixel_color==FOOD_STANDARD_COLOR: return True
        else: return False

class Fruit():
    def __init__(self,x:int,y:int,gene:list) -> None:
        self.x = x
        self.y = y
        self.color = FOOD_STANDARD_COLOR
        self.sprout_chance = FOOD_SPROUT_CHANCE
        self.gene = gene 
        ##[self.energy_capacity,self.metabolism,self.food_spawn_thresold,self.food_spawn_chance,self.health_divisions,self.states,self.brain]
        ##[         0          ,         1     ,           2            ,         3            ,          4          ,     5     ,     6    ] 
        self.energy = self.gene[2]
        self.rect = pygame.Rect(x,y,1,1)        

    def draw(self, canvas) -> None:
        canvas.set_at((int(self.x),int(self.y)), self.color) 

    def update(self, Plants, Fruits):
        if self.energy <= 0:
            Fruits = self.die(Fruits)
            return Plants, Fruits
        self.energy -= 1
        if random.random() < self.sprout_chance:
            Plants, Fruits = self.sprout(Plants, Fruits)
        return Plants, Fruits

    def die(self, Fruits):
        Fruits.remove(self)
        return Fruits

    def sprout(self, Plants, Fruits):
        if self in Fruits:
            Plants.append(Plant(x=self.x, y=self.y, gene=self.gene))
            Fruits.remove(self)
            return Plants, Fruits
        return Plants, Fruits

A = Plant(70,70)

print()

#A = Plant(70,70)
# print(f"Energy states: {A.enegy_state_thresold}, Capacity: {A.energy_capacity}, Metabolism: {A.metabolism}")
# for i in range(10):
#     print()
#     A.update_state_based_on_energy()
#     print(f"Step: {i}")
#     print(f"State = {A.state}, Energy: {A.energy}")

#     A.metabolize()
#     if "eat" in A.state:
#         A.eat()
#     elif "reproduce" in A.state:
#         A.energy -= A.food_spawn_thresold

    
#     A.state_transition()

