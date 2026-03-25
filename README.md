# 🎉 Soc Ops

> **The interactive Social Bingo game that breaks the ice at any mixer!** Find people who match quirky questions, mark your bingo card, and be first to get 5 in a row. Built with AI-assisted development to showcase modern web development workflows.

---

## ✨ What's This About?

Soc Ops is an **educational lab project** that demonstrates how to build full-stack web applications using **GitHub Copilot and AI agents**. The game itself is fun and interactive—but the real magic is in how it's built: a masterclass in test-driven development, agent collaboration, and context engineering.

**Perfect for:**
- 🎓 Learning AI-assisted development workflows
- 🏗️ Understanding modern Python web architecture (FastAPI + HTMX)
- 🤖 Exploring multi-agent development patterns
- 🎮 Building and customizing interactive games

---

## 🎮 Features

- **Interactive Bingo Board** — 5×5 grid with randomized questions
- **No Page Reloads** — Smooth HTMX interactions for desktop and mobile
- **Instant Game Detection** — Auto-detects bingo (horizontal, vertical, diagonal)
- **Customizable Questions** — Easily swap in your own icebreaker prompts
- **Responsive Design** — Works great on any device
- **Built for Education** — Clean, documented code patterns throughout

---

## 🛠️ Tech Stack

```
FastAPI          →  Modern Python web framework
HTMX             →  No-build interactive frontend
Jinja2           →  Server-side templating
Pydantic         →  Type-safe data models
pytest           →  Comprehensive test suite
ruff             →  Lightning-fast linting
```

---

## 🚀 Quick Start

```bash
# Clone and install
git clone <repo>
cd my-soc-ops-python
uv sync

# Run dev server
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
uv run pytest

# Lint code
uv run ruff check .
```

Then open **http://localhost:8000** in your browser and start playing!

---

## 📚 Learning Lab Guide

Dive into **5 structured parts** that walk you through building and extending this project:

| Part | Title | Learning Focus |
|------|-------|---|
| [**00**](https://copilot-dev-days.github.io/agent-lab-python/docs/step.html?step=00-overview) | Overview & Checklist | Project setup & prerequisites |
| [**01**](https://copilot-dev-days.github.io/agent-lab-python/docs/step.html?step=01-setup) | Setup & Context Engineering | Copilot workspace setup & prompts |
| [**02**](https://copilot-dev-days.github.io/agent-lab-python/docs/step.html?step=02-design) | Design-First Frontend | Building HTMX components smartly |
| [**03**](https://copilot-dev-days.github.io/agent-lab-python/docs/step.html?step=03-quiz-master) | Custom Quiz Master | Creating a specialized AI agent |
| [**04**](https://copilot-dev-days.github.io/agent-lab-python/docs/step.html?step=04-multi-agent) | Multi-Agent Development | Orchestrating multiple agents together |

> 📝 **Prefer offline reading?** All guides are in the [`workshop/`](workshop/) folder.

---

## 📂 Project Structure

```
app/
├── main.py           # FastAPI routes & HTMX endpoints
├── models.py         # Pydantic data models
├── game_logic.py     # Core game mechanics
├── game_service.py   # Session management
├── data.py           # Question bank
├── templates/        # Jinja2 templates (server-rendered)
└── static/           # CSS & HTMX lib (no build step!)

tests/
├── test_api.py       # FastAPI endpoint tests
└── test_game_logic.py # Unit tests
```

---

## 🎯 Getting Started Now

👉 **[Head to Part 00: Overview](https://copilot-dev-days.github.io/agent-lab-python/docs/step.html?step=00-overview)** to check prerequisites and begin the lab.

Or jump straight in with `uv sync` + `uv run uvicorn ...` above!

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on improving the game, adding features, or fixing bugs.

---

## 📜 License & Code of Conduct

- **License:** See [LICENSE](LICENSE)
- **Security:** See [SECURITY.md](SECURITY.md)
- **Code of Conduct:** See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

---

## ❓ Need Help?

Check [SUPPORT.md](SUPPORT.md) for troubleshooting and FAQ.
