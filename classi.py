import random
import g2d

class Actor():
    '''Interfaccia che deve essere implementata dai vari tipi
       di personaggi del gioco
    '''

    def move(self):
        '''Chiamato da Arena, ad ogni turno del personaggio
        '''
        raise NotImplementedError('Abstract method')

    def collide(self, other: 'Actor'):
        '''Chiamato da Arena, quando il personaggio (self)
           entra in collisione con un altro personaggio (other)
        '''
        raise NotImplementedError('Abstract method')

    def position(self) -> (int, int, int, int):
        '''Restituisce il rettangolo che contiene il personaggio
           tupla di 4 valori interi: (left, top, width, height)
        '''
        raise NotImplementedError('Abstract method')

    def symbol(self) -> (int, int, int, int):
        '''Restituisce la posizione (x, y, w, h) dello sprite corrente,
           se l'immagine è contenuta in una immagine di grandi dimensioni
           altrimenti restituisce la tupla (0, 0, 0, 0)
        '''
        raise NotImplementedError('Abstract method')


class Arena():
    '''Generica 2D game, cui vengono assegnate le dimensioni di gioco
       e che contiene la lista dei personaggi del gioco
    '''

    def __init__(self, width: int, height: int):
        '''Crea una arena con specifica altezza e larghezza
           e lista di personaggi inizialmente vuota
        '''
        self._w, self._h = width, height
        self._actors = []
        self._stop = False

    def add(self, a: Actor):
        '''Aggiunge un personaggio al gioco
           I pesonaggi sono gestiti seguendo il loro ordine di inserimento
        '''
        if a not in self._actors:
            self._actors.append(a)

    def remove(self, a: Actor):
        '''Elimina un personaggio dal gioco
        '''
        if a in self._actors:
            self._actors.remove(a)

    def move_all(self):
        '''chiama il metodo move di ogni personaggio
           dopo aver effettuato il movimento verica
           se è avvenuta un collisione tra il personaggio
           e un altro personaggio e in tal caso chiama
           il metodo collide di entrambi
        '''
        actors = list(reversed(self._actors))
        for a in actors:
            previous_pos = a.position()
            a.move()
            if a.position() != previous_pos:  # inutile per personaggi statici
                for other in actors:
                    # reversed order, so actors drawn on top of others
                    # (towards the end of the cycle) are checked first
                    if other is not a and self.check_collision(a, other):
                        a.collide(other)
                        other.collide(a)

    def check_collision(self, a1: Actor, a2: Actor) -> bool:
        '''Verifica se i due personaggi (parametri) sono in collisione
           (bounding-box collision detection)
        '''
        x1, y1, w1, h1 = a1.position()
        x2, y2, w2, h2 = a2.position()
        return (y2 < y1 + h1 and y1 < y2 + h2
                and x2 < x1 + w1 and x1 < x2 + w2
                and a1 in self._actors and a2 in self._actors)

    def actors(self) -> list:
        '''Restituisce una copia della lista dei personaggi
        '''
        return list(self._actors)

    def size(self) -> (int, int):
        '''Restituisce le dimensioni dell'arena di gioco: (width, height)
        '''
        return (self._w, self._h)

    def stay_all(self):
        for a in self._actors:
            a.stay()

    def stop(self):
        self._stop = True

    def getstop(self):
        return self._stop

class Buche(Actor):
    def __init__(self, arena, x=500):
        self._x = x
        self._y = 399
        self._w1, self._h1 = 20, 20
        self._w2, self._h2 = 30, 40
        self._velocità = -3
        self._arena = arena
        arena.add(self)
        self._dx = self._velocità
        self._dy = 0
        self._bool = bool(random.getrandbits(1))

    def move(self):
        self._x += self._dx
        if self._bool:
            if self._x <= 0 - self._w1:
                self._arena.remove(self)
        else:
            if self._x <= 0 - self._w2:
                self._arena.remove(self)

    def symbol(self):
        if self._bool:
            return 136, 139, 15, 13
        else:
            return 158, 166, 183 - 158, 195 - 166

    def position(self):
        if self._bool:
            return self._x, self._y, self._w1, self._h1
        else:
            return self._x, self._y, self._w2, self._h2

    def collide(self, other):
        if isinstance(other, Rover):
            esplosione = Esplosione(self._arena, other)
            self._arena.remove(other)
            self._arena.stay_all()
            self._arena.stop()

    def stay(self):
        self._dx = 0


class Rover(Actor):

    def __init__(self, arena, x, y):
        self._x, self._y = x, y
        self._w, self._h = 35, 30
        self._speed = 7
        self._dx, self._dy = 0, 0
        self._arena = arena
        self._arena_w, self._arena_h = self._arena.size()
        self._g = 0.4

        arena.add(self)

    def move(self):
        arena_w, arena_h = self._arena.size()
        self._y += self._dy
        self._dy += self._g
        self._x += 0

        if self._y >= self._arena_h - self._h - 98:
            self._y = arena_h - self._h - 98
            self._dy = 0

        if self._x < 0 + self._w - 30:
            self._x = 0 + self._w - 30
        elif self._x > self._arena_w - self._w:
            self._x = self._arena_w - self._w

    def go_left(self):
        self._dx, self._dy = -self._speed, 0

    def go_right(self):
        self._dx, self._dy = +self._speed, 0

    def go_up(self):
        if self._y == self._arena_h - self._h - 98:
            self._dx, self._dy = 0, -self._speed

    def go_down(self):
        self._dx, self._dy = 0, +self._speed

    def stay(self):
        self._dx, self._dy = 0, 0

    def collide(self, other):
        if isinstance(other, Bullet):
            Esplosione(self._arena, self)
            self._arena.remove(self)
            self._arena.stay_all()
            self._arena.stop()

    def position(self):
        return self._x, self._y, self._w, self._h

    def symbol(self):
        if self._dy > 0:
            return 79, 103, 30, 28
        if self._dy < 0:
            return 46, 102, 29, 28
        if self._dy == 0:
            return 211, 157, 32, 24


class Sfondi(Actor):

    def __init__(self, arena, pos: (int, int, int, int), imag: (int, int, int, int), velocità):
        self._x, self._y, self._w, self._h = pos
        self._imagx, self._imagy, self._imagw, self._imagh = imag
        self._velocità = velocità
        self._arena = arena
        self._initx = self._x
        arena.add(self)
        self._dx = velocità
        self._dy = 0

    def move(self):
        self._x += self._dx
        if self._initx - self._x >= 500:
            self._x = self._initx

    def symbol(self):
        return self._imagx, self._imagy, self._imagw, self._imagh

    def position(self):
        return self._x, self._y, self._w, self._h

    def collide(self, other):
        pass

    def stay(self):
        self._dx = 0


class Rocce(Actor):

    def __init__(self, arena, y, choice):

        self._w1, self._h1 = 20, 20
        self._w2, self._h2 = 30, 40
        self._x = 500
        self._y = y
        self._velocità = -3
        self._arena = arena
        arena.add(self)
        self._dx = self._velocità
        self._dy = 0
        self._bool = choice
        self._life = 1

    def move(self):
        self._x += self._dx
        if self._bool:
            if self._x <= 0 - self._w1:
                self._arena.remove(self)
        else:
            if self._x <= 0 - self._w2:
                self._arena.remove(self)

    def symbol(self):
        if self._bool:
            return 62, 208, 10, 10
        else:
            return 94, 200, 16, 18

    def position(self):
        if self._bool:
            return self._x, self._y, self._w1, self._h1
        else:
            return self._x, self._y, self._w2, self._h2

    def collide(self, other):
        if isinstance(other, Rover):
            esplosione = Esplosione(self._arena, other)
            self._arena.remove(other)
            self._arena.stay_all()
            self._arena.stop()
        if isinstance(other, Bullet):
            Esplosione(self._arena, other)
            if not self._bool:
                if self._life == 0:
                    self._arena.remove(self)
                else:
                    self._life -= 1
            else:
                self._arena.remove(self)
            self._arena.remove(other)

    def stay(self):
        self._dx = 0


class Esplosione(Actor):
    def __init__(self, arena, oggetto):
        self._oggetto = oggetto
        self._x, self._y, self._w, self._h = self._oggetto.position()
        self._time = 0
        if isinstance(oggetto, Rover):
            self._dx = 0
        else:
            self._dx = -3
        self._arena = arena
        self._arena.add(self)

    def move(self):

        self._x += self._dx

        if self._time >= 30:
            self._arena.remove(self)

    def symbol(self) -> (int, int, int, int):
        if isinstance(self._oggetto, Rover):
            self._time += 1
            return 213, 102, 42, 29
        else:
            self._time += 1
            return 238, 139, 9, 11

    def collide(self, other):
        pass

    def position(self):
        if isinstance(self._oggetto, Bullet):
            return self._x, self._y-10, 20, 20
        return self._x, self._y, self._w, self._h

    def stay(self):
        self._dx = 0


class Bullet(Actor):
    def __init__(self, arena, x, y, dx, dy):
        self._x = x
        self._y = y
        self._dx = dx
        self._dy = dy
        self._arena = arena
        self._arena.add(self)

    def move(self):
        w, h = self._arena.size()
        if self._x >= w + 5 or self._y <= 0 - 5:
            self._arena.remove(self)
        self._x += self._dx
        self._y += self._dy
        if self._y > 400:
            self._arena.remove(self)
            ran = random.randint(1, 10)
            if ran == 5:
                Buche(self._arena, self._x)

    def symbol(self):
        return 0, 0, 0, 0

    def collide(self, other):
        if isinstance(other, Bullet):
            Esplosione(self._arena, other)
            self._arena.remove(self)

    def stay(self):
        self._dx, self._dy = 0, 0

    def position(self):
        return self._x, self._y, 5, 5


class Alien(Actor):
    def __init__(self, arena, x, y, dx):
        self._x = x
        self._y = y
        self._dx = dx
        self._r = 20
        self._s = 20
        self._arena = arena
        self._arena.add(self)
        
    def move(self):
        self._x += self._dx

        rand = random.randint(1, 10)
        if not self._arena.getstop():

            if rand == 1:
                self._dx = random.choice([-5, 0, 5])

            rand2 = random.randint(1, 60)
            if rand2 == 4:
                Bullet(self._arena, self._x, self._y + self._r, 0, 3)


        if self._x > 500 - self._r:
            self._dx = 0
            self._x = 500 - self._r

        if self._x < 0 + self._s:
            self._dx = 0
            self._x = 0 + self._s

    def symbol(self):
        return 121, 227, 17, 10

    def collide(self, other: 'Actor'):
        if isinstance(other, Bullet):
            Esplosione(self._arena, other)
            self._arena.remove(self)

    def stay(self):
        self._dx, self._dy = 0, 0

    def position(self):
        return self._x, self._y, self._r, self._s
