import pygame, math, random as rd
from config import Parameters
from markov_chain import Brain
from typing import Optional
#TODO: As frutas que evoluem para plantas n:ao tem o thresold de energia porque nunca passando por create states with health

class Plant():
    def __init__(self,x:int,y:int, gene=[0])-> None: #health_divisions:int=0, states=[0], brain=[0]) -> None:
        """(x,y) -> Position
        gene -> [energy_capacity,metabolism,food_spawn_thresold,self.brain]
        if gene = [0] -> standard atributes with a random brain"""
        self.parameter = Parameters()
        self.x = x
        self.y = y
        self.color = self.parameter.plant.base_color      
        self.spawn_radius = self.parameter.plant.spawn_radius 
        self.death_prob = 0
        self.gene = gene
        self.rect = pygame.Rect(self.x-1,self.y-1,2,2)

        self.age = 0
        self.state = self.parameter.plant.states[0]
        self.translation(self.gene)
        
    def draw(self, canvas) -> None:
        canvas.set_at((int(self.x),int(self.y)), self.color) 
        for ix in range(-1,2):
            for iy in range(-1,2):
                canvas.set_at((int(self.x+ix),int(self.y+iy)), self.color) 
        return canvas

    def update(self,Environment,Plants,Fruits,canvas):
        self.age += 1
        self.update_death_prob()
        self.metabolize()
        self.state_transition() # <- brain state and zone are updated in here
        if (self.energy <= 0) or (rd.random() < self.death_prob):
            Plants.remove(self)
            return Plants, Fruits
        if "eat" in self.state:
            self.eat(Environment)
        elif "reproduce" in self.state:
            F = self.spawnFood(canvas)
            if F: Fruits.append(F)
        return Plants, Fruits

    def translation(self, gene):
        ##[self.energy_capacity,self.metabolism,self.food_spawn_thresold,self.brain]
        ##[         0          ,         1     ,           2            ,     3    ] 
        #self.translation(self.gene)
        if len(gene) == 1: 
            gene = [self.parameter.plant.standard_energy_capacity,
                    self.parameter.plant.standard_metabolism,
                    self.parameter.plant.standard_food_spawn_energy_thresold,
                    [0]]            
    
        self.energy_capacity = gene[0]
        self.metabolism = gene[1]
        self.food_spawn_thresold = gene[2]
        self.brain = gene[3]
        self.energy = self.energy_capacity

        if not isinstance(self.brain, Brain): 
            self.brain = Brain(mutation_probability=self.parameter.plant.mutation_prob,
                                               mutation_interval=self.parameter.plant.mutation_interval,
                                               states=self.parameter.plant.states,
                                               transition_zones=rd.randint(1,7))
        else: #if a brain was
            self.brain = self.brain   

        self.assign_brain_zone_to_energy_level()
        self.updates_brain_zone()
        self.gene = [self.energy_capacity,self.metabolism,self.food_spawn_thresold,self.brain]        

    def update_death_prob(self):
        "Updates death probability."
        cons = 0.15
        unit_increment = (self.parameter.plant.max_death_prob/self.parameter.plant.age_max_death_prob)
        self.death_prob += unit_increment*cons

    def state_transition(self):
        "Transitions state"
        self.updates_brain_zone()
        self.brain.state_transition()

    def assign_brain_zone_to_energy_level(self) -> None:
        """Sets Energy Thresolds that determine which brainzone will be used."""
        zone_number = self.brain.transition_grid.shape[0]
        each_zone = 100 / zone_number
        zone_limits = []
        zone_initial_value=0
        zone_final_value=each_zone
        for _ in range(zone_number):
            zone_limits.append((zone_initial_value,zone_final_value))
            zone_initial_value=zone_final_value
            zone_final_value+=each_zone
        self.brain_zones_intervals = zone_limits

    def updates_brain_zone(self) -> None:
        """Identifies which brain zone should be used depending on energy level"""
        for i,(min,max) in enumerate(self.brain_zones_intervals):
            if (self.energy > min) and (self.energy <= max): #zero doesnt matter, cause it dies
                self.brain.current_brain_zone = i
                break

    def eat(self, environment) -> None:
        self.energy += environment.energy_given(self.rect)

    def metabolize(self) -> None:
        self.energy -= self.metabolism
    
    def spawnFood(self,canvas) -> Optional["Fruit"]:
        pos=[self.x+rd.randint(-self.spawn_radius,self.spawn_radius),self.y+rd.randint(-self.spawn_radius,self.spawn_radius)]
        if pos[0] > self.parameter.resolution[0]-1: pos[0] = self.parameter.resolution[0]-1
        elif pos[0] < 0: pos[0] = 0
        if pos[1] > self.parameter.resolution[1]-1: pos[1] = self.parameter.resolution[1]-1
        elif pos[1] < 0: pos[1] = 0
        
        if (self.energy > self.food_spawn_thresold) and not (self.is_pixel_food(canvas,pos)):
            F = Fruit(x=pos[0],y=pos[1],gene=self.gene) 
            self.energy -= self.food_spawn_thresold
            return F
        return None
    
    def is_pixel_food(self,canvas,pos):
        pixel_color = canvas.get_at(pos)
        if pixel_color== self.parameter.plant.food_standard_color: return True
        else: return False

class Fruit():
    def __init__(self,x:int,y:int,gene:list) -> None:
        self.parameter = Parameters()
        self.x = x
        self.y = y
        self.color = self.parameter.plant.food_standard_color
        self.sprout_chance = self.parameter.plant.food_sprout_chance
        self.gene = gene 
        ##[self.energy_capacity,self.metabolism,self.food_spawn_thresold,self.food_spawn_chance,self.health_divisions,self.states,self.brain]
        ##[         0          ,         1     ,           2            ,         3            ,          4          ,     5     ,     6    ] 
        self.energy = self.gene[2]
        self.rect = pygame.Rect(x,y,1,1)        

    def draw(self, canvas) -> None:
        canvas.set_at((int(self.x),int(self.y)), self.color) 
        return canvas

    def update(self, Plants, Fruits):
        if self.energy <= 0:
            Fruits = self.die(Fruits)
            return Plants, Fruits
        self.energy -= 1
        if rd.random() < self.sprout_chance:
            Plants, Fruits = self.sprout(Plants, Fruits)
        return Plants, Fruits

    def die(self, Fruits):
        Fruits.remove(self)
        return Fruits

    def sprout(self, Plants, Fruits):
        if self in Fruits:
            for zone in self.gene[3].transition_grid.shape[0]:
                self.gene[3].mutate(zone)
            Plants.append(Plant(x=self.x, y=self.y, gene=self.gene))
            Fruits.remove(self)
            return Plants, Fruits
        return Plants, Fruits

def main():
    A = Plant(0,0)
    
    energia = [10,20,30,40,50,60,70,80,90,100]
    print(A.brain.transition_grid)
    for nivel in energia:
        A.state_transition()
        print(f"brain state = {A.brain.current_brain_state}, brain zone = {A.brain.current_brain_zone+1}({len(A.brain_zones_intervals)})")
        print(A.energy)
        A.energy = nivel
        print(A.brain.transition_grid[A.brain.current_brain_zone,:,:])
        print()

if __name__ == "__main__":
    main()

