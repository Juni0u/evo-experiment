import pygame, random
from markov_chain import MarkovChain
from typing import Optional
from global_vars import PLANT_COLOR, PLANT_SPAWN_RADIUS, FOOD_STANDARD_COLOR, RESOLUTION, SUN_ENERGY, FOOD_SPROUT_CHANCE
#TODO: As frutas que evoluem para plantas n:ao tem o thresold de energia porque nunca passando por create states with health

class Plant():
    def __init__(self,x:int,y:int,gene:list=[0], states=[0], brain=[0]) -> None:
        self.x = x
        self.y = y
        self.color = PLANT_COLOR      
        self.spawn_radius = PLANT_SPAWN_RADIUS
        self.age = 0
        self.state = "idle0" 

        if len(gene)==1: self.gene = self.generate_random_gene()
        else: self.gene = gene

        self.translation(self.gene)
        self.energy = self.energy_capacity

        if len(states)==1: 
            self.states = ["idle","eat","reproduce"]
            self.create_states_with_health(self.health_divisions)
        else: self.states = states
        
        if not isinstance(brain, MarkovChain): 
            self.brain = MarkovChain(states_list=self.states, probability_matrix=brain)
        else: self.brain = brain

    def translation(self, gene):
        # 0 , 1, 2, 3| 4, 5, 6, 7| 8, 9|10,11,12,13|14
        #[50,50,50,50|25,25,25,25|15,15| 5, 5, 5, 5|5]
        #0-3 = energy capacity
        #4-7 = food_spawn_thresold
        #8-9 = food_spawn_chance
        #10-13 = metabolism
        #14 = health divisions
        self.energy_capacity = sum(gene[0:4])
        self.metabolism = sum(gene[10:14]) + self.energy_capacity * 0.03
        self.food_spawn_thresold = sum(gene[4:8]) - self.metabolism * 0.5
        self.food_spawn_chance = sum(gene[8:10])/100 + self.metabolism/100 * 0.5
        self.health_divisions = int(gene[14] + self.metabolism * 0.15)

    def draw(self, canvas) -> None:
        canvas.set_at((int(self.x),int(self.y)), self.color) 
        for ix in range(-1,2):
            for iy in range(-1,2):
                canvas.set_at((int(self.x+ix),int(self.y+iy)), self.color) 

    def update(self,Plants,Fruits,canvas):
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
    
    def generate_random_gene(self):
        # 0 , 1, 2, 3| 4, 5, 6, 7| 8, 9|10,11,12,13|14
        #[50,50,50,50|25,25,25,25|15,15| 5, 5, 5, 5|5]
        #0-3 = energy capacity
        #4-7 = food_spawn_thresold
        #8-9 = food_spawn_chance
        #10-13 = metabolism
        #14 = health divisions
        gene=[]
        #energy capacity
        for i in range(0,4):
            gene.append(random.randint(1,50))
        #food_spawn_thresold
        for i in range(0,4):
            gene.append(random.randint(1,25))
        #food_spawn_chance
        for i in range(0,2):
            gene.append(random.randint(1,15))
        #metabolism + health divisions
        for i in range(0,5):
            gene.append(random.randint(1,5))
        #print(gene)
        return gene
    
    def state_transition(self):
        self.state = self.brain.state_transition(current_state=self.state)

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
        self.age += 1
    
    def spawnFood(self,canvas) -> Optional["Fruit"]:
        pos=[self.x+random.randint(-self.spawn_radius,self.spawn_radius),self.y+random.randint(-self.spawn_radius,self.spawn_radius)]
        if pos[0] > RESOLUTION[0]-1: pos[0] = RESOLUTION[0]-1
        elif pos[0] < 0: pos[0] = 0
        if pos[1] > RESOLUTION[1]-1: pos[1] = RESOLUTION[1]-1
        elif pos[1] < 0: pos[1] = 0
        
        if (self.energy > self.food_spawn_thresold) and (random.random() <= self.food_spawn_chance) and not (self.is_pixel_food(canvas,pos)):
            F = Fruit(x=pos[0],y=pos[1],gene=self.gene,states=self.states, brain=self.brain) 
            self.energy -= self.food_spawn_thresold*0.8
            return F
        return None
    
    def is_pixel_food(self,canvas,pos):
        pixel_color = canvas.get_at(pos)
        if pixel_color==FOOD_STANDARD_COLOR: return True
        else: return False

class Fruit():
    def __init__(self,x:int,y:int,gene:list, states:list, brain:"MarkovChain") -> None:
        self.x = x
        self.y = y
        self.color = FOOD_STANDARD_COLOR
        self.sprout_chance = FOOD_SPROUT_CHANCE
        self.gene = gene
        self.states = states
        self.brain = brain
        self.brain.mutate_matrix()
        self.translation(gene)
        self.rect = pygame.Rect(x,y,1,1)        

    def translation(self, gene):
        # 0 , 1, 2, 3| 4, 5, 6, 7| 8, 9|10,11,12,13|14
        #[50,50,50,50|25,25,25,25|15,15| 5, 5, 5, 5|5]
        #0-3 = energy capacity
        #4-7 = food_spawn_thresold
        #8-9 = food_spawn_chance
        #10-13 = metabolism
        #14 = health divisions
        self.energy_capacity = sum(gene[0:4])
        self.metabolism = sum(gene[10:14]) + self.energy_capacity * 0.03
        self.food_spawn_thresold = sum(gene[4:8]) - self.metabolism * 0.5
        self.food_spawn_chance = sum(gene[8:10])/100 + self.metabolism/100 * 0.5
        self.health_divisions = int(gene[14] + self.metabolism * 0.15)
        self.energy = self.energy_capacity

    def draw(self, canvas) -> None:
        canvas.set_at((int(self.x),int(self.y)), self.color) 

    def update(self, Plants, Fruits):
        if self.energy <= 0:
            self.die(Fruits)
        self.energy -= 1
        if random.random() < self.sprout_chance:
            self.sprout(Plants, Fruits)
        return Plants, Fruits

    def die(self, Fruits):
        Fruits.remove(self)
        return Fruits

    def sprout(self, Plants, Fruits):
        if self in Fruits:
            Plants.append(Plant(x=self.x, y=self.y, gene=self.gene, states=self.states, brain=self.brain))
            Fruits.remove(self)
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

