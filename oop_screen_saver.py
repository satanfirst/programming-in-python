import pygame
import math
import random

SCREEN_DIM = (800, 600)
BACKGROUND_COLOR = (0, 0, 0)


class Vec2d:
    """class of 2-dimensional vectors"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'({self.x}, {self.y})'

    def __add__(self, other):
        return Vec2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2d(self.x - other.x, self.y - other.y)

    def __mul__(self, k):
        return Vec2d(self.x * k, self.y * k)

    def __len__(self):
        return int(math.sqrt(self.x * self.x + self.y * self.y))

    def int_pair(self):
        return self.x, self.y


class Polyline:
    """"class of closed polygons with methods responsible for adding points to the polygonal line with its speed"""
    count = 0
    points = []
    speeds = []

    def __init__(self, game_display):
        self.game_display = game_display

    def set_point(self, tupl):
        self.points.append(Vec2d(tupl[0], tupl[1]))

    def set_speed(self, tupl):
        self.speeds.append(Vec2d(tupl[0], tupl[1]))

    def set_points(self):
        """reference point coordinate recalculation function"""
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p].x > SCREEN_DIM[0] or self.points[p].x < 0:
                self.speeds[p] = Vec2d(-self.speeds[p].x, self.speeds[p].y)
            if self.points[p].y > SCREEN_DIM[1] or self.points[p].y < 0:
                self.speeds[p] = Vec2d(self.speeds[p].x, -self.speeds[p].y)

    def draw_points(self, points, style="points", width=3, color=(255, 255, 255)):
        """polyline drawing"""
        if style == "line":
            for p_n in range(-1, len(points) - 1):
                pygame.draw.line(self.game_display, color,
                                 (int(points[p_n].x), int(points[p_n].y)),
                                 (int(points[p_n + 1].x), int(points[p_n + 1].y)), width)
        elif style == "points":
            for p in points:
                pygame.draw.circle(self.game_display, color,
                                   (int(p.x), int(p.y)), width)

    def draw_help(self):
        """program help screen rendering function"""
        self.game_display.fill((50, 50, 50))
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        data = []
        data.append(["F1", "Show Help"])
        data.append(["R", "Restart"])
        data.append(["P", "Pause/Play"])
        data.append(["Num+", "More points"])
        data.append(["Num-", "Less points"])
        data.append(["Del", "Delete the last point added"])
        data.append(["u", "speed up"])
        data.append(["d", "speed down"])
        data.append(["", ""])
        data.append([str(self.count), "Current points"])

        pygame.draw.lines(self.game_display, (255, 50, 50, 255), True, [
            (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for i, text in enumerate(data):
            self.game_display.blit(font1.render(
                text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
            self.game_display.blit(font2.render(
                text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


class Knot(Polyline):
    def __init__(self, game_display):
        super(Knot, self).__init__(game_display=game_display)

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + self.get_point(points, alpha, deg - 1) * (1 - alpha)

    def get_points(self, base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def get_knot(self):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)
            res.extend(self.get_points(ptn, self.count))
        return res

    def speed_change(self, value):
        self.speeds = [item * value for item in self.speeds]


def main():
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("ScreenSaver with OOP")

    play = True
    pause = True
    show_help = False
    speed = 1
    hue = 0
    color = pygame.Color(0)
    game_obj = Knot(gameDisplay)
    game_obj.count = 35

    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    play = False
                if event.key == pygame.K_r:
                    game_obj.points = []
                    game_obj.speeds = []
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    game_obj.count += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    game_obj.count -= 1 if game_obj.count > 1 else 0
                if event.key == pygame.K_DELETE:
                    game_obj.points.pop()
                    game_obj.speeds.pop()
                if event.key == pygame.K_d:
                    if 0.4 < speed:
                        speed -= 0.1
                    elif 1 > speed >= 1.5:
                        speed -= 1.1
                    game_obj.speed_change(speed)
                if event.key == pygame.K_u:
                    if 0.2 < speed < 1:
                        speed += 0.5
                    elif 1 <= speed < 1.5:
                        speed += 0.1
                    game_obj.speed_change(speed)

            if event.type == pygame.MOUSEBUTTONDOWN:
                game_obj.set_point(event.pos)
                game_obj.set_speed((random.random() * 2, random.random() * 2))

        gameDisplay.fill(BACKGROUND_COLOR)
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        game_obj.draw_points(game_obj.points)
        game_obj.draw_points(game_obj.get_knot(), "line", 3, color)
        if not pause:
            game_obj.set_points()
        if show_help:
            game_obj.draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)


if __name__ == '__main__':
    main()
