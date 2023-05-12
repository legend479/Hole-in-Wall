from operator import pos
import pygame
import random


from pygame import surface
from pygame.version import PygameVersion

pygame.font.init()
WIN_SIZE=600# Keep it a fair or keep it square
FILES=15 #Factor of win size or else....

STAT_FONT=pygame.font.SysFont("comic sans",36,True)
class Player:
    SIZE=WIN_SIZE/FILES

    def __init__(self,color):
        self.x=WIN_SIZE/2 - self.SIZE/2
        self.y=self.x
        self.color=color  
    
    def Draw(self,surface):
        pygame.draw.rect(surface,self.color,(self.x,self.y,self.SIZE,self.SIZE))
    
    def Move(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.y>0:
            self.y-=WIN_SIZE/FILES
        elif keys[pygame.K_DOWN] and self.y< WIN_SIZE-self.SIZE:
            self.y+=WIN_SIZE/FILES
        if keys[pygame.K_LEFT] and self.x>0:
            self.x-=WIN_SIZE/FILES
        elif keys[pygame.K_RIGHT] and self.x<WIN_SIZE-self.SIZE:
            self.x+=WIN_SIZE/FILES
    
class Walls:
    SIZE=WIN_SIZE/FILES
    def __init__(self,direcn,wall,color) :#direcn=[(1,0)up,(-1,0)down,(1,1)left,(-1,1)right]]
        if direcn[0]==1:       
            self.pos=-2*self.SIZE
        elif direcn[0]==-1:
            self.pos=WIN_SIZE + self.SIZE
        
        #hole= position of the 0 in the list EX- 3file [1,0,1] hole in the mid [1,0,0] two holes at right end
        self.wall=wall
        self.direcn=direcn
        self.color=color
        self.passed=False

    def Draw(self,surface):
        if  not self.direcn[1]:
            for i in range(FILES):
                if self.wall[i]!=0:
                    pygame.draw.rect(surface,self.color,(i*self.SIZE,self.pos,self.SIZE,self.SIZE))
        else:
            for i in range(FILES):
                if self.wall[i]!=0:
                    pygame.draw.rect(surface,self.color,(self.pos,i*self.SIZE,self.SIZE,self.SIZE))
    
    def Move(self):
        self.pos=self.pos+self.direcn[0]*self.SIZE
    
    def Collide(self,player):
        z=False
        if  not self.direcn[1]:
            if player.y==self.pos:
                for i,x in enumerate(self.wall):
                    if x and player.x==(i)*self.SIZE:
                        z=True
                        break
        else:
            if player.x==self.pos:
                for i,x in enumerate(self.wall):
                    if x and player.y==(i)*self.SIZE:
                        z=True
                        break
        return z          
        
def Generate_Random_Wall(walls):
    direc=random.choice([(1,0),(-1,0),(1,1),(-1,1)])
    hole_number=random.randrange(1,4)
    hole=[]
    wall=[]
    for _ in range(hole_number):
        hole.append(random.randrange(0,FILES))
    for i in range(FILES):
        if i in hole: wall+=[0]
        else: wall+=[1]
    color = random.choice([(0,255,0),(0,0,255),(255,0,127),(255,128,0),(0,204,204),(0,102,51),(160,160,160),(102,0,51),(0,51,51),(102,0,0),(0,255,255),(255,255,0),(204,102,0),(255,0,255)])
    walls.append(Walls(direc,wall,color))

def DrawGrid(surface):
    #Row
    for i in range(FILES):
        pygame.draw.line(surface,(0,0,0),(0,i*WIN_SIZE/FILES),(WIN_SIZE,i*WIN_SIZE/FILES),2)
    for i in range(FILES):
        pygame.draw.line(surface,(0,0,0),(i*WIN_SIZE/FILES,0),(i*WIN_SIZE/FILES,WIN_SIZE),2)

def DrawWindow(surface,walls,score,player):
    #Drawing the screen
        surface.fill((255,255,255))
        player.Draw(surface)
        for wall in walls:
            wall.Draw(surface)
        DrawGrid(surface)
        text=STAT_FONT.render("Score: "+ str(score), 1, (0,0,0))
        surface.blit(text, (WIN_SIZE-5-text.get_width(),WIN_SIZE/30))

        pygame.display.update()

def Main():
    Screen=pygame.display.set_mode((WIN_SIZE,WIN_SIZE))
    p1=Player((255,0,0))
    walls=[]
    Generate_Random_Wall(walls)
    run=True

    Clock=pygame.time.Clock()
    x=0
    vel=3
    score=0

    while run:
        Clock.tick(7)
        #wall to move at 2 ticks and then speed up
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
       
        #Moving the elements
        p1.Move()
        if x>=vel:
            for wall in walls:
                wall.Move()
            x=0

        add_wall=False
        for wall in walls:
            if wall.direcn==(1,1):                                                      #left
                if p1.x<wall.pos and not wall.passed: add_wall,wall.passed=True,True
                if wall.pos>WIN_SIZE: walls.remove(wall)

            elif wall.direcn==(-1,1) :                                                  #right
                if p1.x>wall.pos and not wall.passed: add_wall,wall.passed=True,True
                if wall.pos<0: walls.remove(wall)

            elif wall.direcn==(1,0):                                                    #up
                if p1.y<wall.pos and not wall.passed: add_wall,wall.passed=True,True
                if wall.pos>WIN_SIZE: walls.remove(wall)

            elif wall.direcn==(-1,0):                                                   #down
                if p1.y>wall.pos and not wall.passed: add_wall,wall.passed=True,True
                if wall.pos<0: walls.remove(wall)
        
        if add_wall:
            score+=1
            Generate_Random_Wall(walls)
            add_wall=False
            vel-=0.1

        for wall in walls:
            if wall.Collide(p1): run=False

        DrawWindow(Screen,walls,score,p1)
        x+=1
    
    text=STAT_FONT.render("GAME OVER", 1, (0,0,0))
    Screen.blit(text, (WIN_SIZE/2-text.get_width()/2,WIN_SIZE/2-text.get_height()/2))
    pygame.display.update()
    _=input("Press enter to exit.........")
    pygame.display.quit()
    quit()

if __name__ =="__main__":
    Main()