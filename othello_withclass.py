# Othello game implementation without class & GUI


BLACK = 1
WHITE = 2
EMPTY = 0

BLACK_CHAR = "○"
WHITE_CHAR = "●"
EMPTY_CHAR = "*"


def safe_input(prompt: str) -> int:
    while True:
        try:
            output = input(prompt)
            return int(output)
        except Exception as e:
            print("Invalid input. Please enter a number.")


class Othello:
    BLACK = 1
    WHITE = 2
    EMPTY = 0

    BLACK_CHAR = "○"
    WHITE_CHAR = "●"
    EMPTY_CHAR = "*"

    def __init__(self):
        self.board = self.create_board()

    def flip_color(self, color: int) -> int:
        return WHITE if color == BLACK else BLACK

    def create_board(self) -> list[list[int]]:
        b, w, e = BLACK, WHITE, EMPTY
        return [
            [e, e, e, e, e, e, e, e],
            [e, e, e, e, e, e, e, e],
            [e, e, e, e, e, e, e, e],
            [e, e, e, w, b, e, e, e],
            [e, e, e, b, w, e, e, e],
            [e, e, e, e, e, e, e, e],
            [e, e, e, e, e, e, e, e],
            [e, e, e, e, e, e, e, e],
        ]

    def print_board(self) -> None:
        print(f"black ({BLACK_CHAR}): {sum([row.count(BLACK) for row in self.board])}")
        print(f"white ({WHITE_CHAR}): {sum([row.count(WHITE) for row in self.board])}")
        print("  0 1 2 3 4 5 6 7")
        for y in range(len(self.board)):
            row = self.board[y]
            print(
                f"{y} "
                + " ".join(
                    (
                        BLACK_CHAR
                        if cell == BLACK
                        else WHITE_CHAR if cell == WHITE else EMPTY_CHAR
                    )
                    for cell in row
                )
            )
        print()

    def is_on_board(self, x: int, y: int) -> bool:
        return 0 <= x < 8 and 0 <= y < 8

    def put(self, x: int, y: int, color: int):
        if not self.is_on_board(x, y) or self.board[y][x] != EMPTY:
            return

        directions = self.get_flip_direction(x, y, color)
        if len(directions) == 0:
            return

        self.board[y][x] = color
        for dx, dy in directions:
            for i in range(1, 8):
                cx, cy = x + dx * i, y + dy * i
                if self.board[cy][cx] == self.flip_color(color):
                    self.board[cy][cx] = color
                else:
                    break

    def get_flip_direction(self, x: int, y: int, color: int) -> list[tuple[int, int]]:
        directions = []

        if self.board[y][x] != EMPTY:
            return directions

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                opp_count = 0
                for i in range(1, 8):
                    cx, cy = x + dx * i, y + dy * i

                    if not self.is_on_board(cx, cy):
                        break
                    elif self.board[cy][cx] == EMPTY:
                        break
                    elif self.board[cy][cx] == self.flip_color(color):
                        opp_count += 1
                    else:  # board[cy][cx] == color
                        if opp_count > 0:
                            directions.append((dx, dy))
                        break
        return directions

    def get_flip_positions(self, color: int) -> list[tuple[int, int]]:
        positions = []
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if len(self.get_flip_direction(x, y, color)) > 0:
                    positions.append((x, y))
        return positions

    def play(self):
        self.board = self.create_board()

        current_color = BLACK
        while True:
            print()
            print(f"Current player: {'black' if current_color == BLACK else 'white'}")
            self.print_board()

            black_flip_pos = self.get_flip_positions(BLACK)
            white_flip_pos = self.get_flip_positions(WHITE)

            if len(black_flip_pos) == 0 and len(white_flip_pos) == 0:
                print("No valid moves for both players. Game over.")
                break

            if current_color == BLACK and len(black_flip_pos) == 0:
                print("No valid moves for black. Switching to white.")
                current_color = self.flip_color(current_color)
                continue
            if current_color == WHITE and len(white_flip_pos) == 0:
                print("No valid moves for white. Switching to black.")
                current_color = self.flip_color(current_color)
                continue

            flip_pos = black_flip_pos if current_color == BLACK else white_flip_pos

            while True:
                x = safe_input("Enter x coordinate (0-7): ")
                y = safe_input("Enter y coordinate (0-7): ")

                if (x, y) in flip_pos:
                    break
                else:
                    print(f"Invalid move. Possible moves: {flip_pos}")

            self.put(x, y, current_color)
            current_color = self.flip_color(current_color)


if __name__ == "__main__":
    game = Othello()
    game.play()
