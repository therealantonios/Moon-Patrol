from classi import *
import random
import g2d
from time import time
import os


class MoonPatrolGame():

    def __init__(self):
        self._arena = Arena(500, 500)
        self._g1 = Sfondi(self._arena, (0, 230, 500, 270), (0, 258, 512, 130), -1)  # sfondo collina1
        self._g2 = Sfondi(self._arena, (500, 230, 500, 270), (0, 258, 512, 130), -1)  # sfondo collina2
        self._s1 = Sfondi(self._arena, (0, 400, 500, 100), (0, 513, 512, 125), -3)  # sfondo terra1
        self._s2 = Sfondi(self._arena, (500, 400, 500, 100), (0, 513, 512, 125), -3)  # sfondo terra2
        self._r = Rover(self._arena, 90, 410)  # rover
        if os.path.isfile("config.txt"):
            with open("config.txt", "r") as myfile:
                for i in myfile:
                    if i.startswith("alien"):
                        i = i.strip()
                        self._num = int(i[-1])
        else:
            with open("config.txt", "w") as myfile:
                myfile.write("alien: 2")
                self._num = 2

        for i in range (0, self._num):
            Alien(self._arena, random.randint(0,500), 250, 3)
        self._start = time()
        self._playtime = 60
        self._bucacont = 0
        self._roccecont = 0

    def arena(self):
        return self._arena

    def rover(self):
        return self._r

    def Buche(self):
        if random.randint(0, 50) == 0 and self._bucacont >= 30 and self._arena.getstop() is False and self._roccecont >= 30:
            Buche(self._arena)
            self._bucacont = 0
        self._bucacont += 1

    def Rocce(self):
        a = random.randint(0, 50)
        if a == 0 and self._roccecont >= 30 and self._arena.getstop() is False and self._bucacont >= 30:
            choice = bool(random.getrandbits(1))
            self._roccecont = 0
            if choice:
                Rocce(self._arena, 400 - 10, choice)
            else:
                Rocce(self._arena, 400 - 30, choice)
        self._roccecont += 1

    def game_over(self) -> bool:
        return self._r not in self._arena.actors()

    def game_won(self) -> bool:
        return time() - self._start > self._playtime

    def remaining_time(self) -> int:
        return int(self._start + self._playtime - time())


class MoonPatrolGui():

    def __init__(self):
        self._game = MoonPatrolGame()
        g2d.init_canvas(self._game.arena().size())
        self._sprites = g2d.load_image("moon_patrol.png")
        self._sfondi = g2d.load_image("moon_patrol_bg.png")
        g2d.main_loop(self.tick)

    def handle_keyboard(self):
        rover = self._game.rover()
        x, y, w, h = rover.position()
        if g2d.key_pressed("ArrowUp"):
            rover.go_up()

        if g2d.key_released("ArrowUp"):
            rover.stay()

        if g2d.key_pressed('Spacebar'):
            Bullet(self._game.arena(), x + 1 / 4 * w, y, 0, -12)
            Bullet(self._game.arena(), x + w, y + 1 / 2 * h, 12, 0)

    def tick(self):

        arena = self._game.arena()
        arena.move_all()
        g2d.clear_canvas()
        g2d.draw_image_clip(self._sfondi, (0, 0, 512, 218), (0, 0, 500, 500))  # cielo fermo
        self.drawimage()
        self.handle_keyboard()
        self._game.Buche()
        self._game.Rocce()
        toplay = "Time: " + str(self._game.remaining_time())
        g2d.draw_text(toplay, (0, 0), 24)

        if self._game.game_over():
            g2d.alert("Game over")
            g2d.close_canvas()
        elif self._game.game_won():
            g2d.alert("Game won")
            g2d.close_canvas()

    def drawimage(self):
        arena = self._game.arena()
        for a in arena.actors():
            if a.symbol() != (0, 0, 0, 0):
                if isinstance(a, Sfondi):
                    g2d.draw_image_clip(self._sfondi, a.symbol(), a.position())
                else:
                    g2d.draw_image_clip(self._sprites, a.symbol(), a.position())
            else:
                g2d.fill_rect(a.position())


gui = MoonPatrolGui()
