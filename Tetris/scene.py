import pygame,entity,sys
import render as rd
from globals import *

class Scene:
    def __init__(self):
        pass

    def handles(self):
        kp = {
            't_right': False, 't_left': False, 't_down': False,
            'r_right': False, 'r_left': False,
            'lock_down': False, 'pause': False
        }
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_SPACE: kp['pause'] = True
                    case pygame.K_DOWN: kp['t_down'] = True
                    case pygame.K_UP: kp['lock_down'] = True
                    case pygame.K_RIGHT: kp['t_right'] = True
                    case pygame.K_LEFT: kp['t_left'] = True
                    case pygame.K_RSHIFT: kp['r_right'] = True
                    case pygame.K_RCTRL: kp['r_left'] = True 
        return kp
    
    def updates(self):
        raise NotImplementedError
    
    def render(self):
        raise NotImplementedError
    
class MainScene(Scene):
    def __init__(self):
        super().__init__()
        self.gmst = entity.GameStack()
        self.tetra = entity.Tetramino()
        self.nums = entity.Numbers()
        
    def updates(self,kp):
        self.manager.sync_s2m()
        #Pause
        if(kp['pause']):
            self.manager.goto(PauseScene())

        #Counter Check
        if(self.nums.counter_up()):
            if(not self.manager.collision_t(0,1)): self.manager.tetra.ypos +=1
            else:
                self.manager.lock_and_respawn()
                return
        
        #Lock Down
        if(kp['lock_down']):
            while(not self.manager.collision_t(0,1)): self.manager.tetra.ypos += 1
            self.manager.lock_and_respawn()
            return
        
        #Move Right
        if(kp['t_right'] and not kp['t_left']):
            if(not self.manager.collision_t(1,0)): self.manager.tetra.xpos += 1
        
        #Move Left
        if(kp['t_left'] and not kp['t_right']):
            if(not self.manager.collision_t(-1,0)): self.manager.tetra.xpos -= 1

        #Move Down
        if(kp['t_down']):
            if(not self.manager.collision_t(0,1)): 
                self.manager.tetra.ypos += 1
                self.manager.nums.counter = 0

        #Rotate Right
        if(kp['r_right'] and not kp['r_left']): self.manager.rotate(True)

        #Rotate Left
        if(kp['r_left'] and not kp['r_right']): self.manager.rotate(False)

    def render(self,screen):
        self.manager.sync_m2s()
        #Numbers and Blank Screen
        rd.draw_numbers(self.nums)
        screen.fill(black)
        
        #set board and fill it blank
        board = pygame.Surface(size=(size*width,size*height))
        board.fill(black)
        
        #draw stack and tetramino on board
        box = self.tetra.box()
        rd.draw_gamestack(board,self.gmst)
        rd.draw_box(board,box,self.tetra.xpos,self.tetra.ypos,red)
        
        #draw shadow on board
        z = self.tetra.ypos
        while(not self.manager.coll_check(box,self.tetra.xpos,z+1)): z += 1
        if(z != self.tetra.ypos): rd.draw_box(board,box,self.tetra.xpos,z,white)
        
        #blit and display
        screen.blit(board,(0,0))
        pygame.display.flip()
        
class PauseScene(Scene):
    def __init__(self):
        super().__init__()

    def updates(self,kp):
        if(kp['pause']):
            self.manager.goto(MainScene())
    
    def render(self,screen):
        MainScene.render(self,screen)
        
        
        