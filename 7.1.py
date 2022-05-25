from classi import *
import unittest

class Test(unittest.TestCase):

    def testalien1(self):
        arena = Arena(500, 500)
        a1 = Alien(arena, 250, 250, 3)

        self.assertEqual(a1.symbol(), (121, 227, 17, 10)) #symbol

    def testalien2(self):
        arena = Arena(500, 500)
        a2 = Alien(arena, 250, 250, 3)

        self.assertEqual(a2.symbol(), (121, 227, 17, 10)) #symbol

    def testrover(self):
        arena = Arena(500, 500)
        r = Rover(arena, 90, 410)

        self.assertEqual(r.position(), (90, 410, 35, 30)) #position

if __name__ == "__main__":
    unittest.main()
