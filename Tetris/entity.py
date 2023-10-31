from globals import *
from random import shuffle

class Numbers:
    def __init__(self):
        self.counter = 0
        self.level = 1
        self.score = 0
        self.speed = 60
        self.templc = 0
        
    def counter_up(self):
        if(self.counter == self.speed):
            self.counter = 0
            return True
        else: 
            self.counter += 1
            return False
            
    def spd(self):
        sec = (0.8-((self.level-1)*0.007))**(self.level-1)
        self.speed = int(60*sec)

    def score_up(self,lc):
        match lc:
            case 1: self.score += 100
            case 2: self.score += 300
            case 3: self.score += 500
            case 4: self.score += 800
        
        self.templc += lc
        
        if(self.templc > self.level*10):
            self.templc -= self.level*10
            self.level += 1
            self.spd()
            self.counter = 0

class Tetramino:
    shape = {}
    shapes = {
        'I':[[0,0,0,0],[1,1,1,1],[0,0,0,0],[0,0,0,0]],
        'O':[[1,1],[1,1]],
        'L':[[0,0,1],[1,1,1],[0,0,0]],
        'J':[[1,0,0],[1,1,1],[0,0,0]],
        'T':[[0,1,0],[1,1,1],[0,0,0]],
        'S':[[0,1,1],[1,1,0],[0,0,0]],
        'Z':[[1,1,0],[0,1,1],[0,0,0]]
    }

    def __init__(self):
        self.bag = ['I','O','J','L','S','T','Z']
        self.shape_up()
        shuffle(self.bag)
        self.bagpos = 0
        self.respawn()
        
    def respawn(self):
        self.bagpos += 1
        if(self.bagpos == 7):
            self.bagpos = 0
            shuffle(self.bag)
        self.avatar = self.bag[self.bagpos]
        
        self.dir = 0
        self.xpos = int(width/2) - 1
        self.ypos = 0
        if(self.avatar == 'I'): self.ypos = -1             #check it later
        

    def rotate90(self,box):
        ys = len(box)
        xs = len(box[0])
        
        rbox = [[0 for x in range(ys)] for y in range(xs)]
        for y in range(xs):
            for x in range(ys):
                rbox[y][x] = box[ys-x-1][y]
        return rbox 
    
    def box(self):
        return self.shape[self.avatar][self.dir]
     
    def shape_up(self):
        for avatar in self.bag:
            t0 = self.shapes[avatar]
            t1 = self.rotate90(t0)
            t2 = self.rotate90(t1)
            t3 = self.rotate90(t2)
            self.shape[avatar] = [t0,t1,t2,t3]

class Brick:
    def __init__(self,l,r):
        self.left = l
        self.right = r

    def can_fall(self,l):
        for i in range(self.left,self.right+1):
            if(l[i]==1): return False
        return True

    def unbrick(self,l):
        for i in range(self.left,self.right+1): l[i] = 1
        return l

class GameStack(list):
    def __init__(self):
        self.extend([[0 for x in range(width)] for y in range(height)])

    def make_bricks(self):
        well = []
        for y in range(height):
            input = []
            left, right, off = -1, -1, True
            for x in range(width):
                if(off and self[y][x]==0): pass
                if(off and self[y][x]==1): left, right, off = x, x, False
                if(not off and self[y][x]==1): right = x
                if(not off and self[y][x]==0): 
                    input.append(Brick(left,right)) 
                    off = True
            if(not off): input.append(Brick(left,width-1))
            s = set(input)
            well.append(s)
        return well
        
    def gravity(self,well):
        change = False
        for i in range(height-1,0,-1):
            l = [0 for x in range(width)]
            for brick in well[i]:
                l = brick.unbrick(l)
            for brick in well[i-1].copy():
                if(brick.can_fall(l)):
                    change = True
                    well[i].add(brick)
                    well[i-1].remove(brick)
        if(change): well = self.gravity(well)   
        return well

    def fall(self):
        well = self.make_bricks()
        well = self.gravity(well)
        for y in range(height):
            l = [0 for x in range(width)]
            for brick in well[y]:
                l = brick.unbrick(l)
            self[y] = l 
            
    

