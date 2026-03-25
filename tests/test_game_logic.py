from app.data import FREE_SPACE, QUESTIONS
from app.game_logic import (
    CENTER_INDEX,
    check_bingo,
    generate_board,
    generate_scavenger_hunt_list,
    get_winning_square_ids,
    toggle_hunt_item,
    toggle_square,
)
from app.models import BingoLine, BingoSquareData


class TestGenerateBoard:
    def test_board_has_25_squares(self):
        board = generate_board()
        assert len(board) == 25

    def test_center_is_free_space(self):
        board = generate_board()
        center = board[CENTER_INDEX]
        assert center.is_free_space is True
        assert center.is_marked is True
        assert center.text == FREE_SPACE

    def test_non_center_squares_are_not_free_space(self):
        board = generate_board()
        for i, square in enumerate(board):
            if i != CENTER_INDEX:
                assert square.is_free_space is False
                assert square.is_marked is False

    def test_all_questions_from_pool(self):
        board = generate_board()
        texts = {s.text for s in board if not s.is_free_space}
        assert texts.issubset(set(QUESTIONS))

    def test_squares_have_sequential_ids(self):
        board = generate_board()
        for i, square in enumerate(board):
            assert square.id == i

    def test_board_is_shuffled(self):
        """Verify two boards aren't identical (high probability)."""
        board1 = generate_board()
        board2 = generate_board()
        texts1 = [s.text for s in board1]
        texts2 = [s.text for s in board2]
        # Extremely unlikely to be identical
        assert texts1 != texts2


class TestToggleSquare:
    def test_toggle_marks_unmarked_square(self):
        board = generate_board()
        square_id = 0
        assert board[square_id].is_marked is False
        new_board = toggle_square(board, square_id)
        assert new_board[square_id].is_marked is True

    def test_toggle_unmarks_marked_square(self):
        board = generate_board()
        board = toggle_square(board, 0)
        assert board[0].is_marked is True
        board = toggle_square(board, 0)
        assert board[0].is_marked is False

    def test_toggle_does_not_affect_free_space(self):
        board = generate_board()
        new_board = toggle_square(board, CENTER_INDEX)
        assert new_board[CENTER_INDEX].is_marked is True  # Still marked

    def test_toggle_returns_new_list(self):
        board = generate_board()
        new_board = toggle_square(board, 0)
        assert board is not new_board


class TestCheckBingo:
    def _make_board(self, marked_ids: set[int]) -> list[BingoSquareData]:
        board = generate_board()
        result = []
        for square in board:
            if square.id in marked_ids or square.is_free_space:
                result.append(
                    BingoSquareData(
                        id=square.id,
                        text=square.text,
                        is_marked=True,
                        is_free_space=square.is_free_space,
                    )
                )
            else:
                result.append(square)
        return result

    def test_no_bingo_initially(self):
        board = generate_board()
        assert check_bingo(board) is None

    def test_row_bingo(self):
        # Mark first row: indices 0-4
        board = self._make_board({0, 1, 2, 3, 4})
        result = check_bingo(board)
        assert result is not None
        assert result.type == "row"
        assert result.squares == [0, 1, 2, 3, 4]

    def test_column_bingo(self):
        # Mark first column: indices 0, 5, 10, 15, 20
        board = self._make_board({0, 5, 10, 15, 20})
        result = check_bingo(board)
        assert result is not None
        assert result.type == "column"
        assert result.squares == [0, 5, 10, 15, 20]

    def test_diagonal_bingo(self):
        # Mark diagonal: 0, 6, 12, 18, 24 (12 is free space)
        board = self._make_board({0, 6, 18, 24})
        result = check_bingo(board)
        assert result is not None
        assert result.type == "diagonal"
        assert result.squares == [0, 6, 12, 18, 24]

    def test_partial_line_no_bingo(self):
        board = self._make_board({0, 1, 2, 3})  # Only 4 of 5 in first row
        assert check_bingo(board) is None


class TestGetWinningSquareIds:
    def test_none_line_returns_empty_set(self):
        assert get_winning_square_ids(None) == set()

    def test_returns_square_ids(self):
        line = BingoLine(type="row", index=0, squares=[0, 1, 2, 3, 4])
        assert get_winning_square_ids(line) == {0, 1, 2, 3, 4}


class TestGenerateScavengerHuntList:
    def test_hunt_list_has_24_items(self):
        hunt_list = generate_scavenger_hunt_list()
        assert len(hunt_list) == 24

    def test_hunt_items_are_not_found_initially(self):
        hunt_list = generate_scavenger_hunt_list()
        for item in hunt_list:
            assert item.is_found is False

    def test_hunt_items_have_sequential_ids(self):
        hunt_list = generate_scavenger_hunt_list()
        for i, item in enumerate(hunt_list):
            assert item.id == i

    def test_hunt_items_have_unique_questions(self):
        hunt_list = generate_scavenger_hunt_list()
        texts = [item.text for item in hunt_list]
        assert len(texts) == len(set(texts)), "Hunt items should have unique questions"

    def test_all_hunt_questions_from_pool(self):
        hunt_list = generate_scavenger_hunt_list()
        texts = {item.text for item in hunt_list}
        assert texts.issubset(set(QUESTIONS))

    def test_hunt_list_is_shuffled(self):
        """Verify two hunt lists aren't identical (high probability)."""
        hunt1 = generate_scavenger_hunt_list()
        hunt2 = generate_scavenger_hunt_list()
        texts1 = [item.text for item in hunt1]
        texts2 = [item.text for item in hunt2]
        assert texts1 != texts2


class TestToggleHuntItem:
    def test_toggle_marks_unfound_item(self):
        items = generate_scavenger_hunt_list()
        assert items[0].is_found is False
        new_items = toggle_hunt_item(items, 0)
        assert new_items[0].is_found is True

    def test_toggle_unmarks_found_item(self):
        items = generate_scavenger_hunt_list()
        items = toggle_hunt_item(items, 0)
        assert items[0].is_found is True
        items = toggle_hunt_item(items, 0)
        assert items[0].is_found is False

    def test_toggle_does_not_affect_other_items(self):
        items = generate_scavenger_hunt_list()
        original_state = [item.is_found for item in items[1:]]
        new_items = toggle_hunt_item(items, 0)
        new_state = [item.is_found for item in new_items[1:]]
        assert new_state == original_state

    def test_toggle_returns_new_list(self):
        items = generate_scavenger_hunt_list()
        new_items = toggle_hunt_item(items, 0)
        assert items is not new_items

    def test_toggle_item_with_invalid_id_does_nothing(self):
        items = generate_scavenger_hunt_list()
        original_texts = [item.text for item in items]
        new_items = toggle_hunt_item(items, 999)
        new_texts = [item.text for item in new_items]
        assert original_texts == new_texts
        for item in new_items:
            assert item.is_found is False
