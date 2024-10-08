import pygame, uuid, random, time
from creature import Creature
from food import FoodSpawner, Food

seed = int(time.time() * 777)

pygame.init() 

resolution = (128,128)
screen_size = (640,640)

# CREATING CANVAS 
canvas = pygame.Surface(resolution)
screen = pygame.display.set_mode(screen_size)

# TITLE OF CANVAS 
pygame.display.set_caption("My Board") 
exit = False

class Game():
    def __init__(self,canvas):
        self.seed = seed
        random.seed(self.seed)
        self.canvas = canvas
        self.Agents = []
        self.FoodSpawners = []
        self.Foods = []
        self.add_agent(64,64,(255,0,0),0,"01010001010101010101010")
        self.add_agent(64,34,(255,255,0),0,"01010001010101010101010")
        self.add_agent(64,94,(255,0,255),0,"01010001010101010101010")
        self.add_agent(34,64,(125,125,125),0,"01010001010101010101010")
        self.add_agent(94,64,(0,0,255),0,"01010001010101010101010")
        self.add_food_spawner(x=50,y=50,capacity=10,spawn_radius=15,food_max_energy=10,food_spawn_chance=0.2)
        #self.create_agent_population(20)

    def update(self):
        for agent in self.Agents:
            agent.update(seed=self.seed)

        for foodspawner in self.FoodSpawners:
            self.Foods = foodspawner.update(self.Foods)
            if foodspawner.capacity < 1:
                self.FoodSpawners.remove(foodspawner)

    def draw(self):
        for food in self.Foods:
            food.draw(canvas)

        for foodspawner in self.FoodSpawners:
            foodspawner.draw(canvas)

        for agent in self.Agents:
            agent.draw(canvas)
        
    def add_agent(self,x:int,y:int,color:tuple,born_in:int,chromosome:str):
        id = uuid.uuid4()
        self.Agents.append(Creature(id,x,y,color,born_in,chromosome))

    def add_food_spawner(self,x:int,y:int,capacity:int,spawn_radius:int,food_max_energy:int,food_spawn_chance:float):
        self.FoodSpawners.append(FoodSpawner(x,y,capacity,spawn_radius,food_max_energy, food_spawn_chance))

    def create_agent_population(self,quantity):
        for i in range(quantity):
            chromosome = ""
            for _ in range(23): #chromosome lenght
                chromosome += str(random.choice([0,1]))

            self.add_agent(
                x=random.randint(0,127),
                y=random.randint(0,127),
                color=(255,0,0),
                born_in=0,
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