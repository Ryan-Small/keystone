# Project Overview

Keystone is an example project demonstrating production-grade software development practices. It showcases industry best practices from the DevOps Handbook, Google's engineering practices, and behavior-driven development (BDD).

## Purpose

This project serves as a reference implementation for:
- BDD workflows with Gherkin and automated testing
- CI/CD pipeline design with quality gates
- Branch protection and code review practices
- Automated dependency management
- Production deployment planning

## Architecture

**Stack:**
- **Backend**: FastAPI (Python 3.14)
- **Frontend**: Angular 17 with TypeScript
- **Testing**: Behave (BDD), pytest (unit), Playwright (E2E)
- **Infrastructure**: Docker Compose, GitHub Actions
- **Task Runner**: just (command standardization)

**Monorepo Structure:**
```
backend/     - FastAPI application
frontend/    - Angular application
e2e/         - BDD scenarios and E2E tests
docs/        - Project documentation
.github/     - Issue templates, PR template, CI workflows
```

## Behavior-Driven Development (BDD)

### Issue Templates with Gherkin

All issues (bugs, features) use Gherkin format to describe behavior:

**Bug reports** define current vs expected behavior:
```gherkin
Current Behavior:
  Given a user is on the login page
  When they submit an empty form
  Then they see a validation error

Expected Behavior:
  Given a user is on the login page
  When they submit an empty form
  Then they see "Username is required"
```

**Features** define acceptance criteria:
```gherkin
Scenario: User logs in successfully
  Given a user with valid credentials
  When they submit the login form
  Then they are redirected to the dashboard
```

### Why Gherkin?

- **Traceability**: Issue → Test → Code in one format
- **Stakeholder communication**: Non-technical stakeholders can write/review scenarios
- **Regression prevention**: Bug scenarios become regression tests
- **Living documentation**: Tests document expected behavior

### Test Pyramid

```
       E2E (BDD)           <- Stakeholder scenarios, full system
      /         \
   Frontend    Backend     <- Component tests, integration
  /                    \
Unit                  Unit <- Fast, isolated tests
```

E2E tests generate PDF reports with screenshots for change management approval.

## Branch Protection

The `main` branch enforces quality gates before merge:

**Require pull request before merging**
- Prevents direct commits to main
- Creates audit trail for all changes
- Ensures code review happens

**Require status checks to pass**
- Required: `backend-tests`, `frontend-tests`, `e2e-tests`
- Prevents broken code from merging
- Automated quality gates

**Require linear history**
- Enforces squash or rebase merges
- Clean, readable git history
- Easier to bisect and revert

**Require branches to be up to date**
- Prevents integration conflicts
- Tests run against latest code
- Reduces "works on my branch" issues

**Require signed commits**
- Cryptographic proof of commit authorship
- Prevents commit spoofing and impersonation
- Supply chain security best practice
- Commits verified via GPG or SSH signatures

### DevOps Handbook Principles

These protections align with:
- **Small batch sizes**: PRs are focused changes
- **Fast feedback**: CI fails fast on quality issues
- **Automated quality gates**: No manual approval for objective checks
- **Continuous integration**: Every change tested against main

## CI/CD Pipeline

### Three-Stage Pipeline

```
backend-tests ──┐
                ├──> e2e-tests
frontend-tests ─┘
```

**Stage 1: Unit Tests (Parallel)**
- Backend: pytest with FastAPI test client
- Frontend: Vitest component tests
- Fast feedback (< 1 minute)

**Stage 2: E2E Tests (Sequential)**
- Requires both unit test stages to pass
- Full system testing with Docker Compose
- Behave scenarios with Playwright
- Generates PDF report with screenshots
- Uploads artifacts (PDF 30 days, screenshots 7 days)

### Why This Structure?

- **Fail fast**: Unit tests catch most issues quickly
- **Resource efficiency**: E2E only runs if units pass
- **Comprehensive**: Full coverage from unit to system level
- **Audit trail**: PDF reports for compliance/change management

## Dependency Management

### Dependabot Configuration

Automated dependency updates with strategic grouping:

**Python (backend + e2e):**
- Weekly updates on Mondays
- Minor/patch updates grouped together
- Major updates separate (breaking changes)

**npm (frontend):**
- Weekly updates on Mondays
- Angular packages always grouped (must stay in sync)
- Other packages grouped by minor/patch
- TypeScript separate (tested for Angular compatibility)

**GitHub Actions:**
- Weekly updates on Mondays
- Keep CI actions current

### Why This Strategy?

- **Security**: Automated CVE notifications within hours
- **Reduced noise**: Grouping prevents PR spam
- **Safe majors**: Breaking changes reviewed individually
- **Ecosystem sync**: Angular packages upgrade atomically
- **CI validation**: All updates tested before human review

## Pull Request Workflow

### Template Structure

PRs document:
1. **Context**: Why this change, link to issue
2. **Implementation**: How it works, architectural decisions
3. **Deployment Plan**: Migrations, config changes, rollback
4. **Risks & Mitigations**: Breaking changes, performance, security

### Why This Structure?

- **Knowledge transfer**: Decisions documented before merge
- **Deployment safety**: Plan captured upfront
- **Risk awareness**: Problems surfaced early
- **Reviewer guidance**: Clear context for review

## Future Phases

This project demonstrates foundational practices. Planned additions:

**Phase 2: Database + Migrations**
- PostgreSQL with Alembic migrations
- Seed data for development
- Migration testing in CI

**Phase 3: Ephemeral PR Environments**
- Preview environment per PR
- Database provisioning per environment
- Automated cleanup on PR close

**Phase 4: Production Deployment**
- Staging auto-deploy on main merge
- Production deploy via git tags
- Rollback mechanisms
- Infrastructure as Code (Terraform for ECS)

## References

This project draws from:
- **The DevOps Handbook** (Kim, Humble, Debois, Willis)
- **Google's Software Engineering Practices**
- **Behavior-Driven Development** (Cucumber/Behave)
- **Conventional Commits** specification
- **Semantic Versioning** principles

## Questions?

For questions about these practices, open a discussion issue or reach out to the maintainers.
