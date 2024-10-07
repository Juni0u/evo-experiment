import pygame, uuid, random, time
from creature import Creature

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
        self.add_agent(64,64,(255,0,0),0,"0101000101001010101010")
        self.add_agent(64,34,(255,255,0),0,"0101000101001010101010")
        self.add_agent(64,94,(255,0,255),0,"0101000101001010101010")
        self.add_agent(34,64,(0,255,0),0,"0101000101001010101010")
        self.add_agent(94,64,(0,0,255),0,"0101000101001010101010")
        self.create_agent_population(20)

    def update(self):
        for agent in self.Agents:
            agent.update(seed=self.seed)

    def draw(self):
        for agent in self.Agents:
            agent.draw(canvas)
        
    def add_agent(self,x:int,y:int,color:tuple,born_in:int,chromosome:str):
        id = uuid.uuid4()
        self.Agents.append(Creature(id,x,y,color,born_in,chromosome))

    def create_agent_population(self,quantity):
        for i in range(quantity):
            chromosome = ""
            for _ in range(22): #chromosome lenght
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