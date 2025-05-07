import random
from enum import Enum


class Field:
    def __init__(self, x: int, y: int, bomb_number: int, first_to_open: tuple[int, int] | tuple) -> None:
        if x < 5 or y < 5:  # устанавливаем минимальный размер поля
            raise ValueError("x, y must be >= 5")
        if bomb_number < 3:  # устанавливаем минимальное количество бомб
            raise ValueError("the number of bombs must be >= 3")
        if bomb_number >= x * y:
            raise ValueError("Too many bombs")

        self.width = x
        self.height = y
        self.field = [[Cell(empty=True, open=False) for _ in range(x)] for _ in range(y)]  # empty, closed at this moment
        self.bomb_number = bomb_number
        self.first_to_open = first_to_open
        self.closed_cells_countdown = (self.width * self.height) - self.bomb_number

    def _neighbour_cell(self, nx, ny):
        """ Checks if cell is within field boarders and contains a bomb"""
        x_boarder = 0 <= nx < self.height
        y_boarder = 0 <= ny < self.width

        if x_boarder and y_boarder and not self.field[nx][ny].empty:
            return True

        return False

    def generate_field(self) -> None:
        all_cells = [(i, j) for i in range(self.height) for j in range(self.width)]
        try:
            all_cells.remove(self.first_to_open)
        except Exception as e:
            raise ValueError("Invalid first cell coords") from e

        bomb_positions = random.sample(all_cells, self.bomb_number)

        for x, y in bomb_positions:
            self.field[x][y].set_bomb()

        for i in range(self.height):
            for j in range(self.width):
                if self.field[i][j].empty:
                    bomb_count = 0

                    for dx in [-1, 0, 1]:  # displacement
                        for dy in [-1, 0, 1]:
                            nx, ny = i + dx, j + dy  # next
                            if self._neighbour_cell(nx, ny):  # boarders
                                bomb_count += 1
                    self.field[i][j].empty_cell_content = str(bomb_count) if bomb_count > 0 else ' '


class Cell:
    __CLOSED_CELL = "*"
    __BOMB = "!"

    def __init__(self, empty: bool, open: bool) -> None:
        self.empty = empty
        self.open = open
        self.empty_cell_content = ''

    def __repr__(self) -> str:
        if self.open:
            return self.empty_cell_content if self.empty else self.__BOMB
        else:
            return self.__CLOSED_CELL

    def set_bomb(self) -> None:
        self.empty = False


class ConsoleOutput:
    RULES = ("      * * * * * * *\n"
             "        COMMANDS\n"
             "start - to start the game.\n"
             "quit - to stop the game.\n"
             ""
             "     IN GAME COMMANDS\n"
             "show - to show the field.\n"
             "open X V - to open a cell.\n"
             "      * * * * * * *")

    @staticmethod
    def print_field(field: Field) -> None:
        print("  ", end="")
        for col in range(field.width):
            print(f"{col:2}", end="")
        print()

        for i, row in enumerate(field.field):
            print(f"{i:2} ", end="")  # row number
            print(" ".join(str(cell) for cell in row))

    @staticmethod
    def print_rules() -> None:
        print(ConsoleOutput.RULES)


class GameLogic:
    def __init__(self, field: Field) -> None:
        self.bomb_flag = False  # indicates if a bomb was found
        self.open_cells_flag = False  # indicates if all sells were opened
        self.field: Field = field
        self.field.generate_field()
        self.closed_cells_countdown = self.field.closed_cells_countdown

    def open_cell(self, x: int, y: int) -> None:
        cur_cell = self.field.field[x][y]
        if cur_cell.open:
            return

        if not cur_cell.empty:
            self.bomb_flag = True

        cur_cell.open = True
        self.closed_cells_countdown -= 1

        if cur_cell.empty_cell_content == ' ':
            self.open_neighbors(x, y)

    def open_neighbors(self, x: int, y: int) -> None:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.field.height and 0 <= ny < self.field.width:
                    if not self.field.field[nx][ny].open:
                        self.open_cell(nx, ny)

    def open_all_cells(self) -> None:
        for _x in range(self.field.height):
            for _y in range(self.field.width):
                self.open_cell(_x, _y)


class CMD(Enum):
    QUIT = "quit"
    Q = "q"
    OPEN = "open"
    SHOW = "show"
    START = "start"


class GameController:
    @staticmethod
    def run_game(game, field):
        """ The main cycle of the game"""
        while True:
            if game.bomb_flag:
                print("You lost!")
                game.open_all_cells()
                ConsoleOutput.print_field(field=field)
                break

            if game.closed_cells_countdown == 0:
                print("You won!")
                game.open_all_cells()
                ConsoleOutput.print_field(field=field)
                break

            command = input()

            if command.lower() in {CMD.QUIT.value, CMD.Q.value}:
                print("END")
                break

            elif command.startswith(CMD.OPEN.value):
                try:
                    coords = command.split()[1:]
                    x, y = map(int, coords)
                    game.open_cell(x, y)
                    ConsoleOutput.print_field(field=field)
                except (ValueError, IndexError):
                    print("Invalid coordinates format")

            elif command == CMD.SHOW.value:
                ConsoleOutput.print_field(field=field)

            else:
                print("Unknown command")
                ConsoleOutput.print_rules()

    @staticmethod
    def run() -> None:
        try:
            x_ = int(input("The width of the field: "))
            y_ = int(input("The height of the field: "))
            bomb_number_ = int(input("The number of bombs: "))
            first = tuple(map(int, input("The first cell to open (X Y): ").split()))
            field = Field(x=x_, y=y_, bomb_number=bomb_number_, first_to_open=first)
            game = GameLogic(field)
            ConsoleOutput.print_rules()
            start_command = input("Enter 'start' to start the game: ")

            if start_command == CMD.START.value:
                ConsoleOutput.print_field(field=field)

                # while cycle for the main game
                GameController.run_game(game=game, field=field)

            elif start_command.lower() in {CMD.QUIT.value, CMD.Q.value}:
                print("END")
            else:
                print("Unknown command")
                ConsoleOutput.print_rules()

        except ValueError as ve:
            print(ve)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    GameController.run()
