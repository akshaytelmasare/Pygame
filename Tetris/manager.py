import entity
from scene import MainScene
from globals import *

class SceneManager:
    def __init__(self):
        self.gmst = entity.GameStack()
        self.tetra = entity.Tetramino()
        self.nums = entity.Numbers()
        self.goto(MainScene())

    def goto(self,scene):
        self.scene = scene
        self.scene.manager = self

    def sync_m2s(self):
        self.scene.gmst = self.gmst
        self.scene.tetra = self.tetra
        self.scene.nums = self.nums

    def sync_s2m(self):
        self.gmst = self.scene.gmst 
        self.tetra = self.scene.tetra 
        self.nums = self.scene.nums 

    def lock(self):
        box = self.tetra.box()
        for y in range(len(box)):
            for x in range(len(box[0])):
                if(box[y][x]==1): self.gmst[y+self.tetra.ypos][x+self.tetra.xpos] = 1

    def coll_check(self,box,x0,y0):
        for y in range(len(box)):
            for x in range(len(box[0])):
                if(box[y][x]==1):
                    xi = x + x0
                    yi = y + y0
                    if(xi < 0 or yi < 0): return True
                    if(xi >= width or yi >= height): return True
                    if(self.gmst[yi][xi] == 1): return True
        return False
    
    def collision_t(self,xr,yr):
        box = self.tetra.box()
        xn = self.tetra.xpos + xr
        yn = self.tetra.ypos + yr
        return self.coll_check(box,xn,yn)
    
    def lines_to_clear(self):
        lc = []
        for y in range(height):
            kill = True
            for x in range(width): 
                if(self.gmst[y][x] == 0): 
                    kill = False
            if(kill): lc.append(y)
        return lc
    
    def clear_lines(self):                  
        lc = self.lines_to_clear() 
        cleared = len(lc)                    
        if(cleared):
            for y in lc:
                for x in range(width): self.gmst[y][x] = 0
            self.gmst.fall()
            self.nums.score_up(cleared) 
        
    def rotate(self,isRight):
        if(self.tetra.avatar == 'O'): return
        
        old = self.tetra.dir
        
        if(isRight): new = (old + 1)%4
        else: new = (old - 1)%4
        
        self.tetra.dir = new
        x,y = self.tetra.xpos,self.tetra.ypos
        box = self.tetra.box()
        
        if(not self.coll_check(box,x,y)): pass
        elif(not self.coll_check(box,x+1,y)): self.tetra.xpos += 1
        elif(not self.coll_check(box,x-1,y)): self.tetra.xpos -= 1
        
        elif(self.tetra.avatar == 'I'):
            if(not self.coll_check(box,x+2,y)): self.tetra.xpos += 2
            elif(not self.coll_check(box,x-2,y)): self.tetra.xpos -= 2
            else: self.tetra.dir = old
        else: self.tetra.dir = old

    def lock_and_respawn(self):
        self.lock()
        self.clear_lines()   
        self.tetra.respawn()
        
            