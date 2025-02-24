import pygame
import pyivp
import json
from random import choice

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
WHITE = (255, 255, 255)


class Brick():
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.poly = pyivp.string_to_poly(
            "x = " + str(x) + ", y = " + str(y) + ", format = radial, radius = " + str(radius) + ", pts = 4")
        self.get_vertex()

    def get_vertex(self):
        self.vertex = []
        self.seg = self.poly.export_seglist()
        for i in range(self.seg.size()):
            self.vertex.append((self.seg.get_vx(i), self.seg.get_vy(i)))

    def draw(self, screen):
        pygame.draw.lines(screen, WHITE, True, self.vertex)

    def dis_to_brick(self, x, y):
        return self.poly.dist_to_poly(x, y)


class Ball():
    def __init__(self, x, y, radius):
        self.x = 300
        self.y = 400
        self.x_direction = choice((-2, 2))
        self.y_direction = -2
        self.radius = 10

    def move(self):
        self.x += self.x_direction
        self.y += self.y_direction
        self.contact_detect_wall()

    def bounce(self, brick):
          if self.x < brick.x - (brick.radius / 1.414):
            self.x_direction = -2
          elif self.x > brick.x + (brick.radius / 1.414):
            self.x_direction = 2
          elif self.y < brick.y - (brick.radius / 1.414):
            self.y_direction = -2
          elif self.y > brick.y + (brick.radius / 1.414):
            self.y_direction = 2

    def contact_detect_wall(self):
        if self.x + self.radius >= SCREEN_WIDTH or\
                self.x - self.radius <= 0:
            self.x_direction = -self.x_direction

        if self.y + self.radius >= SCREEN_HEIGHT or\
                self.y - self.radius <= 0:
            self.y_direction = -self.y_direction

    def contact_detect_brick(self, bricks):
        for brick in bricks:
           if (brick.dis_to_brick(self.x, self.y) - self.radius <= 0):
            self.bounce(brick)
            bricks.remove(brick)
            break
        
    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius)
class Pad:
    def __init__(self, x, y, w, h):
        self.x=x
        self.y=y
        self.w=w
        self.h=h

    def draw(self,screen):
        pygame.draw.rect(screen, (255,255,255), (self.x,self.y, self.w, self .h))

    def move_left(self):
        self.x -= 5
    def move_right(self):
        self.x += 5
    def bounce_ball(self, ball):
        if ball.y + ball.radius >=self.y and ball.x >=self.x and ball.x <= self.x +self.w:
            ball.y_direction = -ball.y_direction
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Brick')

# load config
with open('./config/07_config.json', 'r') as f:
    config = json.load(f)

ball = Ball(config["ball_x"], config["ball_y"], config["ball_radius"])
pad = Pad(config["pad_x"], config["pad_y"],config["pad_w"], config["pad_h"])
bricks = []
for i in config["bricks"]:
     brick=Brick(i["x"],i["y"],i["radius"])
     bricks.append(brick)
# game loop
is_running = True
while is_running:
    screen.fill((0, 0, 0))
    for brick in bricks:
       brick.draw(screen)
    ball.contact_detect_brick(bricks)
    ball.move()
    for brick in bricks:
        brick.draw(screen)
    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            is_running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        pad.move_left()
    elif keys[pygame.K_RIGHT]:
        pad.move_right()
    pad.bounce_ball(ball)
    pad.draw(screen)
    ball.draw(screen)
    pygame.display.flip()
    clock.tick(50)
pygame.quit()
