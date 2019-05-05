import arcade


class Monster:
    DELAY_TIME = 0
    MONSTER_FOLDER = 4
    LIST_MONSTER = ["1.png", "2.png", "3.png", "4.png", "5.png", "6.png", "7.png", "8.png", "9.png", "10.png"]

    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.count = 0
        self.attacked = False
        self.monster_folder = 1
        self.monster_stage = self.LIST_MONSTER[0]
        self.hp = 100
        self.hp_default = self.hp

    def update(self, delta):
        print(self.world.height)
        self.DELAY_TIME += 1
        if self.DELAY_TIME == 3:
            if not self.attacked:
                self.count += 1
                self.DELAY_TIME = 0
                if self.count < 9:
                    self.monster_stage = self.LIST_MONSTER[self.count]
                else:
                    self.count = 0
            elif self.attacked:
                self.monster_stage = self.LIST_MONSTER[9]
                self.DELAY_TIME = -10
                self.attacked = False

    def fight_position(self):
        self.y = self.world.height - 130

    def coin_position(self):
        self.y = 1000

    def is_dead(self):
        return self.hp <= 0

    def set_new_lv_hp(self, hp):
        self.hp = hp

    def monster_level_change(self, world_level):
        if self.is_dead():
            self.set_new_lv_hp(world_level * 100)
            if self.monster_folder < self.MONSTER_FOLDER:
                self.monster_folder += 1
            else:
                self.monster_folder = 1

    def attack_effect(self, damage, world_level):
        self.attacked = True
        self.hp -= damage
        self.monster_level_change(world_level)


class Player:
    HIT_SPACE = 50
    MOVE_SPACE = 5

    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.damage = 10

    def plus_damage(self, plus):
        self.damage += plus

    def is_hit_coin(self, coin):
        if coin.center_x - self.HIT_SPACE <= self.x <= coin.center_x + self.HIT_SPACE:
            if coin.center_y - self.HIT_SPACE <= self.y <= coin.center_y + self.HIT_SPACE:
                return True

    def is_hit_monster(self, player, monster):
        return arcade.check_for_collision(player, monster)

    def move_left(self):
        self.x -= self.MOVE_SPACE

    def move_right(self):
        self.x += self.MOVE_SPACE

    def update(self, delta):
        pass


class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.player = Player(self, self.width // 2, self.height // 3)
        self.monster = Monster(self, self.width // 2, self.height - 130)
        self.player_state = 0
        # World level define the hp of monster too.
        self.world_level = 1
        self.world_stage = "Fight"

    def check_change_world_level(self):
        if self.monster.hp <= self.player.damage:
            self.world_level += 1

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.SPACE and self.world_stage == "Fight":
            self.check_change_world_level()
            self.player_state = 1
            self.monster.attack_effect(self.player.damage, self.world_level)
        if self.world_stage == "Coin":
            if key == arcade.key.LEFT:
                self.player.move_left()
            if key == arcade.key.RIGHT:
                self.player.move_right()

    def on_key_release(self, key, key_modifiers):
        self.player_state = 0

    def update(self, delta):
        self.player.update(delta)
        self.monster.update(delta)
