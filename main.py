import pygame, uuid, random, time
from creature import Creature
from plants import Plant, Fruit
from global_vars import RESOLUTION
from tqdm import tqdm
import statistics, datetime, os, numpy, imageio
import cProfile

seed = int(time.time() * 777)

pygame.init() 

resolution = RESOLUTION
screen_size = (640,640)

# CREATING CANVAS 
canvas = pygame.Surface(resolution)
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()


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
        
        self.create_plant_population(50)

    def update(self):
        self.year += 1
        random.shuffle(self.AgentList)
        random.shuffle(self.PlantsList)
        if (self.year%10==0):
            self.create_plant_population(1)

        for plant in self.PlantsList:
            self.PlantsList, self.FruitList = plant.update(self.PlantsList,self.FruitList, self.canvas)
        
        for fruit in self.FruitList:
            self.PlantsList, self.FruitList = fruit.update(self.PlantsList, self.FruitList)

    def draw(self):
        for plant in self.PlantsList:
            plant.draw(canvas)
            
        for fruit in self.FruitList:
            fruit.draw(canvas)
            
    def add_agent(self,x:int,y:int,color:tuple,born_in:int,chromosome:str):
        id = uuid.uuid4()
        self.AgentList.append(Creature(id,x,y,color,born_in,chromosome))

    def add_plant(self,x:int,y:int,gene:list=[0]):
        self.PlantsList.append(Plant(x,y,gene))

    def create_plant_population(self, quantity):
        for i in range(quantity):
            self.add_plant(x=random.randint(0,RESOLUTION[0]-5),y=random.randint(0,RESOLUTION[1]-5))

    def create_agent_population(self,quantity):
        for i in range(quantity):
            chromosome = ""
            for _ in range(17): #chromosome lenght
                chromosome += str(random.choice([0,1]))

            self.add_agent(
                x=random.randint(0,RESOLUTION[0]),
                y=random.randint(0,RESOLUTION[1]),
                color=(255,0,0),
                born_in=self.year,
                chromosome=chromosome
                )

    def print_plant_data(self, experiment_folder):
        file_name = f"{experiment_folder}/PlantsTatistics.txt"
        brain_size = [len(plant.states) for plant in self.PlantsList]
        age = [plant.age for plant in self.PlantsList]
        green_shade = [plant.color[1] for plant in self.PlantsList]
        output = f"[{self.year}]------------------------------------------------------------------------------------------------------------------"
        output += f"\n     BRAIN -> Median:{round(statistics.median(brain_size),2)}, Mean:{round(statistics.mean(brain_size),2)}, Std.Dev:{round(statistics.stdev(brain_size),2)}"
        output += f"\n     AGE   -> Median:{round(statistics.median(age),2)}, Mean:{round(statistics.mean(age),2)}, Std.Dev:{round(statistics.stdev(age),2)}\n"
        output += f"\n     COLOR -> Median:{round(statistics.median(green_shade),0)}, Mean:{round(statistics.mean(green_shade),0)}, Std.Dev:{round(statistics.stdev(green_shade),0)}\n"

        with open(file_name, "a") as file:
            file.write(output)

    def print_plants_brain(self, experiment_folder):
        file_name = f"{experiment_folder}/Top10Oldest.txt"
        top_10_oldest = sorted(self.PlantsList, key=lambda plant: plant.age, reverse=True)[:10]
        with open(file_name, "a") as file:
            file.write(f"YEAR {self.year} -------------------------------------------------------\n")
            for plant in top_10_oldest:
                file.write("\n")
                file.write(f"{plant.age}, {plant.states}\n")
                numpy.savetxt(file, plant.brain.probability_matrix, fmt='%.2f', delimiter=' ')
            

def main(steps:int, render: bool=True):
    frames = []
    currentime = datetime.datetime.now()
    currentime = currentime.strftime(f"%Y-%m-%d_%H-%M-%S")
    experiment_folder = f"Results/Experiment {currentime}"
    os.makedirs(experiment_folder)

    game = Game(canvas)
    global exit
    with tqdm(total=steps, desc="Progress", ncols=100) as progress_bar:
        while not exit: 
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    exit = True
        #############################################
            canvas.fill((0, 0, 0)) 
            game.update()
            game.draw()
            game.print_plant_data(experiment_folder)
            game.print_plants_brain(experiment_folder)
            steps -= 1
        #############################################
            if render:        
                scaled_canvas = pygame.transform.scale(canvas, screen_size)
                screen.blit(scaled_canvas, (0, 0))  # Draw scaled canvas on the screen
                pygame.display.update() 
        #############################################
            frame = pygame.surfarray.array3d(canvas)
            frame = frame.transpose([1, 0, 2])
            frames.append(frame)
            #clock.tick(30)
        #############################################
            if steps < 1:
                exit = True
            progress_bar.update(1)
    imageio.mimsave(f'{experiment_folder}/recording.mp4', frames)
    pygame.quit()

if __name__ == "__main__":
    main(steps=1500,render=False)
    #cProfile.run("main(steps=1000,render=False)")