from dataclasses import dataclass, field

from app.game_logic import (
    check_bingo,
    generate_board,
    generate_scavenger_hunt_list,
    get_winning_square_ids,
    toggle_hunt_item,
    toggle_square,
)
from app.models import (
    BingoLine,
    BingoSquareData,
    GameMode,
    GameState,
    ScavengerHuntItem,
)


@dataclass
class GameSession:
    """Holds the state for a single game session."""

    game_mode: GameMode | None = None
    game_state: GameState = GameState.START
    board: list[BingoSquareData] = field(default_factory=list)
    hunt_items: list[ScavengerHuntItem] = field(default_factory=list)
    winning_line: BingoLine | None = None
    show_bingo_modal: bool = False

    @property
    def winning_square_ids(self) -> set[int]:
        return get_winning_square_ids(self.winning_line)

    @property
    def has_bingo(self) -> bool:
        return self.game_state == GameState.BINGO

    @property
    def hunt_progress(self) -> tuple[int, int]:
        """Return (found_count, total_count) for scavenger hunt."""
        found = sum(1 for item in self.hunt_items if item.is_found)
        return (found, len(self.hunt_items))

    @property
    def hunt_complete(self) -> bool:
        """Check if all hunt items are found."""
        if not self.hunt_items:
            return False
        return all(item.is_found for item in self.hunt_items)

    def _reset_state(self) -> None:
        """Reset shared game state."""
        self.board = []
        self.hunt_items = []
        self.winning_line = None
        self.game_state = GameState.PLAYING
        self.show_bingo_modal = False

    def start_game_bingo(self) -> None:
        self._reset_state()
        self.game_mode = GameMode.BINGO
        self.board = generate_board()

    def start_game_scavenger_hunt(self) -> None:
        self._reset_state()
        self.game_mode = GameMode.SCAVENGER_HUNT
        self.hunt_items = generate_scavenger_hunt_list()

    def handle_square_click(self, square_id: int) -> None:
        if self.game_state != GameState.PLAYING or self.game_mode != GameMode.BINGO:
            return
        self.board = toggle_square(self.board, square_id)

        if self.winning_line is None:
            bingo = check_bingo(self.board)
            if bingo is not None:
                self.winning_line = bingo
                self.game_state = GameState.BINGO
                self.show_bingo_modal = True

    def handle_hunt_item_click(self, item_id: int) -> None:

        if (
            self.game_state != GameState.PLAYING
            or self.game_mode != GameMode.SCAVENGER_HUNT
        ):
            return
        self.hunt_items = toggle_hunt_item(self.hunt_items, item_id)
        if self.hunt_complete:
            self.game_state = GameState.COMPLETE

    def reset_game(self) -> None:
        self.game_mode = None
        self.game_state = GameState.START
        self.board = []
        self.hunt_items = []
        self.winning_line = None
        self.show_bingo_modal = False

    def dismiss_modal(self) -> None:
        self.show_bingo_modal = False
        self.game_state = GameState.PLAYING


# In-memory session store keyed by session ID
_sessions: dict[str, GameSession] = {}


def get_session(session_id: str) -> GameSession:
    """Get or create a game session for the given session ID."""
    if session_id not in _sessions:
        _sessions[session_id] = GameSession()
    return _sessions[session_id]
