# Dice Roller
# Written by Jon Etiz
# Created on 03SEP2022

from dataclasses import dataclass
import this
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from math import sqrt

v = (
    [0, 1, 0],
    [sqrt(8/9), -1/3, 0],
    [-sqrt(2/9), -1/3, sqrt(2/3)],
    [-sqrt(2/9), -1/3, -sqrt(2/3)]
)

e = (
    (0, 1),
    (0, 2),
    (0, 3),
    (1, 2),
    (1, 3),
    (2, 3)
)

f = (
    (0, 1, 2),
    (0, 2, 3),
    (0, 1, 3),
    (1, 2, 3)
)

ground_vertices = (
    (100, -1, 100),
    (100, -1, -100),
    (-100, -1, -100),
    (-100, -1, 100)
)


@dataclass(frozen=True)
class Shape:
    vertices: tuple
    faces: tuple
    edges: tuple


class Entity:
    def __init__(self, position, shape: Shape):
        self.position = position
        self.shape = shape

    def draw(self):
        glBegin(GL_QUADS)
        glColor3fv((0.5, 0.5, 0.5))
        for face in self.shape.faces:
            for vertex in face:
                glVertex3fv(tuple(map(lambda i, j: i + j, self.position, self.shape.vertices[vertex])))

        glEnd()

        # Begin the process of drawing lines
        glBegin(GL_LINES)
        glColor3fv((1, 1, 1))
        for edge in self.shape.edges:
            # For each edge take the corresponding verticies
            for vertex in edge:
                # Applies vertices to the above function (in this case, draws lines)
                glVertex3fv(tuple(map(lambda i, j: i + j, self.position, self.shape.vertices[vertex])))
                # if this.shape.vertices[vertex][1] > -3:
                #     this.shape.vertices[vertex][1] = this.shape.vertices[vertex][1] - 0.01
        glEnd()

        if self.position[1] > -3:
            self.position[1] = self.position[1] - 0.01


tetrahedron = Shape(v, f, e)
tetrahedral_die = Entity([0, 0, 0], tetrahedron)


def Ground():
    glBegin(GL_QUADS)
    for vertex in ground_vertices:
        glColor3fv((0, 0.5, 0.2))
        glVertex3fv(vertex)

    glEnd()


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(90, display[0]/display[1], 0.0, 50.0)

    glTranslatef(0.0, 0.0, -5)
    glRotatef(0, 0, 0, 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Ground()
        tetrahedral_die.draw()
        pygame.display.flip()
        pygame.time.wait(10)


main()
