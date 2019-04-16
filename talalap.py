import arcade
from models import World
import random

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 420
FONT_COLOR = arcade.color.WARM_BLACK
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
    BONUS_TIME = 10
    COIN_DELAY_TIME = 20

    def __init__(self, width, height):
        super().__init__(width, height, "TaLaLap")
        arcade.set_background_color(arcade.color.WHITE)
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.player = PlayerSprite()
        self.background = arcade.load_texture("images/bg2.jpg")
        self.monster = MonsterSprite()
        self.stage = 0
        self.bonus_time = 0
        self.coin_list = arcade.SpriteList()
        self.random_coin_list()
        self.coin_delay = 0

    def random_coin_list(self):
        for i in range(5):
            coin = arcade.Sprite("images/coin.png", 0.09)
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randint(SCREEN_HEIGHT - 100, SCREEN_HEIGHT)
            self.coin_list.append(coin)

    def on_draw(self):
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        if self.stage == -1:
            # Draw coin with the velocity -1.
            if self.coin_delay == self.COIN_DELAY_TIME:
                for coin in self.coin_list:
                    if coin.center_y < 0:
                        coin.kill()
                    coin.center_y -= 1
                self.coin_list.draw()
            else:
                self.coin_delay += 1

        self.monster.draw(self.world.monster.x, self.world.monster.y)
        self.player.draw(self.world.player.x, self.world.player.y)

        # Display information
        arcade.draw_text("Coin: " + str(self.world.coin), self.width - 590, self.height - 60, FONT_COLOR,
                         20)
        arcade.draw_text("HP: " + str(self.world.monster.hp), self.width - 590, self.height - 30, FONT_COLOR,
                         20)
        arcade.draw_text("Damage: " + str(self.world.player.damage), self.width - 590, self.height - 410,
                         FONT_COLOR, 20)
        arcade.draw_text("Level: " + str(self.world.hp_level), self.width - 350, self.height - 20,
                         FONT_COLOR, 20)

    def update(self, delta):
        if self.stage == 0:
            # Check monster hp before can access the bonus time stage(-1).
            if self.world.monster.hp <= 0:
                self.stage = -1
                self.world.monster.y = 1000
            # Update animation for monster.
            if self.monster.stage != 9:
                self.monster.update(self.monster.stage + 1)
            else:
                self.monster.stage = 0
            # Update monster level
            self.monster.level = self.world.level
        else:
            # Update coin when hit.
            self.coin_list.update()
            coin_hit_list = arcade.check_for_collision_with_list(self.player.player_sprite, self.coin_list)
            for coin in coin_hit_list:
                coin.kill()
                self.world.coin += 5
            # Check is coin list is empty before turn to fight stage(0).
            if not self.coin_list:
                self.stage = 0
                self.world.monster.y = SCREEN_HEIGHT - 130
                self.random_coin_list()
                self.world.player.x = SCREEN_WIDTH // 2
        self.world.update(delta)

    def on_key_press(self, symbol: int, modifiers: int):
        # Check user press space bar key in the fight stage(0).
        if symbol == 32 and self.stage == 0:
            arcade.play_sound(self.player.hit_sound)
            self.monster.delay = -15
            self.player.stage = 1
            # Check that player hit monster
            is_hit = arcade.check_for_collision(self.player.player_sprite, self.monster.monster_sprite)
            self.world.on_key_press(self, 0, is_hit)
        # Check user press left or right in the bonus time stage(-1).
        if self.stage == -1:
            if symbol == 65361:
                self.world.on_key_press(self, -1, 'L')
            if symbol == 65363:
                self.world.on_key_press(self, -1, 'R')

    def on_key_release(self, symbol: int, modifiers: int):
        self.player.stage = 0


def main():
    window = TaLaLapWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()


if __name__ == '__main__':
    main()
