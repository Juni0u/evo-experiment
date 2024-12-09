class ColorGradient():
    def __init__(self) -> None:
        self.gradient_dict = {}
        
    def addGradient(self,name:str,color_i:tuple[int,int,int],color_f:tuple[int,int,int],steps:int) -> tuple:
        if not (isinstance(color_i, tuple) and len(color_i) == 3 and all(isinstance(c, int) for c in color_i)):
            raise ValueError("A cor inicial deve ser uma tupla de três inteiros.")
        if not (isinstance(color_f, tuple) and len(color_f) == 3 and all(isinstance(c, int) for c in color_f)):
            raise ValueError("A cor final deve ser uma tupla de três inteiros.")
        if steps < 2:
            raise ValueError("O número de steps deve ser pelo menos 2.")
        
        gradient = []
        for i in range(steps):
            r = color_i[0] + (color_f[0] - color_i[0]) * i / (steps - 1)
            g = color_i[1] + (color_f[1] - color_i[1]) * i / (steps - 1)
            b = color_i[2] + (color_f[2] - color_i[2]) * i / (steps - 1)
            gradient.append((round(r), round(g), round(b)))
        
        self.gradient_dict[name] = tuple(gradient)
        return tuple(gradient)  
    
if __name__ == "__main__":
    import pygame
    pygame.init()
    screen = pygame.display.set_mode((500,500))
    canvas = pygame.Surface((500,500))
    font = pygame.font.Font(None,16)

    
    ColorBase = ColorGradient()
    ColorBase.addGradient(name="Flamengo",color_i=(255,0,0),color_f=(0,0,0),steps=15)
    ColorBase.addGradient(name="Vasco",color_i=(255,255,255),color_f=(0,0,0),steps=15)  
    name = "Vasco"
    
    
    color_list = list(ColorBase.gradient_dict[name])
    print(color_list)
    index = 0
    exit = 0
    while (not exit):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT: 
                exit=True
                
        index = (index + 1) % len(color_list)

        color_index = font.render(f"{name}: {index}/{len(color_list)}",True, (0,0,0))

        canvas.fill(color_list[index])
        canvas.blit(color_index,(5,5))
        screen.blit(canvas,(0,0))

        pygame.display.flip()
        pygame.time.delay(500)


        
        

    
    