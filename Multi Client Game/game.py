import pygame
from network import Network


class Player():
    width = height = 50

    def __init__(self, startx, starty, color=(255,0,0)):
        self.x = startx
        self.y = starty
        self.velocity = 5
        self.color = color
        self.bullets = []
        self.health = 10
        self.hitEvent = pygame.USEREVENT
        self.rect = pygame.Rect(self.x, self.y, 100, 100)

        

    def draw(self, g):
        g.blit(self.image, (self.x, self.y))
        self.rect = pygame.Rect(self.x, self.y, 100, 100)
        #pygame.draw.rect(g, self.color ,(self.x, self.y, self.width, self.height), 0)
    
    def drawBullets(self, g):
        for bullet in self.bullets:
            pygame.draw.rect(g.screen, self.color, bullet)

    def move(self, dirn):
        """
        :param dirn: 0 - 4 (right, left, up, down, space)
        :return: None
        """
        
        if dirn == 0:
            self.x += self.velocity
        elif dirn == 1:
            self.x -= self.velocity
        elif dirn == 2:
            self.y -= self.velocity
        elif dirn == 3:
            self.y += self.velocity
        elif dirn == 4:
            bullet = pygame.Rect(self.x, self.y + 48, 20, 10)
            if (len(self.bullets) < 5):
                self.bullets.append(bullet)
                pygame.time.delay(100)
            



class Game:

    def __init__(self, w, h):
        self.net = Network()
        self.width = w
        self.height = h
        self.player = Player(50, 50)
        self.player2 = Player(800,100)
        print(self.net.id)
        self.player.image = pygame.transform.scale(pygame.image.load('assets/crow.png'), (100, 100))
        self.player2.image = pygame.transform.scale(pygame.image.load('assets/johnson.png'), (100, 100))
        if(self.net.id == "0"):
            self.currPlayer = self.player
            self.oppPlayer = self.player2
            self.currPlayer.hitEvent += 1
            self.oppPlayer.hitEvent += 2
            self.currPlayer.color = (255,0,0)
            self.oppPlayer.color = (0,0,255)
        elif(self.net.id == "1"):
            self.currPlayer = self.player2
            self.oppPlayer = self.player
            self.currPlayer.hitEvent += 1
            self.oppPlayer.hitEvent += 2
            self.oppPlayer.color = (255,0,0)
            self.currPlayer.color = (0,0,255)
        
        self.canvas = Canvas(self.width, self.height, "Testing...")
        

    def run(self):
        clock = pygame.time.Clock()
        run = True
        while self.run:
            clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.K_ESCAPE:
                    run = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_RIGHT]:
                if self.currPlayer == self.player:
                    if self.currPlayer.x +100 <= (self.width)/2 - self.currPlayer.velocity:
                        self.currPlayer.move(0)
                elif self.currPlayer == self.player2:
                    if self.currPlayer.x +100 <= self.width - self.currPlayer.velocity:
                        self.currPlayer.move(0)

            if keys[pygame.K_LEFT]:
                if self.currPlayer == self.player:
                    if self.currPlayer.x >= self.currPlayer.velocity:
                        self.currPlayer.move(1)
                elif self.currPlayer == self.player2:
                    if self.currPlayer.x >= (self.width)/2 + self.currPlayer.velocity:
                        self.currPlayer.move(1)

            if keys[pygame.K_UP]:
                if self.currPlayer.y >= self.currPlayer.velocity:
                    self.currPlayer.move(2)

            if keys[pygame.K_DOWN]:
                if self.currPlayer.y + 100 <= self.height - self.currPlayer.velocity:
                    self.currPlayer.move(3)
                  
            if keys[pygame.K_SPACE]:
                self.currPlayer.move(4)

            

            # Send Network Stuff
            self.oppPlayer.x, self.oppPlayer.y, self.currPlayer.health = self.parse_data(self.send_data())

            # Update Canvas
            self.canvas.draw_background()
            self.handle_bullets(self.currPlayer, self.oppPlayer)
            
            if(self.currPlayer == self.player):
                self.canvas.draw_text(str.encode(str(self.currPlayer.health)), 50, 0,0)
                self.canvas.draw_text(str.encode(str(self.oppPlayer.health)), 50, (self.width)-50,0)
            elif(self.currPlayer == self.player2):
                self.canvas.draw_text(str.encode(str(self.currPlayer.health)), 50, (self.width)-50,0)
                self.canvas.draw_text(str.encode(str(self.oppPlayer.health)), 50, 0,0)
            self.currPlayer.draw(self.canvas.get_canvas())
            self.oppPlayer.draw(self.canvas.get_canvas())

            self.winner() 

            self.canvas.update()

        pygame.quit()

    def handle_bullets(self, p, p2):
        for bullet in p.bullets:
            if p == self.player:
                bullet.x += 7
            elif p == self.player2:
                bullet.x -= 7
            if p2.rect.colliderect(bullet):
                pygame.event.post(pygame.event.Event(p2.hitEvent))
                p.bullets.remove(bullet)
                p2.health -= 1
            elif bullet.x > self.width or bullet.x < 0:
                p.bullets.remove(bullet)
        for bullet in p2.bullets:
            if p2 == self.player:
                bullet.x += 7
            elif p2 == self.player2:
                bullet.x -= 7
            if p.rect.colliderect(bullet):
                pygame.event.post(pygame.event.Event(p.hitEvent))
                p2.bullets.remove(bullet)
                p.health -= 1
            elif bullet.x > self.width or bullet.x < 0:
                p2.bullets.remove(bullet)
        p.drawBullets(self.canvas)
        p2.drawBullets(self.canvas)
            
    def winner(self):
        if(self.player.health <= 0):
            self.canvas.draw_text(str.encode("Johnson Wins"), 100, (self.width)/2 - 350,(self.height)/2 - 15)
            self.reset()
            pygame.time.delay(5000)
        elif(self.player2.health <= 0):
            self.canvas.draw_text(str.encode("Crow Wins"), 100, (self.width)/2 - 230,(self.height)/2 - 15)
            self.reset()
            pygame.time.delay(5000)

    def reset(self):
        self.player.x = 50
        self.player.y = 100
        self.player2.x = 800
        self.player2.y = 100
        self.currPlayer.health = 10
        self.oppPlayer.health = 10
        self.player.bullets = []
        self.player2.bullets = []
        self.canvas.update()
    def send_data(self):
        """
        Send position to server
        :return: None
        """
        data = str(self.net.id) + ":" + str(self.currPlayer.x) + "," + str(self.currPlayer.y) +"," + str(self.oppPlayer.health) + ","
        reply = self.net.send(data)
        return reply

    @staticmethod
    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1]), int(d[2])
        except:
            return 800,100,10


class Canvas:

    def __init__(self, w, h, name="None"):
        self.width = w
        self.height = h
        self.bg = pygame.transform.scale(pygame.image.load('assets/space.jpg'), (1000,700))
        self.screen = pygame.display.set_mode((w,h))
        pygame.display.set_caption(name)

    @staticmethod
    def update():
        pygame.display.update()

    def draw_text(self, text, size, x, y):
        pygame.font.init()
        font = pygame.font.SysFont("comicsans", size)
        render = font.render(text, 1, (255,255,255))

        self.screen.blit(render, (x,y))

    def get_canvas(self):
        return self.screen

    
    def draw_background(self):
        self.screen.blit(self.bg, (0,0))
        pygame.draw.rect(self.screen, (255,0,255), ((self.width)/2 - 20, 0, 40, self.height))
     
    
