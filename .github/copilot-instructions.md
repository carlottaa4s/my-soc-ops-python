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

## Design Guide: Pixel Arcade Aesthetic

**Soc Ops** features a bold **Pixel Arcade** theme inspired by modern retro 80s/90s arcade cabinets. This guide ensures visual consistency across all UI elements.

### Color Palette

| Color | Hex | CSS Variable | Usage |
|-------|-----|--------------|-------|
| Black | `#0a0a0a` | `--arcade-black` | Primary background (all screens) |
| Red | `#ff3333` | `--arcade-red` | Victory/winning states, action buttons, emphasis |
| Yellow | `#ffff00` | `--arcade-yellow` | Marked squares, titles, accents |
| Blue | `#3366ff` | `--arcade-blue` | Unmarked squares, interactive elements |
| Cyan | `#00ffff` | `--arcade-cyan` | Instructions, secondary text, info |
| Green | `#00ff00` | `--arcade-green` | Free space center (alternative highlight) |
| White | `#ffffff` | `--arcade-white` | Borders, contrast elements, text on dark |

### Typography

| Font | Usage | CSS Class |
|------|-------|-----------|
| **Press Start 2P** (Google Fonts) | Headings, titles, pixel authenticity | `.text-3xl`, `.text-4xl`, `.text-5xl`, `.font-bold` |
| **Courier Prime** (Google Fonts) | Body text, instructions, monospace feel | Default body font, `.text-sm`, `.text-lg` |

**Implementation**:
```html
<!-- In base.html, fonts are imported from Google Fonts -->
<!-- Headings automatically use Press Start 2P via CSS rules -->
<h1 class="text-5xl font-bold text-arcade-yellow">SOC OPS</h1>

<!-- Body text uses Courier Prime -->
<p class="text-arcade-cyan">Instructions here</p>
```

### Component Styling Patterns

#### Buttons & Interactive Elements
```html
<!-- Arcade buttons have chunky 3D borders and press feedback -->
<button class="arcade-button" style="background-color: var(--arcade-red);">
    ► ACTION ◄
</button>
```

**Styling rules**:
- 4px solid white border (`.arcade-button` includes this)
- 4-6px drop shadow (simulates cabinet depth)
- Active state: transform `translate(4px, 4px)` with reduced shadow (press effect)
- Background colors: Red (#ff3333), Blue (#3366ff), or Yellow (#ffff00)

#### Bingo Board Squares
```html
<!-- Unmarked squares: Blue background, white border -->
<button style="
    background-color: var(--arcade-blue);
    border: 3px solid var(--arcade-white);
    color: var(--arcade-white);
    box-shadow: 2px 2px 0 var(--arcade-shadow);
">Question text</button>

<!-- Marked squares: Yellow background, black text -->
<button style="
    background-color: var(--arcade-yellow);
    border: 3px solid var(--arcade-white);
    color: var(--arcade-black);
    box-shadow: 3px 3px 0 var(--arcade-shadow);
">Question text</button>

<!-- Winning squares: Red background, yellow border, star marker -->
<button style="
    background-color: var(--arcade-red);
    border: 3px solid var(--arcade-yellow);
    color: var(--arcade-yellow);
    box-shadow: 4px 4px 0 var(--arcade-shadow);
">Question text
    <span style="position: absolute; top: 0.125rem; right: 0.125rem;">★</span>
</button>

<!-- Free space: Cyan background, white border, pixel font -->
<button disabled style="
    background-color: var(--arcade-cyan);
    border: 3px solid var(--arcade-white);
    color: var(--arcade-black);
    font-family: 'Press Start 2P', cursive;
    font-weight: bold;
    box-shadow: 3px 3px 0 var(--arcade-shadow);
">FREE SPACE</button>
```

#### Header & Navigation
```html
<!-- Yellow border header -->
<header style="border: 3px solid var(--arcade-yellow); background-color: var(--arcade-black);">
    <h1 class="text-5xl font-bold" style="color: var(--arcade-yellow); font-family: 'Press Start 2P', cursive;">SOC OPS</h1>
</header>

<!-- Cyan bordered back button -->
<button style="
    color: var(--arcade-yellow);
    border: 2px solid var(--arcade-yellow);
    background-color: transparent;
    font-family: 'Courier Prime', monospace;
    font-weight: bold;
">◄ BACK</button>
```

#### Information Boxes (Instructions, Messages)
```html
<!-- Chunky bordered box with arcade styling -->
<div class="arcade-border-thick" style="
    background-color: var(--arcade-black);
    border: 4px solid var(--arcade-white);
">
    <h2 class="font-bold" style="color: var(--arcade-white); font-family: 'Press Start 2P', cursive; font-size: 0.7rem;">HOW TO PLAY</h2>
    <ul style="color: var(--arcade-cyan); font-family: 'Courier Prime', monospace;">
        <li>► FIND PEOPLE WHO MATCH</li>
        <li>► TAP A SQUARE WHEN FOUND</li>
        <li>► GET 5 IN A ROW TO WIN!</li>
    </ul>
</div>
```

### Animations

| Animation | Trigger | Effect | Duration |
|-----------|---------|--------|----------|
| `arcade-shake` | Bingo modal appears | Screen shake (4px oscillation, 10 frames) | 0.6s |
| `arcade-flash` | Victory text | Color flash (yellow ↔ red) | 0.3s infinite |
| Button press | `:active` state | Transform translate + shadow reduction | 50ms |
| Scanline overlay | Page load | Subtle repeating lines (CRT effect) | N/A |

**Example**: Apply screen shake to bingo modal
```html
<div class="arcade-shake-modal" style="animation: arcade-shake 0.6s ease-in-out;">
    <h2 style="animation: arcade-flash 0.3s ease-in-out infinite;">BINGO!</h2>
</div>
```

### Design Consistency Checklist

When adding or modifying UI elements:
- ✅ All backgrounds use `var(--arcade-black)` (no white/gray backgrounds)
- ✅ All borders are 2-4px solid (no rounded corners, all 90° angles)
- ✅ All interactive elements have drop shadow (`box-shadow: Xpx Xpx 0 var(--arcade-shadow)`)
- ✅ Headings use Press Start 2P (`font-family: 'Press Start 2P', cursive`)
- ✅ Text uses high-contrast arcade colors (yellow on black, cyan on black, white on dark)
- ✅ Buttons include active/press state feedback (transform translate)
- ✅ Use ► and ◄ characters for arcade-style bullets/navigation
- ✅ Replace ✓ checkmarks with ★ stars for marked indicators
- ✅ No rounded corners or soft shadows (all arcade, all sharp)

### CSS Variable Reference

Access all arcade colors and effects via CSS variables in `app/static/css/app.css`:
```css
:root {
    --arcade-black: #0a0a0a;
    --arcade-red: #ff3333;
    --arcade-yellow: #ffff00;
    --arcade-blue: #3366ff;
    --arcade-cyan: #00ffff;
    --arcade-green: #00ff00;
    --arcade-white: #ffffff;
    --arcade-shadow: rgba(0, 0, 0, 0.9);
    --marked-yellow: #ffff00;
    --winning-red: #ff3333;
}
```

Use in templates: `style="color: var(--arcade-yellow);"`

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
