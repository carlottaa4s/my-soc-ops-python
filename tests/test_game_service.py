from app.game_service import GameSession
from app.models import GameMode, GameState


class TestGameSessionScavengerHunt:
    def test_start_game_scavenger_hunt_initializes_hunt_items(self):
        session = GameSession()
        session.start_game_scavenger_hunt()
        assert len(session.hunt_items) == 24
        assert session.game_mode == GameMode.SCAVENGER_HUNT
        assert session.game_state == GameState.PLAYING

    def test_hunt_items_are_all_not_found_initially(self):
        session = GameSession()
        session.start_game_scavenger_hunt()
        for item in session.hunt_items:
            assert item.is_found is False

    def test_hunt_progress_property_returns_correct_tuple(self):
        session = GameSession()
        session.start_game_scavenger_hunt()
        assert session.hunt_progress == (0, 24)

    def test_hunt_progress_updates_after_toggle(self):
        session = GameSession()
        session.start_game_scavenger_hunt()
        session.handle_hunt_item_click(0)
        assert session.hunt_progress == (1, 24)

    def test_hunt_progress_with_multiple_items(self):
        session = GameSession()
        session.start_game_scavenger_hunt()
        for i in range(5):
            session.handle_hunt_item_click(i)
        assert session.hunt_progress == (5, 24)

    def test_hunt_complete_property_false_initially(self):
        session = GameSession()
        session.start_game_scavenger_hunt()
        assert session.hunt_complete is False

    def test_hunt_complete_property_true_when_all_found(self):
        session = GameSession()
        session.start_game_scavenger_hunt()
        for i in range(24):
            session.handle_hunt_item_click(i)
        assert session.hunt_complete is True
        assert session.game_state == GameState.COMPLETE

    def test_handle_hunt_item_click_toggles_item(self):
        session = GameSession()
        session.start_game_scavenger_hunt()
        assert session.hunt_items[5].is_found is False
        session.handle_hunt_item_click(5)
        assert session.hunt_items[5].is_found is True
        session.handle_hunt_item_click(5)
        assert session.hunt_items[5].is_found is False

    def test_hunt_item_click_ignored_when_not_playing(self):
        session = GameSession()
        session.start_game_scavenger_hunt()
        session.game_state = GameState.COMPLETE
        # Try to toggle an item
        session.handle_hunt_item_click(0)
        # Should still be not found because game state is COMPLETE
        assert session.hunt_items[0].is_found is False

    def test_hunt_item_click_ignored_when_wrong_mode(self):
        session = GameSession()
        session.start_game_bingo()
        # Try to handle hunt item click in bingo mode
        session.handle_hunt_item_click(0)
        # Should not have hunt items
        assert session.hunt_items == []

    def test_reset_game_clears_hunt_items(self):
        session = GameSession()
        session.start_game_scavenger_hunt()
        session.handle_hunt_item_click(0)
        session.reset_game()
        assert session.hunt_items == []
        assert session.game_mode is None

    def test_hunt_items_are_unique_questions(self):
        session = GameSession()
        session.start_game_scavenger_hunt()
        texts = [item.text for item in session.hunt_items]
        assert len(texts) == len(set(texts)), (
            "All hunt items should have unique questions"
        )


class TestGameSessionBingoMode:
    def test_start_game_bingo_initializes_board(self):
        session = GameSession()
        session.start_game_bingo()
        assert len(session.board) == 25
        assert session.game_mode == GameMode.BINGO
        assert session.game_state == GameState.PLAYING

    def test_start_game_bingo_clears_hunt_items(self):
        session = GameSession()
        session.start_game_scavenger_hunt()
        assert len(session.hunt_items) > 0
        session.start_game_bingo()
        assert session.hunt_items == []

    def test_bingo_square_click_ignored_in_hunt_mode(self):
        session = GameSession()
        session.start_game_scavenger_hunt()
        # Try to handle a bingo square click
        session.handle_square_click(0)
        # Board should still be empty
        assert session.board == []


class TestGameSessionReset:
    def test_reset_returns_to_start_state(self):
        session = GameSession()
        session.start_game_scavenger_hunt()
        session.handle_hunt_item_click(5)
        session.reset_game()
        assert session.game_state == GameState.START
        assert session.game_mode is None
        assert session.board == []
        assert session.hunt_items == []
        assert session.winning_line is None
        assert session.show_bingo_modal is False
