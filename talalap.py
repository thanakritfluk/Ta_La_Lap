import arcade
from models import World

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 420
FONT_COLOR = arcade.color.WARM_BLACK


class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)

        super().__init__(*args, **kwargs)

    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)

    def draw(self):
        self.sync_with_model()
        super().draw()


class TaLaLapWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, "TaLaLap")
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.plus_dam = arcade.Sprite("images/DoubleDam.png", scale=0.7)
        self.double_dam = arcade.Sprite("images/DoubleDamT.png", scale=0.7)

    def update(self, delta):
        self.world.update(delta)
        self.player = ModelSprite("images/stand.png"
                                  if self.world.player_state == 0
                                  else "images/hit.png",
                                  scale=0.4,
                                  model=self.world.player)
        self.monster = ModelSprite(
            "images/monster/" + str(self.world.monster.monster_folder) + "/" + self.world.monster.monster_stage,
            scale=0.5, model=self.world.monster)

    def display_information(self):
        # arcade.draw_text("Coin: " + str(self.world.coin), self.width - 590, self.height - 60, FONT_COLOR,
        #                  20)
        arcade.draw_text("HP: " + str(self.world.monster.hp), self.width - 590, self.height - 30, FONT_COLOR,
                         20)
        arcade.draw_text("Damage: " + str(self.world.player.damage), self.width - 590, self.height - 410,
                         FONT_COLOR, 20)
        arcade.draw_text("Level: " + str(self.world.world_level), self.width - 350, self.height - 20,
                         FONT_COLOR, 20)

    def on_draw(self):
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2,
                                      SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH,
                                      SCREEN_HEIGHT,
                                      arcade.load_texture("images/bg2.jpg"))
        self.display_information()
        self.monster.draw()
        self.player.draw()

    # def key_action_fight_stage(self):
    #     arcade.play_sound(self.player.hit_sound)
    #     self.monster.delay = -15
    #     self.player.stage = 1
    #     # Check that player hit monster
    #     is_hit = arcade.check_for_collision(self.player.player_sprite, self.monster.monster_sprite)
    #     self.world.on_key_press(self, 0, is_hit)
    #
    # # Check user press left or right in the bonus time stage(-1).
    # def key_action_coin_stage(self, symbol):
    #     if symbol == 65361:
    #         self.world.on_key_press(self, -1, 'L')
    #     if symbol == 65363:
    #         self.world.on_key_press(self, -1, 'R')

    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)

    def on_key_release(self, key, key_modifiers):
        self.world.on_key_release(key, key_modifiers)

    # def press_double_dam(self, x, y):
    #     if 472 <= x <= 526 and 10 <= y <= 60:
    #         return True
    #     else:
    #         return False
    #
    # def press_plus_dam(self, x, y):
    #     if 532 <= x <= 583 and 9 <= y <= 60:
    #         return True
    #     else:
    #         return False
    #
    # def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
    #     if self.press_double_dam(x, y) and self.world.coin >= 100 and self.item_time == 0 and self.stage == 0:
    #         self.world.player.damage *= 2
    #         self.item_time = 100
    #         self.world.coin -= 100
    #     if self.press_plus_dam(x, y) and self.world.coin >= 100 and self.stage == 0:
    #         self.world.player.damage += 10
    #         self.world.coin -= 100


def main():
    window = TaLaLapWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()


if __name__ == '__main__':
    main()
