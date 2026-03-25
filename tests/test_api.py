import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


class TestHomePage:
    def test_home_returns_200(self, client: TestClient):
        response = client.get("/")
        assert response.status_code == 200

    def test_home_contains_start_screen(self, client: TestClient):
        response = client.get("/")
        assert "Soc Ops" in response.text
        assert "BINGO MODE" in response.text
        assert "SCAVENGER HUNT" in response.text
        assert "SELECT MODE" in response.text

    def test_home_sets_session_cookie(self, client: TestClient):
        response = client.get("/")
        assert "session" in response.cookies


class TestStartGame:
    def test_start_returns_game_board(self, client: TestClient):
        # First visit to get session
        client.get("/")
        response = client.post("/start-bingo")
        assert response.status_code == 200
        assert "FREE SPACE" in response.text
        assert "BACK" in response.text

    def test_board_has_25_squares(self, client: TestClient):
        client.get("/")
        response = client.post("/start-bingo")
        # Count the toggle buttons (squares with hx-post="/toggle/")
        assert response.text.count('hx-post="/toggle/') == 24  # 24 + 1 free space


class TestToggleSquare:
    def test_toggle_marks_square(self, client: TestClient):
        client.get("/")
        client.post("/start-bingo")
        response = client.post("/toggle/0")
        assert response.status_code == 200
        # The response should contain the game screen with a marked square
        assert "FREE SPACE" in response.text


class TestResetGame:
    def test_reset_returns_start_screen(self, client: TestClient):
        client.get("/")
        client.post("/start-bingo")
        response = client.post("/reset")
        assert response.status_code == 200
        assert "BINGO MODE" in response.text
        assert "SELECT MODE" in response.text


class TestDismissModal:
    def test_dismiss_returns_game_screen(self, client: TestClient):
        client.get("/")
        client.post("/start-bingo")
        response = client.post("/dismiss-modal")
        assert response.status_code == 200
        assert "FREE SPACE" in response.text


class TestStartScavengerHunt:
    def test_start_scavenger_hunt_returns_hunt_screen(self, client: TestClient):
        client.get("/")
        response = client.post("/start-scavenger-hunt")
        assert response.status_code == 200
        assert "ITEMS FOUND" in response.text

    def test_hunt_screen_has_24_items(self, client: TestClient):
        client.get("/")
        response = client.post("/start-scavenger-hunt")
        # Count buttons with hx-post="/toggle-hunt/"
        assert response.text.count('hx-post="/toggle-hunt/') == 24

    def test_hunt_screen_shows_progress(self, client: TestClient):
        client.get("/")
        response = client.post("/start-scavenger-hunt")
        # Progress should show 0 / 24 initially
        assert "0 / 24" in response.text or "0%" in response.text

    def test_hunt_screen_has_back_button(self, client: TestClient):
        client.get("/")
        response = client.post("/start-scavenger-hunt")
        assert "◄ BACK" in response.text
        assert 'hx-post="/reset"' in response.text


class TestToggleHuntItem:
    def test_toggle_hunt_item_marks_item(self, client: TestClient):
        client.get("/")
        client.post("/start-scavenger-hunt")
        response = client.post("/toggle-hunt/0")
        assert response.status_code == 200
        # After toggling, the progress should show 1 / 24
        assert "1 / 24" in response.text or "4%" in response.text

    def test_toggle_hunt_item_unmarks_item(self, client: TestClient):
        client.get("/")
        client.post("/start-scavenger-hunt")
        client.post("/toggle-hunt/0")
        response = client.post("/toggle-hunt/0")
        # After toggling again, should return to 0 / 24
        assert "0 / 24" in response.text or "0%" in response.text

    def test_toggle_multiple_hunt_items(self, client: TestClient):
        client.get("/")
        client.post("/start-scavenger-hunt")
        client.post("/toggle-hunt/0")
        client.post("/toggle-hunt/5")
        response = client.post("/toggle-hunt/10")
        # Three items toggled should show 3 / 24
        assert "3 / 24" in response.text or "12%" in response.text

    def test_hunt_completion_message_appears(self, client: TestClient):
        """Mark all 24 items and verify completion message."""
        client.get("/")
        client.post("/start-scavenger-hunt")
        # Toggle all 24 items
        for i in range(24):
            client.post(f"/toggle-hunt/{i}")
        response = client.post("/toggle-hunt/0")  # Final toggle to verify state
        # Should show completion message
        assert "ALL FOUND" in response.text


class TestGameSessionFilters:
    def test_hunt_item_toggle_does_not_affect_bingo_game(self, client: TestClient):
        """Toggling hunt items in hunt mode shouldn't affect anything else."""
        client.get("/")
        response = client.post("/start-scavenger-hunt")
        response = client.post("/toggle-hunt/5")
        # Should still be in hunt screen, not bingo
        assert "ITEMS FOUND" in response.text
        assert "FREE SPACE" not in response.text

    def test_bingo_toggle_does_not_affect_hunt_mode(self, client: TestClient):
        """Toggling bingo squares when in hunt mode should not alter hunt state."""
        client.get("/")
        client.post("/start-scavenger-hunt")
        # Try toggling a bingo square (should be ignored in hunt mode)
        response = client.post("/toggle/0")
        # Should still be in hunt screen
        assert "ITEMS FOUND" in response.text
