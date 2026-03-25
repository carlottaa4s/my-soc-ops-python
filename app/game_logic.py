import functools
import random

from app.data import FREE_SPACE, QUESTIONS
from app.models import BingoLine, BingoSquareData, ScavengerHuntItem

BOARD_SIZE = 5
CENTER_INDEX = 12  # 5x5 grid, center is index 12 (row 2, col 2)


def generate_board() -> list[BingoSquareData]:
    """Generate a new 5x5 bingo board."""
    questions = iter(random.sample(QUESTIONS, 24))
    return [
        BingoSquareData(id=i, text=FREE_SPACE, is_marked=True, is_free_space=True)
        if i == CENTER_INDEX
        else BingoSquareData(id=i, text=next(questions))
        for i in range(BOARD_SIZE * BOARD_SIZE)
    ]


def toggle_square(
    board: list[BingoSquareData], square_id: int
) -> list[BingoSquareData]:
    """Toggle a square's marked state. Returns a new board list."""
    return [
        sq.model_copy(update={"is_marked": not sq.is_marked})
        if sq.id == square_id and not sq.is_free_space
        else sq
        for sq in board
    ]


def generate_scavenger_hunt_list() -> list[ScavengerHuntItem]:
    """Generate a new scavenger hunt list with all 24 questions."""
    questions = random.sample(QUESTIONS, 24)
    return [
        ScavengerHuntItem(id=i, text=question) for i, question in enumerate(questions)
    ]


def toggle_hunt_item(
    items: list[ScavengerHuntItem], item_id: int
) -> list[ScavengerHuntItem]:
    """Toggle a hunt item's found state. Returns a new items list."""
    return [
        item.model_copy(update={"is_found": not item.is_found})
        if item.id == item_id
        else item
        for item in items
    ]


@functools.cache
def _get_winning_lines() -> tuple[BingoLine, ...]:
    """Get all possible winning lines (cached)."""
    lines: list[BingoLine] = []

    # Rows
    for row in range(BOARD_SIZE):
        squares = [row * BOARD_SIZE + col for col in range(BOARD_SIZE)]
        lines.append(BingoLine(type="row", index=row, squares=squares))

    # Columns
    for col in range(BOARD_SIZE):
        squares = [row * BOARD_SIZE + col for row in range(BOARD_SIZE)]
        lines.append(BingoLine(type="column", index=col, squares=squares))

    # Diagonals
    lines.append(BingoLine(type="diagonal", index=0, squares=[0, 6, 12, 18, 24]))
    lines.append(BingoLine(type="diagonal", index=1, squares=[4, 8, 12, 16, 20]))

    return tuple(lines)


def check_bingo(board: list[BingoSquareData]) -> BingoLine | None:
    """Check if there's a bingo and return the winning line."""
    if len(board) < BOARD_SIZE * BOARD_SIZE:
        return None
    return next(
        (
            line
            for line in _get_winning_lines()
            if all(board[idx].is_marked for idx in line.squares)
        ),
        None,
    )


def get_winning_square_ids(line: BingoLine | None) -> set[int]:
    """Get the square IDs that are part of a winning line."""
    return set(line.squares) if line else set()
