from __future__ import division

import time

import numpy as np
import pygame
import sys
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from numpy import array, linalg, frombuffer, fromstring, short
from OpenGL.GL import shaders
from sys import exit as exitsystem
from math import cos, sin, pi
from Vector import *


def toRadians(degrees):
    return degrees * pi / 180


def ReadFile(filename):
    data = ""
    with open(filename, 'r') as f:
        data = f.read()
    return data


VERTEX_SHADER = ReadFile("vertexShader.glsl")
FRAGMENT_SHADER = ReadFile("fragmentShader.glsl")


class Renderer:
    def __init__(self, width, height):
        pygame.init()
        self.resolution = width, height
        self.identity = np.identity(4)

        pygame.display.set_mode(self.resolution, DOUBLEBUF | OPENGL)

        self.clock = pygame.time.Clock()
        self.clock.tick(60)

        self.quadVertices = array([-1.0, -1.0, 0.0,
                                   1.0, -1.0, 0.0,
                                   1.0, 1.0, 0.0,
                                   -1.0, 1.0, 0.0], dtype='float32')

        self.vertex_shader = shaders.compileShader(VERTEX_SHADER, GL_VERTEX_SHADER)
        self.fragment_shader = shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
        self.shader = shaders.compileProgram(self.vertex_shader, self.fragment_shader)
        # Uniform variables
        self.uniformMouse = glGetUniformLocation(self.shader, 'iMouse')
        self.uniformTime = glGetUniformLocation(self.shader, 'iTime')
        self.uniformValue = glGetUniformLocation(self.shader, 'u_value')
        # self.uniformProjection = glGetUniformLocation(self.shader, 'u_projection')
        self.uniformModel = glGetUniformLocation(self.shader, 'u_model')
        glUseProgram(self.shader)

        # self.uniformCameraPosition = glGetUniformLocation(self.shader, "u_camPosition")
        # self.uniformOrientation = glGetUniformLocation(self.shader, 'u_orientation')
        # self.uniformViewDistance = glGetUniformLocation(self.shader, 'u_viewDistance')
        # self.uniformView = glGetUniformLocation(self.shader, "u_view")
        self.uniformResolution = glGetUniformLocation(self.shader, 'iResolution')
        glUniform2f(self.uniformResolution, *self.resolution)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.quadVertices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)


    def mainloop(self):
        while True:
            delta = self.clock.tick(8192)
            deltaTime = delta / 1000

            glClearColor(0.0, 0.0, 0.0, 1.0)

            glClear(GL_COLOR_BUFFER_BIT)

            glUseProgram(self.shader)

            mx, my = pygame.mouse.get_pos()

            mx = (1.0 / self.resolution[0] * mx) * 2.0 - 1.0
            my = (1.0 / self.resolution[1] * my) * 2.0 - 1.0

            glUniform2f(self.uniformMouse, mx, my)
            glUniform1f(self.uniformTime, pygame.time.get_ticks() / 1000.0)

            glBindVertexArray(self.vao)
            glDrawArrays(GL_QUADS, 0, 4)
            pygame.display.set_caption(f"FPS: {int(self.clock.get_fps())}")
            pygame.display.flip()

            self.handelEvents()

    def handelEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


if __name__ == '__main__':
    renderer = Renderer(1920, 1080)
    renderer.mainloop()
