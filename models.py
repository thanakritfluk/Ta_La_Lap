class Player:

    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.hit = False
        self.damage = 5

    def update(self, delta):
        return

    def hit(self):
        self.hit = True


class Monster:
    def __init__(self, world, x, y, hp):
        self.x = x
        self.y = y
        self.world = world
        self.hp = hp

    def update(self, delta):
        print(self.x)
        if self.x != 0:
            self.x -= 2
        else:
            self.x += 2

    def attacked(self, player):
        return


class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.player = Player(self, width // 2, height // 3)
        self.monster = Monster(self, width // 2, height // 2, 100)
        self.coin = 0

    def update(self, delta):
        self.player.update(delta)
        self.monster.update(delta)

    def on_key_press(self, key, key_modifiers):
        self.monster.hp -= self.player.damage
