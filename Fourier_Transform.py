import pygame
import math
from math import e
from pygame import gfxdraw
import time
import random

pygame.init()
width, height = 1800, 900
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Fourrier Series")
started = False
w = 2 * math.pi
trace = []
n = 1000
f = []
f_c = []
colors = []
for i in range(n):
    colors.append([random.randint(0, 255) for j in range(3)])


def draw_circle(surface, color, x, y, radius):
    gfxdraw.aacircle(surface, x, y, radius, color)
    gfxdraw.filled_circle(surface, x, y, radius, color)


def setup(click, mx, my):
    global started, f, trace, n
    if click:
        f.append(mx + 1j * my)
        trace.append([mx, my])
    keys = pygame.key.get_pressed()
    if keys[pygame.K_s]:
        started = True
        n = len(f)
        init()
    if keys[pygame.K_r]:
        f = []
        trace = []
    draw_traces()


def draw_traces():
    if 2 < len(trace):
        pygame.draw.aalines(win, (255, 255, 255), False, trace)
    if len(trace) > 4000:
        trace.pop(0)


def fourrier_series(k):
    theta = k * w
    xc = yc = c = 0
    for i in range(n):
        radius = abs(f_c[i][0])
        c += f_c[i][0] * e ** (1j * theta * f_c[i][1] / n)
        x, y = c.real, c.imag
        if i != 0:
            gfxdraw.aacircle(win, int(xc), int(yc), int(radius), colors[i % len(colors)])
            pygame.draw.aaline(win, colors[i % len(colors)], [int(xc), int(yc)], [int(x), int(y)])
        xc, yc = x, y

    trace.append([xc, yc])
    draw_traces()


def init():
    global f_c, trace, t0
    trace = []
    for i in range(n):
        c = 0
        for j in range(n):
            c += f[j] * e ** (-i * j * w * 1j / n)
        f_c.append([c / n, i])
    t0 = time.time()
    f_c.sort(key=lambda x: abs(x[0]), reverse=True)


def main():
    run = True
    click = False
    mx, my = 0, 0
    clock = pygame.time.Clock()
    k = 0
    while run:
        clock.tick()
        win.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if not started:
            setup(click, mx, my)
        else:
            fourrier_series(k)
            k = (k + 1) * (k < n)
        click = False
        if pygame.mouse.get_pressed()[0]:
            click = True
        mx, my = pygame.mouse.get_pos()
        pygame.display.update()


main()

pygame.quit()
