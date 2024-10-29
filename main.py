import pygame, uuid, random, time
from creature import Creature
from plants import Plant, Fruit
from global_vars import RESOLUTION
import statistics
import datetime

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
        self.PlantsList = []
        self.FruitList = []        
        
        self.create_plant_population(100)

    def update(self):
        self.year += 1
        random.shuffle(self.AgentList)
        random.shuffle(self.PlantsList)
        if (self.year%5==0) and (len(self.PlantsList)<10):
            self.create_plant_population(3)

        for plant in self.PlantsList:
            self.PlantsList, self.FruitList = plant.update(self.PlantsList,self.FruitList, self.canvas)
        
        for fruit in self.FruitList:
            self.PlantsList, self.FruitList = fruit.update(self.PlantsList, self.FruitList)

        if len(self.PlantsList) > 0:
            print(f"Number of plants: {len(self.PlantsList)}")

    def draw(self):
        for plant in self.PlantsList:
            plant.draw(canvas)
            
        for fruit in self.FruitList:
            fruit.draw(canvas)
            
    def add_agent(self,x:int,y:int,color:tuple,born_in:int,chromosome:str):
        id = uuid.uuid4()
        self.AgentList.append(Creature(id,x,y,color,born_in,chromosome))

    def add_plant(self,x:int,y:int,gene:list=[0]):
        self.PlantsList.append(Plant(x,y))

    def create_plant_population(self, quantity):
        for i in range(quantity):
            self.add_plant(x=random.randint(0,125),y=random.randint(0,125))

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

    def print_population(self):
        currentime = datetime.datetime.now()
        currentime = currentime.strftime(f"%Y-%m-%d_%H-%M-%S")
        file_name = f"Results/{currentime}__{self.year}.txt"
        with open(file_name, "w") as file:
            for creature in self.AgentList:
                file.write(str(creature))

    def get_data(self):
        output = f"Data of year {self.year}\n"
        max_steps = [creature.max_steps for creature in self.AgentList]
        vision_radius = [creature.vision_radius for creature in self.AgentList]
        reprodution_thresold = [creature.reprodution_thresold for creature in self.AgentList]
        output += f"[MAX_STEPS]  Median:{round(statistics.median(max_steps),2)}, Mean:{round(statistics.mean(max_steps),2)}, Std.Dev:{round(statistics.stdev(max_steps),2)}\n"
        output += f"[VISION RADIUS]  Median:{round(statistics.median(vision_radius),2)}, Mean:{round(statistics.mean(vision_radius),2)}, Std.Dev:{round(statistics.stdev(vision_radius),2)}\n"
        output += f"[REPRODUCTION THRSOLD]  Median:{round(statistics.median(reprodution_thresold),2)}, Mean:{round(statistics.mean(reprodution_thresold),2)}, Std.Dev:{round(statistics.stdev(reprodution_thresold),2)}\n"
                
        currentime = datetime.datetime.now()
        currentime = currentime.strftime(f"%Y-%m-%d_%H-%M-%S")
        file_name = f"Results/Population_Data_{self.year}_{currentime}.txt"
        with open(file_name, "w") as file:
            file.write(output)
        
def main(steps:int):
    steps += 1000
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
        steps -= 1
        # if game.year == 1100: 
        #     game.print_population()
        #     game.get_data()
        # if game.year == 1600: 
        #     game.print_population()
        #     game.get_data()
        # if game.year == 2000: 
        #     game.print_population()
        #     game.get_data()
        # if game.year == 2500: 
        #     game.print_population()
        #     game.get_data()
        # if game.year == 2900: 
        #     game.print_population()
        #     game.get_data()
        if steps < 1:
            game.print_population()
            game.get_data()
            exit = True
    pygame.quit()

main(10000)