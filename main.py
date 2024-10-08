import pygame, uuid, random, time
from creature import Creature
from food import FoodSpawner, Food
from global_vars import RESOLUTION

seed = int(time.time() * 777)

pygame.init() 

resolution = RESOLUTION
screen_size = (640,640)

# CREATING CANVAS 
canvas = pygame.Surface(resolution)
screen = pygame.display.set_mode(screen_size)

# TITLE OF CANVAS 
pygame.display.set_caption("My Board") 
exit = False

class Game():
    def __init__(self,canvas):
        self.year = 0
        self.seed = seed
        random.seed(self.seed)
        self.canvas = canvas
        self.AgentList = []
        self.FoodSpawnerList = []
        self.FoodList = []        
        # #top-left
        self.add_food_spawner(x=25,y=25,capacity=100,spawn_radius=25,food_max_energy=5,food_spawn_chance=0.01,rest_time=50)
        # #top-right
        self.add_food_spawner(x=128-25,y=25,capacity=100,spawn_radius=25,food_max_energy=5,food_spawn_chance=0.02,rest_time=50)
        # #botton-left
        self.add_food_spawner(x=25,y=128-25,capacity=100,spawn_radius=25,food_max_energy=5,food_spawn_chance=0.03,rest_time=50)
        # #botton-right
        self.add_food_spawner(x=128-25,y=128-25,capacity=100,spawn_radius=25,food_max_energy=5,food_spawn_chance=0.04,rest_time=50)
        # #middle
        self.add_food_spawner(x=63,y=63,capacity=100,spawn_radius=25,food_max_energy=5,food_spawn_chance=0.05,rest_time=50)

    def update(self):
        self.year += 1
        random.shuffle(self.AgentList)
        if self.year == 1000: self.create_agent_population(15)
            
        for agent in self.AgentList:          
            self.FoodList, self.AgentList = agent.update(year=self.year,seed=self.seed,FoodList=self.FoodList, AgentList=self.AgentList)            
            
        for foodspawner in self.FoodSpawnerList:
            self.FoodList = foodspawner.update(self.FoodList, self.canvas)

    def draw(self):
        for foodspawner in self.FoodSpawnerList:
            foodspawner.draw(canvas)
        
        for agent in self.AgentList:
            agent.draw(canvas)
            
        for food in self.FoodList:
            food.draw(canvas)
            
    def add_agent(self,x:int,y:int,color:tuple,born_in:int,chromosome:str):
        id = uuid.uuid4()
        self.AgentList.append(Creature(id,x,y,color,born_in,chromosome))

    def add_food_spawner(self,x:int,y:int,capacity:int,spawn_radius:int,food_max_energy:int,food_spawn_chance:float,rest_time:int):
        self.FoodSpawnerList.append(FoodSpawner(x,y,capacity,spawn_radius,food_max_energy, food_spawn_chance,rest_time))

    def create_agent_population(self,quantity):
        for i in range(quantity):
            chromosome = ""
            for _ in range(17): #chromosome lenght
                chromosome += str(random.choice([0,1]))

            self.add_agent(
                x=random.randint(0,127),
                y=random.randint(0,127),
                color=(255,0,0),
                born_in=self.year,
                chromosome=chromosome
                )

def main():
    game = Game(canvas)
    global exit
    while not exit: 
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                exit = True
    #############################################
        canvas.fill((0, 0, 0)) 
        game.update()
        game.draw()

    #############################################        
        scaled_canvas = pygame.transform.scale(canvas, screen_size)
        screen.blit(scaled_canvas, (0, 0))  # Draw scaled canvas on the screen
        pygame.display.update() 
    pygame.quit()

main()