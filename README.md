# Keystone

Full-stack greeting application with BDD E2E testing.

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

## Development

### Backend

```bash
cd backend
uv sync --dev
uv run uvicorn main:app --reload --port 8000
```

Run unit tests:
```bash
cd backend
uv run pytest -v
```

### Frontend

```bash
cd frontend
npm install
npm start  # Runs on http://localhost:4200, proxies /api to backend
```

The frontend uses a proxy configuration to route `/api/*` requests to `http://localhost:8000` during development.

Run unit tests:
```bash
cd frontend
npm test
```

### E2E Tests

#### Option 1: Using Docker Compose (Recommended)

```bash
# Start services
docker-compose up -d

# Run E2E tests
cd e2e
uv sync
uv run playwright install chromium
uv run behave

# Stop services
docker-compose down
```

#### Option 2: Manual

Terminal 1:
```bash
cd backend
uv run uvicorn main:app --port 8000
```

Terminal 2:
```bash
cd frontend
npm start
```

Terminal 3:
```bash
cd e2e
uv sync
uv run playwright install chromium
uv run behave
```

## CI/CD

GitHub Actions pipeline runs:
1. Backend unit tests
2. Frontend unit tests
3. E2E BDD tests (after both pass)

## Testing Philosophy

**Unit tests** (pytest/Jasmine): Technical edge cases, validation, internal logic

**BDD E2E tests** (behave + Playwright): User workflows through UI, stakeholder validation scenarios

BDD tests are written in Gherkin (plain English) for stakeholder collaboration on acceptance criteria.
