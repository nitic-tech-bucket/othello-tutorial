# Othello game implementation without class & GUI


BLACK = 1
WHITE = 2
EMPTY = 0

BLACK_CHAR = "○"
WHITE_CHAR = "●"
EMPTY_CHAR = "*"


def flip_color(color: int) -> int:
    return WHITE if color == BLACK else BLACK


def create_board() -> list[list[int]]:
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


def print_board(board: list[list[int]]) -> None:
    print(f"black ({BLACK_CHAR}): {sum([row.count(BLACK) for row in board])}")
    print(f"white ({WHITE_CHAR}): {sum([row.count(WHITE) for row in board])}")
    print("  0 1 2 3 4 5 6 7")
    for y in range(len(board)):
        row = board[y]
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


def is_on_board(x: int, y: int) -> bool:
    return 0 <= x < 8 and 0 <= y < 8


def put(board: list[list[int]], x: int, y: int, color: int) -> list[list[int]]:
    if not is_on_board(x, y) or board[y][x] != EMPTY:
        return board

    directions = get_flip_direction(board, x, y, color)
    if len(directions) == 0:
        return board

    board[y][x] = color
    for dx, dy in directions:
        for i in range(1, 8):
            cx, cy = x + dx * i, y + dy * i
            if board[cy][cx] == flip_color(color):
                board[cy][cx] = color
            else:
                break

    return board


def get_flip_direction(
    board: list[list[int]], x: int, y: int, color: int
) -> list[tuple[int, int]]:
    directions = []

    if board[y][x] != EMPTY:
        return directions

    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            opp_count = 0
            for i in range(1, 8):
                cx, cy = x + dx * i, y + dy * i

                if not is_on_board(cx, cy):
                    break
                elif board[cy][cx] == EMPTY:
                    break
                elif board[cy][cx] == flip_color(color):
                    opp_count += 1
                else:  # board[cy][cx] == color
                    if opp_count > 0:
                        directions.append((dx, dy))
                    break
    return directions


def get_flip_positions(board: list[list[int]], color: int) -> list[tuple[int, int]]:
    positions = []
    for y in range(len(board)):
        for x in range(len(board[y])):
            if len(get_flip_direction(board, x, y, color)) > 0:
                positions.append((x, y))
    return positions


def safe_input(prompt: str) -> int:
    while True:
        try:
            output = input(prompt)
            return int(output)
        except Exception as e:
            print("Invalid input. Please enter a number.")


def play():
    board = create_board()

    current_color = BLACK
    while True:
        print()
        print(f"Current player: {'black' if current_color == BLACK else 'white'}")
        print_board(board)

        black_flip_pos = get_flip_positions(board, BLACK)
        white_flip_pos = get_flip_positions(board, WHITE)

        if len(black_flip_pos) == 0 and len(white_flip_pos) == 0:
            print("No valid moves for both players. Game over.")
            break

        if current_color == BLACK and len(black_flip_pos) == 0:
            print("No valid moves for black. Switching to white.")
            current_color = flip_color(current_color)
            continue
        if current_color == WHITE and len(white_flip_pos) == 0:
            print("No valid moves for white. Switching to black.")
            current_color = flip_color(current_color)
            continue

        flip_pos = black_flip_pos if current_color == BLACK else white_flip_pos

        while True:
            x = safe_input("Enter x coordinate (0-7): ")
            y = safe_input("Enter y coordinate (0-7): ")

            if (x, y) in flip_pos:
                break
            else:
                print(f"Invalid move. Possible moves: {flip_pos}")

        board = put(board, x, y, current_color)

        current_color = flip_color(current_color)


if __name__ == "__main__":
    play()
