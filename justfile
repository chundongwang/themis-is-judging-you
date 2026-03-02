# Country Simulator — task runner
# https://github.com/casey/just

# Default: list available recipes
default:
    @just --list

# Run frontend and backend concurrently (split panes via tmux)
dev:
    tmux new-session -d -s dev -x 220 -y 50
    tmux send-keys -t dev "cd {{justfile_directory()}}/backend && uv run python -m uvicorn app.main:app --reload --port 8000 --workers 1" Enter
    tmux split-window -h -t dev
    tmux send-keys -t dev "cd {{justfile_directory()}}/frontend && npm run dev" Enter
    tmux attach -t dev

# Start only the backend dev server
[working-directory: 'backend']
backend:
    uv run python -m uvicorn app.main:app --reload --port 8000 --workers 1

# Start only the frontend dev server
frontend:
    npm run --prefix frontend dev

# Install all dependencies (frontend npm + backend uv sync)
[working-directory: 'backend']
install:
    npm install --prefix ../frontend
    uv sync

# Seed the database with fixture data
[working-directory: 'backend']
seed:
    uv run python -m scripts.seed

# Build the frontend for production
build:
    npm run --prefix frontend build

# Lint the frontend
lint:
    npm run --prefix frontend lint

# Run a database migration (pass message as argument)
# Usage: just migrate "describe your change"
[working-directory: 'backend']
migrate message:
    uv run alembic revision --autogenerate -m "{{message}}"

# Apply pending migrations
[working-directory: 'backend']
migrate-up:
    uv run alembic upgrade head
