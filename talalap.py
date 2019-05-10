import arcade
from models import World

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 420


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
        self.font_color = arcade.color.WARM_BLACK
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.coin_list = self.world.coin_list
        self.plus_dam = arcade.Sprite("images/DoubleDam.png", scale=0.7)
        self.double_dam = arcade.Sprite("images/DoubleDamT.png", scale=0.7)
        self.plus_dam.set_position(SCREEN_WIDTH - 40, SCREEN_HEIGHT - 385)
        self.double_dam.set_position(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 385)

    def update(self, delta):
        self.world.update(delta)
        self.player = ModelSprite("images/stand.png"
                                  if self.world.player.player_frame == 0
                                  else "images/hit.png",
                                  scale=0.4,
                                  model=self.world.player)
        self.monster = ModelSprite(
            "images/monster/" + str(self.world.monster.monster_folder) + "/" + self.world.monster.monster_frame,
            scale=0.5, model=self.world.monster)

    def display_information(self):
        arcade.draw_text("Coin: " + str(self.world.coin), self.width - 590, self.height - 60, self.font_color,
                         20)
        arcade.draw_text("HP: " + str(self.world.monster.hp), self.width - 590, self.height - 30, self.font_color,
                         20)
        arcade.draw_text("Damage: " + str(self.world.player.damage), self.width - 590, self.height - 410,
                         self.font_color, 20)
        arcade.draw_text("Level: " + str(self.world.world_level), self.width - 350, self.height - 20,
                         self.font_color, 20)
        arcade.draw_text(self.world.end_text, self.width // 3.65, self.height // 2 + 50, color=arcade.color.ORANGE_RED,
                         font_size=50, bold=2)
        arcade.draw_text(self.world.desc, self.width // 2.85, self.height // 2.35 + 50, color=arcade.color.WHITE_SMOKE,
                         font_size=15, bold=2)
        if self.world.item.item_time > 0:
            arcade.draw_text("Item_time: " + str(self.world.item.item_time), self.width - 590, self.height - 90,
                             self.font_color,
                             20)
        if self.world.world_stage == "Fight":
            arcade.draw_text("Time: " + str(self.world.stage_time), self.width - 108, self.height - 20,
                             self.font_color, 20)

    def on_draw(self):
        if self.world.stage_time <= 0:
            arcade.draw_rectangle_filled(SCREEN_WIDTH // 2,
                                         SCREEN_HEIGHT // 2,
                                         SCREEN_WIDTH,
                                         SCREEN_HEIGHT,
                                         arcade.color.BLACK)
        else:
            arcade.draw_texture_rectangle(SCREEN_WIDTH // 2,
                                          SCREEN_HEIGHT // 2,
                                          SCREEN_WIDTH,
                                          SCREEN_HEIGHT,
                                          arcade.load_texture("images/bg2.jpg"))

        if self.world.on_fight_stage():
            if self.world.end_text == "":
                self.monster.draw()
                self.double_dam.draw()
                self.plus_dam.draw()
            elif self.world.end_text == "Game Over":
                self.font_color = arcade.color.BLACK
        else:
            self.coin_list.coin.draw()
        self.player.draw()

        self.display_information()

    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)

    def on_key_release(self, key, key_modifiers):
        self.world.on_key_release(key, key_modifiers)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.world.on_mouse_press(x, y, button, modifiers)


def main():
    window = TaLaLapWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()


if __name__ == '__main__':
    main()
