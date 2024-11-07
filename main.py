from config import Parameters
from tqdm import tqdm
from plants import Plant, Fruit
from environment import Environment
import pygame, time, datetime, os, random as rd

class EvoSim():
    def __init__(self) -> None:
        self.config_initialization()
        self.var_initialization()

    def update(self,events):
        self.check_if_QUIT(events)
        rd.shuffle(self.PlantsList)
        rd.shuffle(self.FruitList)
        self.step += 1
        if len(self.PlantsList)==0: print(f"{self.step} WHOA")

        for plant in self.PlantsList:
            self.PlantsList, self.FruitList = plant.update(self.env, self.PlantsList,self.FruitList, self.canvas)

        for fruit in self.FruitList:
            self.PlantsList, self.FruitList = fruit.update(self.PlantsList, self.FruitList)

    def before_draw(self):
        self.canvas.fill((0, 0, 0)) 

    def draw(self):

        if len(self.PlantsList) < 3: self.create_plant_population(50)
        
        for fruit in self.FruitList:
            self.canvas = fruit.draw(self.canvas)

        for plant in self.PlantsList:
            self.canvas = plant.draw(self.canvas)

        font = pygame.font.Font(None,16)
        step_text = font.render(f"{self.step}",True, (255,0,255))
        self.canvas.blit(step_text,(5,5))

    def update_screen(self):
        # scaled_canvas = pygame.transform.scale(self.canvas, self.parameter.screen_size)
        scaled_canvas = pygame.transform.scale(self.canvas, self.parameter.screen_size)
        self.screen.blit(scaled_canvas, (0, 0))  # Draw scaled canvas on the screen
        pygame.display.update() 

    def start_game(self,max_steps:int=1000, render:bool=False, save_video:bool=True) -> None:
        self.create_experiment_folder()
        self.create_plant_population(50)

        with tqdm(total=max_steps, desc="Progress", ncols=100) as progress_bar:
            while (not self.exit) and (self.step!=max_steps) and (len(self.PlantsList)>0):
                events = pygame.event.get()
                self.update(events)
                self.before_draw()
                self.draw()
                self.update_screen()
                if save_video: self.save_frame()
                progress_bar.update(1)
        pygame.quit()

    def initialize_environments(self):
        self.env.create_new_region(0,0,int(self.parameter.resolution[0]/2),int(self.parameter.resolution[1]/2), self.parameter.sun_energy*1.25)
        self.env.create_new_region(int(self.parameter.resolution[0]/2),0,int(self.parameter.resolution[0]/2),int(self.parameter.resolution[1]/2), self.parameter.sun_energy*0.5)
        self.env.create_new_region(int(self.parameter.resolution[0]/2),int(self.parameter.resolution[1]/2),int(self.parameter.resolution[0]/2),int(self.parameter.resolution[1]/2), self.parameter.sun_energy*0.25)

    def add_plant(self,x:int,y:int,gene:list=[0]):
        self.PlantsList.append(Plant(x,y,gene))

    def create_plant_population(self, quantity):
        for i in range(quantity):
            self.add_plant(x=rd.randint(0,self.parameter.resolution[0]-5),y=rd.randint(0,self.parameter.resolution[1]-5))        

    def save_frame(self):
        frame = pygame.surfarray.array3d(self.canvas)
        frame = frame.transpose([1,0,2])
        self.frames.append(frame)

    def get_configurations(self) -> str:
        output = f"""
        Configuration Variables
            - seed: {self.seed}
            - render: {self.render}
            - number of steps: {self.step}
            - simulation duration: [tempo]
        """
        return output

    def var_initialization(self,render:bool=False) -> None:
        self.AgentList = []
        self.PlantsList = []
        self.FruitList = []     
        self.frames = []
        self.env = Environment()
        self.exit = False
        self.render = False
        self.step = 0

    def config_initialization(self) -> None:
        pygame.init()
        pygame.font.init()
        self.parameter = Parameters()
        self.seed = int(time.time() * 777)
        self.screen = pygame.display.set_mode(tuple(self.parameter.screen_size))
        self.canvas = pygame.Surface(tuple(self.parameter.resolution))#self.parameter.resolution)
        self.clock = pygame.time.Clock()

    def check_if_QUIT(self, events) -> None:
        for event in events:
            if event.type == pygame.QUIT: 
                self.exit=True

    def create_experiment_folder(self, address:str=""):
        if address != "": self.parameter.experiment_folder = address
        currentime = datetime.datetime.now()
        currentime = currentime.strftime(f"%Y-%m-%d_%H-%M-%S")
        new_folder = f"{self.parameter.experiment_folder}/Experiment {currentime}"
        os.makedirs(new_folder)

def main(max_steps,render,save_video):
    sim = EvoSim()
    sim.start_game(max_steps, render, save_video)

if __name__ == "__main__":
    main(max_steps=10000, render=True, save_video=True)