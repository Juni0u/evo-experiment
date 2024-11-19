from config import Parameters
from tqdm import tqdm
# from plants import Plant, Fruit
from grid import Grid
from environment import Environment
import pygame, time, datetime, os, imageio, random as rd, numpy as np

class EvoSim():
    def __init__(self) -> None:
        self.config_initialization()
        self.pygame_config_initialization()
        self.var_initialization()

    def update(self,events, save_video):
        self.check_if_QUIT(events, save_video)
        self.step += 1
        # if self.step%100:
        #     self.create_plant_population(1) 

        shuffled_plants = list(self.simulation.plants_occupy)
        shuffled_fruits = list(self.simulation.fruits_occupy)
        rd.shuffle(shuffled_plants)
        rd.shuffle(shuffled_fruits)

        for x,y in shuffled_plants:
            self.simulation = self.simulation.grid[x][y]["plant"].update(self.simulation)

        for x,y in shuffled_fruits:
            self.simulation = self.simulation.grid[x][y]["fruit"].update(self.simulation)

       # self.simulation.save_grid_state(address=self.grid_folder,step=self.step)

    def before_draw(self):
        self.canvas.fill((0, 0, 0)) 

    def draw(self):        
            self.before_draw()

            for x,y in self.simulation.fruits_occupy:
                self.canvas = self.simulation.grid[x][y]["fruit"].draw(self.canvas)

            for x,y in self.simulation.plants_occupy:
                self.canvas = self.simulation.grid[x][y]["plant"].draw(self.canvas)

            font = pygame.font.Font(None,16)
            step_text = font.render(f"{self.step}",True, (255,0,255))
            n_plants = font.render(f"{len(self.simulation.plants_occupy)}", True, (255,0,255))
            n_fruits = font.render(f"{len(self.simulation.fruits_occupy)}", True, (255,0,255))

            self.canvas.blit(step_text,(5,5))
            self.canvas.blit(n_plants,(5,25))
            self.canvas.blit(n_fruits,(5,45))



    def update_screen(self,scaled_canvas):
        self.screen.blit(scaled_canvas, (0, 0))  # Draw scaled canvas on the screen
        pygame.display.update() 

    def start_game(self,max_steps:int=1000, render:bool=False, save_video:bool=True) -> None:
        self.create_experiment_folder()
        self.initialize_environments()
        #self.create_plant_population(150)
        # self.create_population_per_environment(50)
        self.create_population_per_environment_per_brain_zone(50)

        with tqdm(total=max_steps, desc="Progress", ncols=100) as progress_bar:
            while (not self.exit) and (self.step!=max_steps):
                events = pygame.event.get()
                self.update(events, save_video)
                # self.before_draw()
                if render or save_video: 
                    self.draw()
                    scaled_canvas = pygame.transform.scale(self.canvas, self.parameter.screen_size)
                if render: self.update_screen(scaled_canvas)
                if save_video: self.save_frame(scaled_canvas)
                # if self.step%500: self.get_plants_brains()
                progress_bar.update(1)
        if save_video: imageio.mimsave(f'{self.parameter.experiment_folder}/recording.mp4', self.frames)
        pygame.quit()

    def initialize_environments(self):
        #up-left = 1.25*normal-food
        self.simulation.add_rectangle_region(0,0,int(self.parameter.resolution[0]/2),int(self.parameter.resolution[1]/2), self.parameter.sun_energy*1.25)
        #up-right = 0.75*normal-food
        self.simulation.add_rectangle_region(int(self.parameter.resolution[0]/2),0,int(self.parameter.resolution[0]/2),int(self.parameter.resolution[1]/2), self.parameter.sun_energy*0.75)
        #down-righ = 0.5*normal-food
        self.simulation.add_rectangle_region(int(self.parameter.resolution[0]/2),int(self.parameter.resolution[1]/2),int(self.parameter.resolution[0]/2),int(self.parameter.resolution[1]/2), self.parameter.sun_energy*0.5)

    def create_population_per_environment_per_brain_zone(self, qty_per_brain_zone_per_environment):
        for region in self.simulation.environment.regions:
            for _ in range(qty_per_brain_zone_per_environment):
                for i in range(self.parameter.plant.brain_size_interval[0],self.parameter.plant.brain_size_interval[1]):
                    self.simulation.add_plant(x=rd.randint(region.x+5,region.x+region.w-5),y=rd.randint(region.y+5,region.y+region.h-5),gene=[i])

    def create_population_per_environment(self,quantity_per_environment):
        for region in self.simulation.environment.regions:
            for _ in range(quantity_per_environment):
                self.simulation.add_plant(x=rd.randint(region.x+5,region.x+region.w-5),y=rd.randint(region.y+5,region.y+region.h-5))

    def create_plant_population(self, quantity):
        for _ in range(quantity):
            self.simulation.add_plant(x=rd.randint(0,self.parameter.resolution[0]-5),y=rd.randint(0,self.parameter.resolution[1]-5))        

    def save_frame(self,scaled_canvas):
        frame = pygame.surfarray.array3d(scaled_canvas)
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
        # self.AgentList = []
        # self.PlantsList = []
        # self.FruitList = []     
        self.frames = []
        self.env = Environment()
        self.exit = False
        self.render = False
        self.step = 0
        self.simulation = Grid(x_size=self.parameter.resolution[0],y_size=self.parameter.resolution[1])

    def pygame_config_initialization(self) -> None:
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(tuple(self.parameter.screen_size))
        self.canvas = pygame.Surface(tuple(self.parameter.resolution))#self.parameter.resolution)
        self.clock = pygame.time.Clock()

    def config_initialization(self) -> None:
        self.parameter = Parameters()
        self.seed = int(time.time() * 777)

    def check_if_QUIT(self, events, save_video) -> None:
        for event in events:
            if event.type == pygame.QUIT: 
                self.exit=True
                if save_video: imageio.mimsave(f'{self.parameter.experiment_folder}/recording.mp4', self.frames)

    def create_experiment_folder(self, address:str=""):
        if address != "": self.parameter.experiment_folder = address
        currentime = datetime.datetime.now()
        currentime = currentime.strftime(f"%Y-%m-%d_%H-%M-%S")
        new_folder = f"{self.parameter.experiment_folder}/Experiment {currentime}"
        os.makedirs(new_folder)
        self.parameter.experiment_folder = new_folder
        self.grid_folder = f"{self.parameter.experiment_folder}/Grids"
        os.makedirs(self.grid_folder)

    # Evo-experiment-Results
    # def get_plants_brains(self, file_name=""):
    #     if file_name=="": file_name= f"{self.parameter.experiment_folder}"
    #     file_name += "/Top10Oldest.txt"


    #     top_10_oldest = sorted(self.PlantsList, key=lambda plant: plant.age, reverse=True)[:10]
    #     with open(file_name, "a") as file:
    #         file.write(f"YEAR {self.step} -------------------------------------------------------\n")
    #         for plant in top_10_oldest:
    #             file.write("\n")
    #             file.write(f"{plant.age}\n")
    #             for matrix in plant.brain.transition_grid:
    #                 np.savetxt(file, matrix, fmt='%.5f', delimiter=' ')
    #                 file.write("\n")    

def main(max_steps,render,save_video):
    sim = EvoSim()
    sim.start_game(max_steps, render, save_video)

if __name__ == "__main__":
    main(max_steps=5000, render=False, save_video=True)