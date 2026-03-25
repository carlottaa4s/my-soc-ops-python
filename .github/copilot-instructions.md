---
applyTo: "**"
---

# Copilot Workspace Instructions

**Soc Ops** is a Social Bingo game built with **FastAPI + Jinja2 + HTMX**. Players find people who match questions to mark squares and get 5 in a row. This is an educational lab project demonstrating AI-assisted development workflows.

## Quick Start

| Command | Purpose |
|---------|---------|
| `uv sync` | Install dependencies |
| `uv run pytest` | Run all tests |
| `uv run ruff check .` | Lint code |
| `uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000` | Start dev server on `http://localhost:8000` |

**Environment**: Python 3.13+, FastAPI, HTMX

## Architecture

```
app/
├── main.py              # FastAPI routes & HTMX endpoints
├── models.py            # Pydantic models (GameState, BingoSquare)
├── game_logic.py        # Board generation & bingo detection
├── game_service.py      # Session management (GameSession)
├── data.py              # Question bank
├── templates/           # Jinja2 templates
│   ├── base.html        # Layout wrapper
│   ├── home.html        # Landing page
│   └── components/      # HTMX components (bingo_board, game_screen, etc.)
└── static/
    ├── css/app.css      # Custom utility classes
    └── js/htmx.min.js   # HTMX library (no build step)

tests/
├── test_api.py          # FastAPI endpoint tests (httpx + TestClient)
└── test_game_logic.py   # Game logic unit tests
```

## Code Conventions

### Python
- **Type hints required** on function signatures
- **snake_case** for functions and variables
- **SCREAMING_SNAKE_CASE** for constants
- **Pydantic models** for all data structures
- **No unused imports** (linted by ruff)
- **Line length**: 88 characters

### Testing
- **Test-Driven Development (TDD)** encouraged via `/create-agent TDD-Cycle`
- **HTTP tests** use FastAPI's TestClient (in `test_api.py`)
- **Unit tests** isolate game logic (in `test_game_logic.py`)
- All 25 tests must pass before committing
- Aim for >80% code coverage

### Frontend (Jinja2 + HTMX)
- **No build step** — templates are rendered server-side
- **HTMX attributes** handle dynamic interactions (`hx-get`, `hx-post`, etc.)
- **Custom CSS utilities** defined in `app/static/css/app.css` (Tailwind-like syntax)
- See [CSS Utilities Instruction](/.github/instructions/css-utilities.instructions.md) for available classes
- See [Frontend Design Instruction](/.github/instructions/frontend-design.instructions.md) for design guidance

## Development Workflow

### Before Committing
```bash
# 1. Format & lint
uv run ruff check . --fix

# 2. Run all tests
uv run pytest

# 3. Verify dev server still runs
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Adding a Feature
1. **Write failing tests** in `tests/` matching the feature spec
2. **Implement** the feature in `app/` to pass tests
3. **Lint & test** to ensure no regressions
4. **Manual test** by running dev server and interacting with the UI

### Using AI Agents
- **`/TDD Supervisor`** agent orchestrates the full TDD cycle (red → green → refactor)
- **Setup & context** provided by `/setup` prompt

## Key Files & Patterns

### Game Logic (`app/game_logic.py`)
- `generate_bingo_board()` — Creates randomized 5x5 grid
- `check_bingo()` — Detects 5-in-a-row (horizontal, vertical, diagonal)
- Deterministic for reproducibility; uses seeded randomness when needed

### Session Management (`app/game_service.py`)
- `GameSession` class persists game state server-side
- State signed with itsdangerous for security
- Cookie-based client-side tracking

### API Routes (`app/main.py`)
- `GET /` — Home page
- `POST /start` — Initialize game, return board HTML
- `POST /mark` — Mark square, return updated board
- `GET /result` — Game result screen
- All HTMX responses return partial HTML, not full documents

### Styling Philosophy
- **No CSS framework** (no Tailwind CDN, no Bootstrap)
- **Custom utilities** composed in `app/static/css/app.css`
- Consistent with [CSS Utilities](/.github/instructions/css-utilities.instructions.md)

## State & Data Management

### Game State
```python
class GameState(BaseModel):
    board: list[BingoSquare]  # 25 squares, 5x5 grid
    marked: dict[int, bool]   # Track marked squares
    timestamp: datetime       # Game creation time

class BingoSquare(BaseModel):
    id: int
    question: str
```

### Persistence
- Session state stored server-side in `GameSession` instances
- Client maintains state reference via signed cookie
- No database (in-memory for lab purposes)

## Important Notes

- **No Simple Browser**: The VS Code Simple Browser doesn't support HTMX correctly. Always use `$BROWSER` or instruct users to open `http://localhost:8000` in their default browser.
- **Workshop Documentation**: Lab guides in `workshop/` folder explain design decisions and learning objectives. Reference when appropriate.
- **Existing Instructions**: Backend logic → follow Python conventions. Frontend → see CSS Utilities & Frontend Design skills.

## References

- [README.md](../../README.md) — Project overview & lab guide links
- [Contributing.md](../../CONTRIBUTING.md) — Contribution guidelines
- [workshop/](../../workshop/) — Detailed lab guides (Steps 0-4)
