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
#   just test-backend           # All tests
#   just test-backend -k hello  # Filter by name
#   just test-backend -vv       # Very verbose
test-backend +FLAGS="-v":
    cd backend && uv run pytest {{FLAGS}}

# Run frontend unit tests
# Examples:
#   just test-frontend       # Run all tests
#   just test-frontend --ui  # Run with UI
test-frontend +FLAGS="":
    cd frontend && npm test {{FLAGS}}

# Run E2E tests (requires services running: just dev -d)
# Examples:
#   just dev -d && just e2e      # Start services, then test
#   just e2e                     # Headless mode
#   just e2e false               # With visible browser
#   just e2e true --tags=@smoke  # Headless with tags
e2e headless="true" +FLAGS="":
    cd e2e && HEADLESS={{headless}} uv run behave {{FLAGS}}

# Shortcut for headless E2E tests
e2e-headless: (e2e "true")

# Shortcut for headed E2E tests
e2e-headed: (e2e "false")

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
    rm -rf backend/.venv backend/__pycache__ backend/.pytest_cache
    rm -rf frontend/node_modules frontend/dist frontend/.angular
    rm -rf e2e/.venv e2e/reports e2e/screenshots

# Rebuild Docker images
# Examples:
#   just rebuild         # No cache rebuild
#   just rebuild --pull  # Pull base images first
rebuild +FLAGS="--no-cache":
    docker compose build {{FLAGS}}

# Run linter/formatter (placeholder for future)
lint:
    @echo "Linting not yet configured"
