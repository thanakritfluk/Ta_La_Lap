import arcade
from models import World
import random

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 420
FONT_COLOR = arcade.color.WARM_BLACK
MONSTER_IMG = ["1.png", "2.png", "3.png", "4.png", "5.png", "6.png", "7.png", "8.png", "9.png", "10.png"]
PLAYER_IMG = ["images/stand.png", "images/hit.png"]


# ["images/P_Set.png", "images/P_Hit.png"]

class MonsterSprite:
    DELAY_TIME = 8

    def __init__(self):
        self.delay = 0
        self.stage = 0
        self.level = 1
        self.monster_sprite = arcade.Sprite("images/monster/" + str(self.level) + "/" + MONSTER_IMG[self.stage],
                                            scale=0.5)

    def draw(self, x, y):
        if self.delay < 0:
            self.monster_sprite = arcade.Sprite("images/monster/" + str(self.level) + "/" + MONSTER_IMG[9], scale=0.5)
        else:
            self.monster_sprite = arcade.Sprite("images/monster/" + str(self.level) + "/" + MONSTER_IMG[self.stage],
                                                scale=0.5)
        self.monster_sprite.set_position(x, y)
        self.monster_sprite.draw()

    def update(self, stage):
        self.delay += 1
        if self.delay == MonsterSprite.DELAY_TIME:
            self.delay = 0
            self.stage = stage


class PlayerSprite():
    def __init__(self):
        self.stage = 0
        self.hit_sound = arcade.load_sound("sound/hit.wav")
        self.player_sprite = arcade.Sprite(PLAYER_IMG[self.stage], scale=0.4)

    def draw(self, x, y):
        self.player_sprite = arcade.Sprite(PLAYER_IMG[self.stage], scale=0.4)
        self.player_sprite.set_position(x, y)
        self.player_sprite.draw()

    def update(self, stage):
        self.stage = stage


class TaLaLapWindow(arcade.Window):
    COIN_DELAY_TIME = 20
    NUMBER_COIN = 5
    COIN_VELOCITY = 2

    def __init__(self, width, height):
        super().__init__(width, height, "TaLaLap")
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.background = arcade.load_texture("images/bg2.jpg")
        self.player = PlayerSprite()
        self.monster = MonsterSprite()
        self.plus_dam = arcade.Sprite("images/DoubleDam.png", 0.7)
        self.double_dam = arcade.Sprite("images/DoubleDamT.png", 0.7)
        self.stage = 0
        self.coin_list = arcade.SpriteList()
        self.random_coin_list()
        self.coin_delay = 0
        self.item_time = 0

    def random_coin_list(self):
        for i in range(self.NUMBER_COIN):
            coin = arcade.Sprite("images/coin.png", 0.09)
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randint(SCREEN_HEIGHT - 100, SCREEN_HEIGHT)
            self.coin_list.append(coin)

    # Display information
    def display_information(self):
        arcade.draw_text("Coin: " + str(self.world.coin), self.width - 590, self.height - 60, FONT_COLOR,
                         20)
        arcade.draw_text("HP: " + str(self.world.monster.hp), self.width - 590, self.height - 30, FONT_COLOR,
                         20)
        arcade.draw_text("Damage: " + str(self.world.player.damage), self.width - 590, self.height - 410,
                         FONT_COLOR, 20)
        arcade.draw_text("Level: " + str(self.world.hp_level), self.width - 350, self.height - 20,
                         FONT_COLOR, 20)

    def draw_coin(self):
        # Draw coin with the velocity -1.
        if self.coin_delay == self.COIN_DELAY_TIME:
            for coin in self.coin_list:
                if coin.center_y < 0:
                    coin.kill()
                coin.center_y -= self.COIN_VELOCITY
            self.coin_list.draw()
        else:
            self.coin_delay += 1

    def on_draw(self):
        self.plus_dam.set_position(SCREEN_WIDTH - 40, SCREEN_HEIGHT - 385)
        self.double_dam.set_position(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 385)
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        if self.item_time != 0:
            arcade.draw_text("Item time: " + str(self.item_time), self.width - 590, self.height - 90, FONT_COLOR,
                             20)
        self.plus_dam.draw()
        self.double_dam.draw()
        if self.stage == -1:
            self.draw_coin()
        self.monster.draw(self.world.monster.x, self.world.monster.y)
        self.player.draw(self.world.player.x, self.world.player.y)
        self.display_information()

    def fight_stage(self):
        # Check monster hp before can access the bonus time stage(-1).
        if self.world.monster.hp <= 0:
            self.stage = -1
            self.world.monster.y = 1000
        # Update animation for monster.
        if self.monster.stage != len(MONSTER_IMG) - 1:
            self.monster.update(self.monster.stage + 1)
        else:
            self.monster.stage = 0
        # Check if the items is used.
        if self.item_time != 0:
            self.item_time -= 1
            if self.item_time == 1:
                self.world.player.damage = self.world.player.damage // 2
        # Update monster level
        self.monster.level = self.world.level

    def coin_stage(self):
        # Update coin when hit.
        self.coin_list.update()
        coin_hit_list = []
        for coin in self.coin_list:
            if self.world.player.is_hit(coin):
                coin_hit_list.append(coin)
        for coin in coin_hit_list:
            sound = arcade.load_sound("sound/coins.wav")
            arcade.play_sound(sound)
            coin.kill()
            self.world.coin += 5 * 2 + (self.world.level - 1)
        # Check is coin list is empty before turn to fight stage(0).
        if not self.coin_list:
            self.stage = 0
            self.world.monster.y = SCREEN_HEIGHT - 130
            self.random_coin_list()
            self.world.player.x = SCREEN_WIDTH // 2

    def update(self, delta):
        if self.stage == 0:
            self.fight_stage()
        else:
            self.coin_stage()
        self.world.update(delta)

    def key_action_fight_stage(self):
        arcade.play_sound(self.player.hit_sound)
        self.monster.delay = -15
        self.player.stage = 1
        # Check that player hit monster
        is_hit = arcade.check_for_collision(self.player.player_sprite, self.monster.monster_sprite)
        self.world.on_key_press(self, 0, is_hit)

    # Check user press left or right in the bonus time stage(-1).
    def key_action_coin_stage(self, symbol):
        if symbol == 65361:
            self.world.on_key_press(self, -1, 'L')
        if symbol == 65363:
            self.world.on_key_press(self, -1, 'R')

    def on_key_press(self, symbol: int, modifiers: int):
        # Check user press space bar key in the fight stage(0).
        if symbol == 32 and self.stage == 0:
            self.key_action_fight_stage()
        if self.stage == -1:
            self.key_action_coin_stage(symbol)

    def on_key_release(self, symbol: int, modifiers: int):
        self.player.stage = 0

    def press_double_dam(self, x, y):
        if 472 <= x <= 526 and 10 <= y <= 60:
            return True
        else:
            return False

    def press_plus_dam(self, x, y):
        if 532 <= x <= 583 and 9 <= y <= 60:
            return True
        else:
            return False

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if self.press_double_dam(x, y) and self.world.coin >= 100 and self.item_time == 0 and self.stage == 0:
            self.world.player.damage *= 2
            self.item_time = 100
            self.world.coin -= 100
        if self.press_plus_dam(x, y) and self.world.coin >= 100 and self.stage == 0:
            self.world.player.damage += 10
            self.world.coin -= 100


def main():
    window = TaLaLapWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()


if __name__ == '__main__':
    main()
