class Player:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.damage = 50


class Monster:
    def __init__(self, world, x, y, hp):
        self.x = x
        self.y = y
        self.world = world
        self.hp_default = hp
        self.hp = hp

    def update(self, delta):
        if self.hp <= 0:
            self.world.hp_level += 1
            if self.world.level == 2:
                self.world.level = 1
            else:
                self.world.level += 1
            self.hp = self.hp_default * self.world.hp_level


class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.player = Player(self, width // 2, height // 3)
        self.monster = Monster(self, width // 2, height - 130, 100)
        self.coin = 0
        self.hp_level = 1
        self.level = 1

    def update(self, delta):
        self.monster.update(delta)

    def on_key_press(self, symbol: int, stage, hit):
        if hit and stage == 0:
            self.monster.hp -= self.player.damage
        if stage == -1:
            if hit == 'L':
                self.player.x -= 20
            if hit == 'R':
                self.player.x += 20
