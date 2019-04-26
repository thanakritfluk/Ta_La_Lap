NUMBER_OF_MONSTER = 4


class Player:
    HIT_SPACE = 50

    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.damage = 10

    def plus_damage(self, plus):
        self.damage += plus

    def is_hit(self, coin):
        if coin.center_x - self.HIT_SPACE <= self.x <= coin.center_x + self.HIT_SPACE:
            if coin.center_y - self.HIT_SPACE <= self.y <= coin.center_y + self.HIT_SPACE:
                return True


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
            if self.world.level == NUMBER_OF_MONSTER:
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
        if hit and stage == 0 or stage == 1 and hit:
            if stage == 0:
                self.monster.hp -= self.player.damage
            else:
                self.monster.hp -= self.player.damage * 2
        if stage == -1:
            if hit == 'L':
                self.player.x -= 30
            if hit == 'R':
                self.player.x += 30
