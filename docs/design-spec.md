# Card Deck Shuffle Mode - Design Spec

## Overview
New game mode where every player opens the game, taps, and gets a random card with a question. Builds on the existing Pixel Arcade aesthetic.

## Feature: Card Deck Shuffle

### Description
- Players start the game
- Each tap/interaction reveals a random card from the deck
- Each card displays a single question
- Cards are shuffled and appear one at a time
- Simple, quick interactions suited for icebreakers

### UX Flow
1. **Start Screen** → Add "CARD SHUFFLE" button alongside BINGO and HUNT modes (Red color for variety)
2. **Card Screen** → Clean card display with single question visible
3. **Tap Interaction** → Each tap shuffles to next card or shows a new one
4. **Back/Reset** → Option to return to start screen or shuffle through more cards

### Design Decisions
- Card as a full-screen visual element (not small)
- 3D flip animation on card reveal
- Rotating card colors (Blue → Red → Cyan → Yellow)
- Shimmer effect for visual polish
- Track cards shown (e.g., "Card 3 of 24")
- Endless mode — loops back to start after last card

### Visual Spec
- **Card Container**: 5px arcade borders with chunky shadows
- **Colors**: Rotating palette (Red, Yellow, Blue, Cyan)
- **Typography**: Press Start 2P for card questions
- **Animation**: 3D flip + shimmer on card reveal
- **Interaction**: Mouse press feedback on back button

### Implementation Complete ✅

#### 1. Backend Models (models.py)
- Added `GameMode.CARD_DECK` enum
- Added `CardData` model for card state

#### 2. Game Service (game_service.py)
- Added `cards` and `current_card_index` fields to `GameSession`
- Implemented `start_game_card_deck()` to initialize shuffled deck
- Added `get_next_card()` to advance through deck with looping
- Added `get_current_card()` to display active card

#### 3. API Routes (main.py)
- `POST /start-card-deck` → Initializes game, returns card_deck_screen
- `POST /next-card` → Advances to next card, returns updated screen

#### 4. Templates
- **start_screen.html** → Added CARD SHUFFLE button (red, arcade-styled)
- **card_deck_screen.html** → Full-screen card display with:
  - Rotating background colors
  - 3D flip animation on card reveal
  - Shimmer effect overlay
  - Back button and deck counter
  - Instruction text

#### 5. Styling & Animations
- `arcade-card-flip`: 3D rotation + scale animation
- `arcade-shine`: Shimmer effect across card
- Interactive button press feedback

### Status
- ✅ Core implementation complete
- ✅ All 62 tests passing
- ✅ Visual polish applied
- ✅ Ready for user testing & feedback

### Next Steps (Optional Features)
- [ ] Card categories filter (by theme)
- [ ] Difficulty levels (simple vs. complex questions)
- [ ] Card flip sound effects
- [ ] Multiplayer voting on cards
- [ ] Statistics tracking (cards shown, completion time)



