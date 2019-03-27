import arcade
from models import World

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600


class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)
        super().__init__(*args)

    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)

    def draw(self):
        self.sync_with_model()
        super().draw()


class TaLaLapWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.WHITE)
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.player = ModelSprite('images/Player100x141.png', model=self.world.player)
        self.background = arcade.load_texture("images/bg.png")
        self.monster = ModelSprite('images/monster.png', model=self.world.monster)

    def on_draw(self):
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.monster.draw()
        self.player.draw()
        arcade.draw_text("Coin: "+str(self.world.coin), self.width - 120, self.height - 30, arcade.color.BLACK, 20)
        arcade.draw_text("HP: " + str(self.world.monster.hp), self.width - 550, self.height - 30, arcade.color.BLACK, 20)

    def update(self, delta):
        self.world.update(delta)


def main():
    window = TaLaLapWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()


if __name__ == '__main__':
    main()
