from grid import Grid, pickle

class SimulationAnalyser():
    def __init__(self, simulation_grid_object:str) -> None:
        with open(simulation_grid_object, "rb") as file:
            self.grid_object = pickle.load(file)    
        self.all_grids = []       
        # for i,grid in enumerate(self.grid_object.all_grid_steps):
        #     print(i)
        #     self.all_grids.append(pickle.loads(grid))
        self.all_grids = self.grid_object.all_grid_steps
        self.environment = self.grid_object.environment
        self.id = self.grid_object.id   
        self.x_size = self.grid_object.x_size
        self.y_size = self.grid_object.y_size
        self.total_steps = len(self.all_grids)
        
    def draw_simulation(self, screen_size:tuple[int,int]=(0,0)):
        if screen_size[0]==0: screen_size=(self.x_size,self.y_size)        
        import pygame
        pygame.init()
        screen = pygame.display.set_mode(screen_size)
        canvas = pygame.Surface((self.x_size,self.y_size))
        font = pygame.font.Font(None,16)
        
        for step, grid in enumerate(self.all_grids):
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT: 
                    break
            #clear screen
            canvas.fill((0, 0, 0))
            
            #
            plants_n = 0
            fruits_n = 0
            #draw plants
            for y in range(self.y_size):
                for x in range(self.x_size):
                    if "plant" in grid[x][y]: 
                        canvas = grid[x][y]["plant"].draw(canvas)
                        plants_n += 1
                    if "fruit" in grid[x][y]:
                        fruits_n += 1
            # for x,y in grid.plants_occupy:
            #     canvas = grid.grid[x][y]["plant"].draw(canvas)
                
            #draw texts
            step_text = font.render(f"{step+1}",True, (255,0,255))
            n_plants_text = font.render(f"{plants_n}", True, (255,0,255))
            n_fruits_text = font.render(f"{fruits_n}", True, (255,0,255))
            canvas.blit(step_text,(5,5))
            canvas.blit(n_plants_text,(5,25))
            canvas.blit(n_fruits_text,(5,45))
            
            #update screen
            scaled_canvas = pygame.transform.scale(canvas, screen_size)
            screen.blit(scaled_canvas, (0, 0))  # Draw scaled canvas on the screen
            pygame.display.update() 
        pygame.quit()
        
if __name__ == "__main__":
    simulation = SimulationAnalyser(simulation_grid_object="/home/nonato/GitRepositories/evo-experiment/Evo-experiment-Results/Experiment 2024-12-09_17-35-25/simulation-b37b5d59-70fd-4c67-b6f0-63f09e7d08dd")        
    simulation.draw_simulation((500,500))
    print(simulation.total_steps)
        
