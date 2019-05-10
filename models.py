import arcade
from random import randint


class Monster:
    DELAY_TIME = 0
    MONSTER_FOLDER = 4
    LIST_MONSTER = ["1.png", "2.png",
                    "3.png", "4.png",
                    "5.png", "6.png",
                    "7.png", "8.png",
                    "9.png", "10.png"]

    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.hp = 100
        self.hp_default = self.hp
        self.monster_folder = 1
        self.current_frame = 0
        self.monster_frame = self.LIST_MONSTER[0]
        self.attacked = False

    def update(self, delta):
        self.DELAY_TIME += 1
        if self.DELAY_TIME == 3:
            if not self.attacked:
                self.current_frame += 1
                self.DELAY_TIME = 0
                if self.current_frame < 9:
                    self.monster_frame = self.LIST_MONSTER[self.current_frame]
                else:
                    self.current_frame = 0
            elif self.attacked:
                self.monster_frame = self.LIST_MONSTER[9]
                self.DELAY_TIME = -5
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
    MOVE_SPEED = 20

    def __init__(self, world, x, y):
        self.world = world
        self.player_frame = 0
        self.x = x
        self.y = y
        self.damage = 10

    def set_stand_frame(self):
        self.player_frame = 0

    def set_hit_frame(self):
        arcade.play_sound(arcade.load_sound("sound/hit.wav"))
        self.player_frame = 1

    def plus_damage(self, plus):
        self.damage += plus

    def is_hit_coin(self, coin):
        if coin.center_x - self.HIT_SPACE <= self.x <= coin.center_x + self.HIT_SPACE:
            if coin.center_y - self.HIT_SPACE <= self.y <= coin.center_y + self.HIT_SPACE:
                return True

    def is_hit_monster(self, player, monster):
        return arcade.check_for_collision(player, monster)

    def move_left(self):
        self.x -= self.MOVE_SPEED

    def move_right(self):
        self.x += self.MOVE_SPEED

    def set_init_position(self):
        self.x = self.world.width // 2


class ITEM:
    DELAY_TIME = 20

    def __init__(self, world):
        self.world = world
        self.count_delay = 0
        self.item_time = 0

    def press_double_dam(self, x, y):
        if 472 <= x <= 526 and 10 <= y <= 60:
            if self.world.coin >= 50 and self.item_time == 0 and self.world.on_fight_stage():
                self.world.player.damage *= 2
                self.item_time = 10
                self.world.coin -= 50

    def press_plus_dam(self, x, y):
        if 532 <= x <= 583 and 9 <= y <= 60:
            if self.world.coin >= 100 and self.world.on_fight_stage():
                self.world.player.damage += 10
                self.world.coin -= 100

    def update(self):
        if self.item_time > 0 and self.world.on_fight_stage():
            if self.item_time == 1:
                self.world.player.damage //= 2
                self.item_time = 0
            self.count_delay += 1
            if self.count_delay == self.DELAY_TIME:
                self.item_time -= 1
                self.count_delay = 0


class Coin:
    NUMBER_OF_COIN = 5

    def __init__(self, world):
        self.world = world
        self.coin = arcade.SpriteList()

    def random_coin_list(self):
        for i in range(self.NUMBER_OF_COIN):
            coin = arcade.Sprite("images/coin.png", 0.09)
            coin.center_x = randint(20, self.world.width)
            coin.center_y = randint(self.world.height - 100, self.world.height)
            self.coin.append(coin)

    def is_empty_list(self):
        return not self.coin

    def update(self):
        for coin in self.coin:
            coin.center_y -= 1
            if coin.center_y < 0:
                coin.kill()
            if self.world.player.is_hit_coin(coin):
                arcade.play_sound(arcade.load_sound("sound/coins.wav"))
                coin.kill()
                self.world.coin += randint(10, 60)


class World:
    DELAY_TIME = 15

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.player = Player(self, self.width // 2, self.height // 3)
        self.item = ITEM(self)
        self.monster = Monster(self, self.width // 2, self.height - 130)
        self.coin_list = Coin(self)
        self.coin = 50
        # World level define the hp of monster too.
        self.end_text = ""
        self.desc = ""
        self.world_level = 1
        self.world_stage = "Fight"
        self.stage_time = 20
        self.count_delay = 0

    def check_change_to_coin_stage(self):
        if self.monster.hp <= self.player.damage:
            self.world_level += 1
            self.coin_list.random_coin_list()
            self.world_stage = "Coin"
            self.stage_time = 20

    def check_change_to_fight_stage(self):
        if self.coin_list.is_empty_list():
            self.world_stage = "Fight"
            self.player.set_init_position()

    def on_fight_stage(self):
        return self.world_stage == "Fight"

    def on_coin_stage(self):
        return self.world_stage == "Coin"

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.ENTER and self.on_fight_stage() and self.end_text == "Game Over":
            self.end_text = ""
            self.desc = ""
            self.set_start_stage()
        if key == arcade.key.SPACE and self.on_fight_stage() and self.end_text == "":
            self.check_change_to_coin_stage()
            self.player.set_hit_frame()
            self.monster.attack_effect(self.player.damage, self.world_level)
        if self.on_coin_stage():
            if key == arcade.key.LEFT:
                self.player.move_left()
            if key == arcade.key.RIGHT:
                self.player.move_right()

    def on_key_release(self, key, key_modifiers):
        self.player.set_stand_frame()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.item.press_plus_dam(x, y)
        self.item.press_double_dam(x, y)

    def set_start_stage(self):
        self.coin = 50
        self.world_level = 1
        self.monster.hp = 100
        self.world_stage = "Fight"
        self.stage_time = 20
        self.monster.monster_folder = 1
        self.player.damage = 10

    def update(self, delta):
        if self.on_fight_stage():
            if self.stage_time <= 0:
                self.end_text = "Game Over"
                self.desc = "Press ENTER to try again"
            else:
                self.count_delay += 1
            if self.stage_time >= 0 and self.DELAY_TIME == self.count_delay:
                self.stage_time -= 1
                self.count_delay = 0

        self.check_change_to_fight_stage()
        self.monster.update(delta)
        self.coin_list.update()
        self.item.update()
