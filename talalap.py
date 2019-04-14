import arcade
from models import World
import random

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 420
MONSTER_IMG = ["1.png", "2.png", "3.png", "4.png", "5.png", "6.png", "7.png", "8.png", "9.png", "10.png"]
PLAYER_IMG = ["images/P_Set.png", "images/P_Hit.png"]


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


class PlayerSprite:
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
    def __init__(self, width, height):
        super().__init__(width, height, "TaLaLap")
        arcade.set_background_color(arcade.color.WHITE)
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.player = PlayerSprite()
        self.background = arcade.load_texture("images/bg.png")
        self.monster = MonsterSprite()
        self.coin_list = arcade.SpriteList()
        for i in range(5):
            coin = arcade.Sprite("images/coin.png", 0.09)
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)
            self.coin_list.append(coin)

    def on_draw(self):
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.monster.draw(self.world.monster.x, self.world.monster.y)
        self.player.draw(self.world.player.x, self.world.player.y)
        # self.coin_list.draw()
        # Display information
        arcade.draw_text("Coin: " + str(self.world.coin), self.width - 100, self.height - 30, arcade.color.BLACK, 20)
        arcade.draw_text("HP: " + str(self.world.monster.hp), self.width - 580, self.height - 30, arcade.color.BLACK,
                         20)
        arcade.draw_text("Damage: " + str(self.world.player.damage), self.width - 580, self.height - 400,
                         arcade.color.BLACK, 20)
        arcade.draw_text("Level: " + str(self.world.hp_level), self.width - 340, self.height -20,
                         arcade.color.BLACK, 20)

    def update(self, delta):
        # Update animation for monster.
        if self.monster.stage != 9:
            self.monster.update(self.monster.stage + 1)
        else:
            self.monster.stage = 0
        # Update monster level
        self.monster.level = self.world.level
        # Update coin when hit.
        self.coin_list.update()
        coin_hit_list = arcade.check_for_collision_with_list(self.player.player_sprite, self.coin_list)
        for coin in coin_hit_list:
            coin.kill()
            self.world.coin += 5
        self.world.update(delta)

    def on_key_press(self, symbol: int, modifiers: int):
        # Check user press space bar key.
        if symbol == 32:
            arcade.play_sound(self.player.hit_sound)
            self.monster.delay = -15
            self.player.stage = 1
            self.world.on_key_press(self, symbol)
            print(arcade.check_for_collision(self.player.player_sprite, self.monster.monster_sprite))

    def on_key_release(self, symbol: int, modifiers: int):
        self.player.stage = 0


def main():
    window = TaLaLapWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()


if __name__ == '__main__':
    main()
