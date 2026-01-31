# List available recipes
default:
    @just --list

# =============================================================================
# Development
# =============================================================================

# Start services with Docker Compose
# Examples:
#   just dev          # Foreground with logs
#   just dev -d       # Background (detached)
#   just dev --build  # Rebuild images first
dev +FLAGS="":
    docker compose up {{FLAGS}}

# Stop all services
# Examples:
#   just down    # Stop services
#   just down -v # Stop and remove volumes
down +FLAGS="":
    docker compose down {{FLAGS}}

# View service logs
# Examples:
#   just logs              # All services, follow mode
#   just logs backend      # Single service
#   just logs backend -n 50  # Last 50 lines
logs service="" +FLAGS="-f":
    @if [ -z "{{service}}" ]; then \
        docker compose logs {{FLAGS}}; \
    else \
        docker compose logs {{FLAGS}} {{service}}; \
    fi

# Run backend dev server (without Docker)
dev-backend:
    cd backend && uv run uvicorn main:app --reload --port 8000

# Run frontend dev server (without Docker)
dev-frontend:
    cd frontend && npm start

# =============================================================================
# Testing
# =============================================================================

# Run all tests (unit + E2E)
test: test-backend test-frontend e2e-headless

# Run backend unit tests
# Examples:
#   just test-backend           # All tests with coverage
#   just test-backend -k hello  # Filter by name with coverage
#   just test-backend --no-cov  # Skip coverage (faster iteration)
test-backend +FLAGS="-v":
    cd backend && uv run pytest {{FLAGS}}

# Run frontend unit tests
# Examples:
#   just test-frontend       # Run all tests with coverage
#   just test-frontend --ui  # Run with UI
test-frontend +FLAGS="":
    cd frontend && npm test {{FLAGS}}

# Run E2E tests (requires services running: just dev -d)
# Examples:
#   just dev -d && just e2e      # Start services, then test
#   just e2e                     # Headless mode
#   just e2e false               # With visible browser
#   just e2e true --tags=@smoke  # Headless with tags
#   SCREENSHOT_STEPS=then just e2e   # Screenshot "Then" steps (default)
#   SCREENSHOT_STEPS=all just e2e    # Screenshot every step
#   SCREENSHOT_STEPS=false just e2e  # No step screenshots
e2e headless="true" +FLAGS="":
    cd e2e && HEADLESS={{headless}} uv run behave {{FLAGS}}

# Shortcut for headless E2E tests
e2e-headless: (e2e "true")

# Shortcut for headed E2E tests
e2e-headed: (e2e "false")

# Run E2E tests and generate PDF report for change management
# Examples:
#   just e2e-pdf              # Generate PDF report
#   just e2e-pdf false        # With visible browser
e2e-pdf headless="true":
    #!/usr/bin/env bash
    set -e
    mkdir -p e2e/reports
    cd e2e
    HEADLESS={{headless}} uv run behave \
        --format json \
        --outfile reports/behave-results.json \
        --format pretty
    uv run python generate_pdf_report.py
    cd ..
    echo "PDF report generated: e2e/reports/test-report.pdf"

# =============================================================================
# Installation
# =============================================================================

# Install all dependencies
install: install-backend install-frontend install-e2e

# Install backend dependencies
install-backend:
    cd backend && uv sync --dev

# Install frontend dependencies
install-frontend:
    cd frontend && npm ci

# Install E2E dependencies and Playwright
install-e2e:
    cd e2e && uv sync && uv run playwright install chromium

# =============================================================================
# Maintenance
# =============================================================================

# Clean up Docker resources and build artifacts
# Examples:
#   just clean  # Remove build artifacts and containers
clean:
    docker compose down -v
    rm -rf backend/.venv backend/__pycache__ backend/.pytest_cache backend/.coverage backend/htmlcov backend/coverage.lcov backend/coverage.json
    rm -rf frontend/node_modules frontend/dist frontend/.angular frontend/coverage
    rm -rf e2e/.venv e2e/reports e2e/screenshots

# Rebuild Docker images
# Examples:
#   just rebuild         # No cache rebuild
#   just rebuild --pull  # Pull base images first
rebuild +FLAGS="--no-cache":
    docker compose build {{FLAGS}}

# =============================================================================
# Linting and Formatting
# =============================================================================

# Run all linters (check only, no auto-fix)
lint: lint-backend lint-frontend

# Run all formatters (auto-fix)
fmt: fmt-backend fmt-frontend

# Lint backend Python code (check only)
lint-backend:
    @echo "Linting backend..."
    cd backend && uv run ruff check .
    @echo "Linting e2e..."
    cd e2e && uv run ruff check .

# Lint frontend TypeScript/Angular code (check only)
lint-frontend:
    @echo "Checking Prettier formatting..."
    cd frontend && npm run format:check
    @echo "Running ESLint..."
    cd frontend && npm run lint

# Format backend Python code (auto-fix)
fmt-backend:
    @echo "Formatting backend..."
    cd backend && uv run ruff format . && uv run ruff check --fix .
    @echo "Formatting e2e..."
    cd e2e && uv run ruff format . && uv run ruff check --fix .

# Format frontend code (auto-fix)
fmt-frontend:
    @echo "Running Prettier..."
    cd frontend && npm run format
    @echo "Running ESLint --fix..."
    cd frontend && npm run lint:fix

# Install pre-commit hooks (one-time setup)
pre-commit-install:
    @command -v pre-commit >/dev/null 2>&1 || { echo "Installing pre-commit..."; pip install pre-commit; }
    pre-commit install
    @echo "Pre-commit hooks installed successfully"
