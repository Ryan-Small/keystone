# Keystone

Full-stack greeting application with BDD E2E testing.

## Prerequisites

- [just](https://github.com/casey/just) - Command runner
  ```bash
  # macOS
  brew install just

  # Linux
  curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to /usr/local/bin

  # Or via cargo
  cargo install just
  ```
- Docker & Docker Compose
- Python 3.14+ (for local development without Docker)
- Node.js 20+ (for local development without Docker)

## Structure

```
keystone/
├── backend/              # FastAPI backend
├── frontend/             # Angular frontend
├── e2e/                  # BDD E2E tests (Playwright + Behave)
│   ├── features/
│   └── pyproject.toml
└── .github/workflows/    # CI pipeline
```

## Quick Start

```bash
# Install dependencies
just install

# Start development environment with Docker
just dev

# Run all tests
just test

# Run E2E tests with visible browser
just e2e

# See all available commands
just --list
```

## Development

### Using Docker (Recommended)

```bash
just dev              # Start all services
just logs             # View all logs
just logs backend     # View backend logs only
just down             # Stop services
```

### Manual Setup

#### Backend

```bash
just install-backend
just dev-backend      # Runs on http://localhost:8000
```

Or manually:
```bash
cd backend
uv sync --dev
uv run uvicorn main:app --reload --port 8000
```

Run unit tests:
```bash
just test-backend
```

#### Frontend

```bash
just install-frontend
just dev-frontend     # Runs on http://localhost:4200, proxies /api to backend
```

Or manually:
```bash
cd frontend
npm install
npm start
```

The frontend uses a proxy configuration to route `/api/*` requests to `http://localhost:8000` during development.

Run unit tests:
```bash
just test-frontend
```

### E2E Tests

```bash
# With Docker (recommended)
just dev -d           # Start services in background
just e2e              # Run with visible browser
just e2e-headless     # Run headless
just e2e-report       # Run with HTML report
just down             # Stop services

# Manual (requires backend + frontend running)
just e2e

# Advanced options
just e2e                        # Screenshots "Then" steps by default
SCREENSHOT_STEPS=all just e2e   # Screenshot every step (debugging)
SCREENSHOT_STEPS=false just e2e # No step screenshots
```

**Screenshots & Reports:**
- Screenshots automatically captured on test failures → `e2e/screenshots/`
- "Then" step screenshots captured by default (configurable with `SCREENSHOT_STEPS`)
- **PDF reports for change management**: `just e2e-pdf`
  - Professional PDF with title page, test summary, and sign-off section
  - Screenshots embedded with each scenario
  - Single file ready to attach to change requests
  - Output: `e2e/reports/test-report.pdf`
- CI uploads PDF report as artifact (30-day retention)

## CI/CD

GitHub Actions pipeline runs:
1. Backend unit tests
2. Frontend unit tests
3. E2E BDD tests (after both pass)

## Testing Philosophy

**Unit tests** (pytest/Jasmine): Technical edge cases, validation, internal logic

**BDD E2E tests** (behave + Playwright): User workflows through UI, stakeholder validation scenarios

BDD tests are written in Gherkin (plain English) for stakeholder collaboration on acceptance criteria.
