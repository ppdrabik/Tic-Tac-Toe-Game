import arcade
import random
import time

class Sprite(arcade.Sprite):
    # Class attributes
    SCALE = 0.2

    # Constructor initializes an instance of the Sprite class with the variables: name, spirit_path_texture
    def __init__(self, name, spirit_path_texture):
        # Constructor initialize parent class with variables: spirit_path_texture, scale
        super().__init__(spirit_path_texture, scale=self.SCALE)
        # Instance attributes
        self.name = name
        self.filename = spirit_path_texture

    # Class methods
    def sprite_set_position(self, x_min, y_max):
        self.center_x = x_min + 100
        self.center_y = y_max - 100

    def sprite_draw(self):
        self.draw()


class GameWindow(arcade.Window):
    MAX_WIDTH = 800
    MAX_HEIGHT = 800

    def __init__(self):
        super().__init__(self.MAX_WIDTH, self.MAX_HEIGHT, "My Arcade Game")


class GameScreen(arcade.View, GameWindow):
    # Consts for grid
    MARGIN = 100
    ROW = 3
    COLUMN = 3
    ROW_SIZE = (GameWindow.MAX_WIDTH - 2 * MARGIN) / 3
    COLUMN_SIZE = (GameWindow.MAX_HEIGHT - 2 * MARGIN) / 3

    # Lines for grid
    VERTICAL_LINES = [
        {"x": MARGIN, "start_y": MARGIN, "end_y": GameWindow.MAX_HEIGHT - MARGIN},
        {"x": MARGIN + ROW_SIZE, "start_y": MARGIN, "end_y": GameWindow.MAX_HEIGHT - MARGIN},
        {"x": MARGIN + 2 * ROW_SIZE, "start_y": MARGIN, "end_y": GameWindow.MAX_HEIGHT - MARGIN},
        {"x": MARGIN + 3 * ROW_SIZE, "start_y": MARGIN, "end_y": GameWindow.MAX_HEIGHT - MARGIN},
    ]

    HORIZONTAL_LINES = [
        {"start_x": MARGIN, "end_x": GameWindow.MAX_HEIGHT - MARGIN, "y": MARGIN},
        {"start_x": MARGIN, "end_x": GameWindow.MAX_HEIGHT - MARGIN, "y": MARGIN + ROW_SIZE},
        {"start_x": MARGIN, "end_x": GameWindow.MAX_HEIGHT - MARGIN, "y": MARGIN + 2 * ROW_SIZE},
        {"start_x": MARGIN, "end_x": GameWindow.MAX_HEIGHT - MARGIN, "y": MARGIN + 3 * ROW_SIZE},
    ]

    # List of coordinates of all 9 grid field
    coordinates = (
        # x_min, x_max, y_min, y_max
        (100, 300, 100, 300),
        (300, 500, 100, 300),
        (500, 700, 100, 300),
        (100, 300, 300, 500),
        (300, 500, 300, 500),
        (500, 700, 300, 500),
        (100, 300, 500, 700),
        (300, 500, 500, 700),
        (500, 700, 500, 700),
    )

    # Instance variable
    def __init__(self):
        super().__init__()
        # ================
        # ==== Colors ====
        # ================
        self.background_color = (30, 31, 34)
        self.horizontal_line_color = (49, 52, 56)
        self.vertical_line_color = self.horizontal_line_color
        self.animation_line_color = (219, 50, 77)
        self.hover_color = arcade.csscolor.DARK_GREEN
        self.turn_text_color = arcade.color.WHITE

        # ================
        # ==== Grid ====
        # ================
        # List for storing game progress
        # It is filled during game 0 - O, 1 - X
        # [0] [1] [2]
        # [6, 7, 8]  [0]
        # [3, 4, 5]  [1]
        # [0, 1, 2]  [2]
        self.game_pole = [[10, 34, 21], [44, 32, 41], [34, 31, 39]]

        # Stores current game pole number (0 to 8)
        self.hover_index = None

        self.row = None
        self.column = None

        # ================
        # === Animation ===
        # ================
        # Current distance of line animation, start at 200 to 800
        self.distance = 200
        self.animation_end = None

        # ================
        # === Sprites ===
        # ================
        self.texture_path = None

        # Flag variable for drawing sprite
        self.draw_sprite = None

        # Stores sprites, only for drawing
        self.sprite_x_list = []

        # ================
        # === Game Logic ===
        # ================
        # To determine whose next turn is
        self.players_list = ["X", "O"]

        # First turn is random
        self.whose_turn = random.choice(self.players_list)
        self.turn = arcade.Text(f"Turn: {self.whose_turn}", 350, 750, self.turn_text_color, 16)

        self.win = None

        # For blocking mouse movement after Game Over
        self.mouse_state_move = None
        self.mouse_state_click = None

    # ======================= Custom functions ========================================
    def which_row_and_column(self):
        if self.hover_index in range(0, 3):
            self.row = 2
            self.column = self.hover_index
        elif self.hover_index in range(3, 6):
            self.row = 1
            self.column = self.hover_index - 3
        else:
            self.row = 0
            self.column = self.hover_index - 6

    def check_horizontal(self):
        if len(set(self.game_pole[self.row])) == 1:
            return True
        else:
            return False

    def check_vertical(self):
        temp_list = []
        for i in range(0, 3):
            temp_list.append(self.game_pole[i][self.column])
        if len(set(temp_list)) == 1:
            return True
        else:
            return False

    def check_diagonal_1(self):
        temp_list1 = []
        for i in range(0, 3):
            temp_list1.append(self.game_pole[i][i])
            print(temp_list1)
        if len(set(temp_list1)) == 1:
            return True
        else:
            return False

    def check_diagonal_2(self):
        temp_list2 = []
        for i in range(0, 3):
            temp_list2.append(self.game_pole[2 - i][i])
        if len(set(temp_list2)) == 1:
            return True
        else:
            return False

    def check_score(self):
        if self.check_horizontal():
            self.win = 2
        elif self.check_vertical():
            self.win = 3
        elif self.hover_index % 2 == 0:
            if self.check_diagonal_1():
                self.win = 4
            elif self.check_diagonal_2():
                self.win = 5
        elif len(self.sprite_x_list) == 9:
            self.win = 1

    # Draw grid
    def draw_lines_vertical(self):
        for line in self.VERTICAL_LINES:
            arcade.draw_line(line['x'], line['start_y'], line['x'], line['end_y'], self.vertical_line_color, 3)

    def draw_lines_horizontal(self):
        for line in self.HORIZONTAL_LINES:
            arcade.draw_line(line['start_x'], line['y'], line['end_x'], line['y'], self.horizontal_line_color, 3)

    # Animate line after wining
    def animate_line(self, delta_time):
        # Check if the line is not fully drawn
        if self.distance < 600:
            self.distance += delta_time * 500
            return False
        else:
            return True

    def animate_line_vertical(self):
        arcade.draw_line(200, 200 + (2 - self.row) * 200, self.distance, 200 + (2 - self.row) * 200,
                         self.animation_line_color, 10)

    def animate_line_horizontal(self):
        arcade.draw_line(200 + self.column * 200, 200, 200 + self.column * 200, self.distance,
                         self.animation_line_color, 10)

    def animate_line_diagonal_2(self):
        arcade.draw_line(200, 200, self.distance, self.distance, self.animation_line_color, 10)

    def animate_line_diagonal_1(self):
        arcade.draw_line(600, 200, 800 - self.distance, self.distance, self.animation_line_color, 10)

    # ======================= Render function ========================================
    # Function for drawing on window
    def on_draw(self):

        arcade.set_background_color(self.background_color)

        # Clear everything, only background stay
        self.clear()

        # Start render
        arcade.start_render()

        # Draw game grid
        self.draw_lines_vertical()
        self.draw_lines_horizontal()

        # Draw Turn: text
        self.turn.draw()

        # Draw all sprites
        for sprite in self.sprite_x_list:
            sprite.draw()

        # ======================= Draw hover ========================================
        if self.hover_index is not None:
            # Take dimension from coordinate list and draw hover
            x_min, x_max, y_min, y_max = self.coordinates[self.hover_index]
            arcade.draw_rectangle_outline(x_min + 100, y_max - 100, 170, 170, self.hover_color)

        # ======================= Draw sprite ========================================
        if self.draw_sprite:
            # Get position for sprite
            x_min, x_max, y_min, y_max = self.coordinates[self.hover_index]
            # Get row and column
            self.which_row_and_column()

            # Check if it's already occupited
            if self.game_pole[self.row][self.column] == 1 or self.game_pole[self.row][self.column] == 0:
                self.draw_sprite = False
            else:
                # Check which Sprite to create
                if self.whose_turn == "X":
                    self.texture_path = 'Sprites/x.png'
                    self.game_pole[self.row][self.column] = 1
                else:
                    self.texture_path = 'Sprites/o.png'
                    self.game_pole[self.row][self.column] = 0

                # Create Sprite, set position and add to Sprite list
                sprite = Sprite(f"x{self.hover_index}", self.texture_path)
                sprite.sprite_set_position(x_min, y_max)
                self.sprite_x_list.append(sprite)

                # Change move to next player
                if self.texture_path == 'x.png':
                    self.whose_turn = "O"
                else:
                    self.whose_turn = "X"
                self.turn.text = f"Turn: {self.whose_turn}"

                # Check score
                self.check_score()
                self.draw_sprite = False

        # =========== Game Over ===============
        if self.win is not None:
            # If game is over, first block mouse move and click
            self.mouse_state_move = False
            self.mouse_state_click = False

            # Check which animation to display
            if self.win == 1:
                time.sleep(0.5)
                view = GameOver()
                self.window.show_view(view)
            if self.win == 2:
                self.animate_line_vertical()
            elif self.win == 3:
                self.animate_line_horizontal()
            elif self.win == 4:
                self.animate_line_diagonal_1()
            elif self.win == 5:
                self.animate_line_diagonal_2()

            if self.animation_end is True:
                time.sleep(0.5)
                view = GameOver()
                self.window.show_view(view)

    # ======================= Mouse motion function ========================================
    # Function is called, when the mouse is moved
    # Iterate over coordinates list and save the index of current grid field (1 of 9)
    def on_mouse_motion(self, x, y, dx, dy):
        if self.mouse_state_move is False:
            return False

        self.hover_index = None
        for index, (x_min, x_max, y_min, y_max) in enumerate(self.coordinates):
            if x_min < x < x_max and y_min < y < y_max:
                self.hover_index = index
                break

    # ======================= Mouse press function ========================================
    # Function is called, when the mouse is clicked
    def on_mouse_press(self, x, y, button, modifiers):
        if self.mouse_state_click is False:
            return False

        if button == arcade.MOUSE_BUTTON_LEFT and self.hover_index is not None:
            self.draw_sprite = True

    def on_update(self, delta_time):
        if self.win is not None:
            self.animation_end = self.animate_line(delta_time)


class GameOver(arcade.View):
    def __init__(self):
        super().__init__()

    def on_draw(self):
        self.clear()
        arcade.start_render()
        arcade.draw_text("Game Over - press ENTER to play again", 350, 750, arcade.color.WHITE, 16)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ENTER:
            game = GameScreen()
            self.window.show_view(game)


def main():
    # Create Window object
    window = GameWindow()

    # Create main game View object
    game = GameScreen()

    # Show main game view
    window.show_view(game)

    # Run game main loop
    arcade.run()


if __name__ == "__main__":
    main()
