BLACK_CHAR = "○"
WHITE_CHAR = "●"
EMPTY_CHAR = "*"


def flip_color(color: chr) -> chr:
    if color == BLACK_CHAR:
        return WHITE_CHAR
    elif color == WHITE_CHAR:
        return BLACK_CHAR


def create_board() -> list[list[chr]]:
    b, w, e = BLACK_CHAR, WHITE_CHAR, EMPTY_CHAR
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


def print_board(board: list[list[chr]]) -> None:
    row_number = 0
    black_count = 0
    white_count = 0
    print("  0 1 2 3 4 5 6 7")
    for row in board:
        black_count += row.count(BLACK_CHAR)
        white_count += row.count(WHITE_CHAR)
        print(f"{row_number} ", end="")
        print(*row)
        row_number += 1
    print()
    print(f"black ({BLACK_CHAR}): {black_count}")
    print(f"white ({WHITE_CHAR}): {white_count}")


def is_on_board(x: int, y: int) -> bool:
    return 0 <= x < 8 and 0 <= y < 8


def put(board: list[list[chr]], x: int, y: int, color: chr):
    if not is_on_board(x, y) or board[x][y] != EMPTY_CHAR:
        return board

    directions = get_flip_direction(board, x, y, color)
    if len(directions) == 0:
        return board

    board[y][x] = color
    for dx, dy in directions:
        for i in range(1, 8):
            cx = x + dx * i
            cy = y + dy * i
            if board[cy][cx] == flip_color(color):
                board[cy][cx] = color
            else:
                break

    return board


def get_flip_direction(
    board: list[list[chr]], x: int, y: int, color: chr
) -> list[tuple[int, int]]:
    directions = []

    if board[y][x] != EMPTY_CHAR:
        return directions

    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            opp_count = 0
            for i in range(1, 8):
                cx = x + dx * i
                cy = y + dy * i

                if not is_on_board(cx, cy):
                    break
                elif board[cy][cx] == EMPTY_CHAR:
                    break
                elif board[cy][cx] == flip_color(color):
                    opp_count += 1
                else:
                    if opp_count > 0:
                        directions.append((dx, dy))
                    break

    return directions


def get_flip_positions(board: list[list[chr]], color: chr):
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

    current_color = BLACK_CHAR
    while True:
        print()
        if current_color == BLACK_CHAR:
            current_player = "black"
        else:
            current_player = "white"
        print(f"Current player: {current_player}")
        print_board(board)

        black_flip_pos = get_flip_positions(board, BLACK_CHAR)
        white_flip_pos = get_flip_positions(board, WHITE_CHAR)

        if len(black_flip_pos) == 0 and len(white_flip_pos) == 0:
            print("No valid moves for both players. Game over.")
            break

        if current_color == BLACK_CHAR and len(black_flip_pos) == 0:
            print("No valid moves for black. Switching to white.")
            current_color = flip_color(current_color)
            continue
        if current_color == WHITE_CHAR and len(white_flip_pos) == 0:
            print("No valid moves for white. Switching to black.")
            current_color = flip_color(current_color)
            continue

        if current_color == BLACK_CHAR:
            flip_pos = black_flip_pos
        else:
            flip_pos = white_flip_pos

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
