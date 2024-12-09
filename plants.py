
import pygame, math, random as rd, uuid
from config import Parameters
from markov_chain import Brain
from typing import Optional
# from grid import Grid
#TODO: As frutas que evoluem para plantas n:ao tem o thresold de energia porque nunca passando por create states with health

class Plant():
    def __init__(self,x:int,y:int, gene=[0])-> None: #health_divisions:int=0, states=[0], brain=[0]) -> None:
        """(x,y) -> Position
        gene -> [energy_capacity,metabolism,food_spawn_thresold,self.brain]
        if gene = [0] -> standard atributes with a random brain"""
        self.parameter = Parameters()
        self.id = f"plant-{uuid.uuid4()}"
        self.x = x
        self.y = y
        self.color = self.parameter.plant.base_color      
        self.spawn_radius = self.parameter.plant.spawn_radius 
        self.death_prob = 0
        self.gene = gene
        self.rect = pygame.Rect(self.x,self.y,1,1)

        self.age = 0
        self.state = self.parameter.plant.states[0]
        self.translation(self.gene)
        
    def __hash__(self) -> int:
        return hash(self.id)
    
    def __eq__(self, value: "Plant") -> bool:
        return (self.id==value.id)

    def draw(self, canvas) -> None:
        canvas.set_at((int(self.x),int(self.y)), self.color) 
        return canvas

    def update(self, simulation):
        self.age += 1
        self.update_death_prob()
        self.state_transition() # <- brain state and zone are updated in here
        if (self.energy <= 0) or (rd.random() < self.death_prob):
            simulation.remove_plant(self.x,self.y)
            # if self.energy > 0:
            #     print(f"Age: {self.age}, Prob: {self.death_prob}")
            return simulation
        self.metabolize()
        if "eat" in self.brain.current_brain_state:
            self.eat(simulation)
        elif "reproduce" in self.brain.current_brain_state:
            simulation = self.spawnFood(simulation)
        return simulation

    def translation(self, gene):
        ##[self.energy_capacity,self.metabolism,self.food_spawn_thresold,self.brain]
        ##[         0          ,         1     ,           2            ,     3    ] 
        #self.translation(self.gene)
        if len(gene) == 1: 
            gene = [self.parameter.plant.standard_energy_capacity,
                    self.parameter.plant.standard_metabolism,
                    self.parameter.plant.standard_food_spawn_energy_thresold,
                    0]            
    
        self.energy_capacity = gene[0]
        self.metabolism = gene[1]
        self.food_spawn_thresold = gene[2]
        self.brain = gene[3]
        self.energy = self.energy_capacity

        if not isinstance(self.brain, Brain): 
            brain_zone = gene[3]
            if self.brain==0: 
                brain_zone = rd.randint(self.parameter.plant.brain_size_interval[0],self.parameter.plant.brain_size_interval[1])
            self.brain = Brain(mutation_probability=self.parameter.plant.mutation_prob,
                                               mutation_interval=self.parameter.plant.mutation_interval,
                                               states=self.parameter.plant.states,
                                               transition_zones=brain_zone)
        else: #if a brain was
            self.brain = self.brain   

        self.assign_brain_zone_to_energy_level()
        self.updates_brain_zone()
        #self.color = self.parameter.plant.colors[self.brain.transition_grid.shape[0]-1]
        self.gene = [self.energy_capacity,self.metabolism,self.food_spawn_thresold,self.brain]        

    def update_death_prob(self) -> None:
        "Updates death probability."
        # MAX AGE = MAX SIMULATION STEPS (MAX PROBABILITY OF DEATH)
        if self.death_prob < self.parameter.plant.max_death_prob:
            cons = 1
            unit_increment = (self.parameter.plant.max_death_prob/self.parameter.plant.age_max_death_prob)
            self.death_prob += unit_increment*rd.random()

    def state_transition(self) -> None:
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

    def eat(self, simulation) -> None:
        if simulation.grid[self.x][self.y]["env"]:
            pick_env = rd.choice(list(simulation.grid[self.x][self.y]["env"]))
            to_eat = pick_env.food_available
        else:
            to_eat = simulation.environment.standart_energy
        self.energy += to_eat

    def metabolize(self) -> None:
        self.energy -= self.metabolism
    
    def spawnFood(self,simulation):
        pos=[self.x+rd.randint(-self.spawn_radius,self.spawn_radius),self.y+rd.randint(-self.spawn_radius,self.spawn_radius)]
        if pos[0] > self.parameter.resolution[0]-1: pos[0] = self.parameter.resolution[0]-1
        elif pos[0] < 0: pos[0] = 0
        if pos[1] > self.parameter.resolution[1]-1: pos[1] = self.parameter.resolution[1]-1
        elif pos[1] < 0: pos[1] = 0
        
        if (self.energy > self.food_spawn_thresold):
            if "fruit" in simulation.grid[pos[0]][pos[1]]:
                simulation.remove_fruit(x=pos[0],y=pos[1])
            simulation.add_fruit(x=pos[0],y=pos[1],gene=self.gene)
            self.energy -= self.food_spawn_thresold
        return simulation

class Fruit():
    def __init__(self,x:int,y:int,gene:list) -> None:
        self.parameter = Parameters()
        self.x = x
        self.y = y
        self.id = f"fruit-{uuid.uuid4()}"
        self.color = self.parameter.plant.food_standard_color
        self.sprout_chance = self.parameter.plant.food_sprout_chance
        self.gene = gene 
        ##[self.energy_capacity,self.metabolism,self.food_spawn_thresold,self.food_spawn_chance,self.health_divisions,self.states,self.brain]
        ##[         0          ,         1     ,           2            ,         3            ,          4          ,     5     ,     6    ] 
        self.energy = self.gene[2]
        self.rect = pygame.Rect(x,y,1,1) 

    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, value: "Plant") -> bool:
        return (self.id==value.id)       

    def draw(self, canvas) -> None:
        canvas.set_at((int(self.x),int(self.y)), self.color) 
        return canvas

    def update(self, simulation):
        self.energy -= 1
        if self.energy <= 0:
            simulation.remove_fruit(x=self.x,y=self.y)
            return simulation
        if rd.random() < self.sprout_chance:
            simulation = self.sprout(simulation)
        return simulation

    def die(self, Fruits):
        Fruits.remove(self)
        return Fruits

    def sprout(self, simulation):
        for zone in range(self.gene[3].transition_grid.shape[0]-1):
            self.gene[3].mutate(zone)
        simulation.add_plant(x=self.x, y=self.y, gene=self.gene)
        return simulation

def main():
    A = Plant(0,0)


if __name__ == "__main__":
    main()

