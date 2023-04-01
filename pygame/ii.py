
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
            self.vertex.append((

    def dis_to_brick(self, x, y):
        return self.poly.dist_to_poly(x, y)


class Ball():
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.x_direction = choice((-2, 2))
        self.y_direction = -2
        self.radius = radius

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
        if self.x + self.radiu
