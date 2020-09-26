import pygame
from random import random
from math import sqrt

SCREEN_SIZE = (1280, 720)


class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def int_pair(self):
        a = (self.x, self.y,)
        return a

    def __len__(self):
        return sqrt(int(self.x) ** 2 + int(self.y) ** 2)

    def __mul__(self, other):
        return Vector(int(self.x) * other, int(self.y) * other)

    def __add__(self, other):
        return int(self.x) + other.x, int(self.y) + other.y

    def __sub__(self, other):
        return Vector(int(self.x) - other.x, int(self.y) - other.y)

    def __repr__(self):
        return self.x, self.y


class Line(Vector):
    def __init__(self, x, y, speed=(0, 0,)):
        super().__init__(x, y)
        self.speed = speed

    def set_points(self):
        return Vector.__add__(Vector(self.x, self.y), Vector(self.speed[0], self.speed[1]))

    def draw_points(self, other=None, style="points", width=4, color=(255, 255, 255)):
        if style == "line":
            pygame.draw.line(gameDisplay, color, int(self.x, int(self.y)),
                             (int(other.x), int(other.y)), width)

        elif style == "points":
            pygame.draw.circle(gameDisplay, color,
                               (int(self.x), int(self.y)), width)

    def __repr__(self):
        return self.speed


'''class Joint(Line):
    
    def __init__(self, count, speed):
        super().__init__(speed)
        self.count = count
    
    def get_joint(self, other):
        result = []
        pnt = []
        pnt.append(Vector.__mul__(Vector.__add__(Vector(), other()), 0.5))
        pnt.append(other)
        pnt.append(multiply(add(points[i + 1], points[i + 2]), 0.5))

        result.extend(get_points(pnt, count))
        return result'''


def display_help():
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("arial", 30)
    font2 = pygame.font.SysFont("serif", 30)
    data = [["F1", "Помощь"], ["R", "Перезапуск"], ["P", "Воспроизвести / Пауза"], ["Num+", "Добавить точку"],
            ["Num-", "Удалить точку"], ["", ""], [str(steps), "текущих точек"]]

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for item, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * item))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * item))


if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Screen Saver")

    steps = 20
    cnt = 0
    working = True
    points = []
    speeds = []
    show_help = False
    pause = False

    color_param = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    points = []
                    speeds = []
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                cnt += 1
                points.append(Vector(event.pos[0], event.pos[1]))
                speeds.append(Vector(random() * 2, random() * 2))

        gameDisplay.fill((0, 0, 0))
        color_param = (color_param + 1) % 360
        color.hsla = (color_param, 100, 50, 100)
        if len(points) > 0:
            for i in range(len(points)):
                Line.draw_points(points[i])#draw_points(points)

        if cnt >= 3:
            Line.draw_points("line", 4, color)#draw_points(get_joint(points, steps), "line", 4, color)

        if not pause:
            if len(points) > 0:
                for j in range(len(points)):
                    points[j] = Vector.__add__(points[j], speeds[j])
                    if points[j][0] > SCREEN_SIZE[0] or points[j][0] < 0:
                        speeds[j] = (- speeds[j][0], speeds[j][1])
                    if points[j][1] > SCREEN_SIZE[1] or points[j][1] < 0:
                        speeds[j] = (speeds[j][0], -speeds[j][1])
                    #b = Line(speeds[0], speeds[1])
                    #b.set_points()
        if show_help:
            display_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)

