from global_vars import RESOLUTION, SCREEN_SIZE
import pygame, time

class Game():
    def __init__(self) -> None:
        self.initial_configuration()

    def start_game(self,render:bool=False) -> None:
        self.var_initialization()
        while not self.exit:
            events = pygame.event.get()
            self.check_if_QUIT(events)

            self.update(events)
            if render:
                self.before_draw()
                self.draw()
                self.update_screen()

    def get_configurations(self) -> str:
        output = f"""
        Configuration Variables\n
            - seed: {self.seed}\n
            - render: {self.render}\n
            - number of steps: {self.step}\n
            - simulation duration: [tempo]
        """

        return output

    def var_initialization(self,render:bool=False) -> None:
        self.AgentList = []
        self.PlantsList = []
        self.FruitList = []     
        self.exit = False
        self.render = False
        self.step = 0

    def initial_configuration(self) -> None:
        pygame.init()
        pygame.font.init()
        self.seed = int(time.time() * 777)
        self.resolution = RESOLUTION
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.canvas = pygame.Surface(self.resolution)
        self.clock = pygame.time.Clock()

    def check_if_QUIT(self, events) -> None:
        for event in events:
            if event.type == pygame.QUIT: 
                self.exit=True

    def update(self,events):
        self.step += 1

    def before_draw(self):
        pass

    def draw(self):
        pass

    def update_screen(self):
        pass