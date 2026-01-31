# Contributing to Keystone

This guide covers the practical steps for contributing to this project. For background on the practices and principles demonstrated here, see [OVERVIEW.md](OVERVIEW.md).

## Pull Request Workflow

### 1. Create an Issue First
All PRs should link to an existing issue. Use the appropriate issue template:
- **Bug**: For fixes
- **Feature**: For new functionality
- **Task**: For chores, refactoring, dependencies

### 2. Branch Naming
```
issue/<issue-number>-<short-description>
```

Example: `issue/42-add-user-authentication`

### 3. Commit Signing

All commits must be cryptographically signed. See [GitHub's commit signing documentation](https://docs.github.com/en/authentication/managing-commit-signature-verification) for setup instructions.

### 4. Pre-commit Hooks (Optional but Recommended)

Pre-commit hooks automatically format and lint your code before each commit.

**One-time setup:**
```bash
just pre-commit-install
```

**What it does:**
- Runs Ruff formatter and linter on Python files
- Runs Prettier and ESLint on frontend files
- Checks for trailing whitespace, merge conflicts, large files
- Auto-fixes most issues (re-stage files after fixes)

**Manual formatting:**
```bash
# Format all code (auto-fix)
just fmt

# Check linting without auto-fix (same as CI)
just lint
```

**CI Requirements:**
- All PRs must pass linting checks
- If linting fails, run `just fmt` locally and push changes

### 5. Commit Conventions
Follow conventional commit format:
```
type(scope): description

Examples:
feat(auth): add login endpoint
fix(ui): correct button alignment
deps(python): update fastapi to 0.115.0
```

Types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `deps`

### 6. Before Submitting PR
- Run tests locally: `just test`
- Run linters: `just lint` (or install pre-commit hooks)
- Fix any linting issues: `just fmt`
- Ensure commits are signed
- Link PR to issue: Use "Closes #123" in PR description

### 7. PR Requirements
- All CI checks must pass (lint, backend tests, frontend tests, E2E tests)
- Linear history required (squash or rebase merges only)
- No direct pushes to main
- Branch must be up to date with main before merging

See [OVERVIEW.md](OVERVIEW.md#branch-protection) for details on branch protection settings.

## Automated Dependency Updates (Dependabot)

### How It Works
Dependabot automatically creates PRs for dependency updates:
- **Schedule**: Every Monday
- **Grouping**: Minor and patch updates grouped together, major updates separate
- **Testing**: CI runs automatically on all Dependabot PRs

### Reviewing Dependabot PRs

**For patch and minor updates**:
1. Check that CI passes (green checkmarks)
2. Review changelog/release notes (linked in PR description)
3. Merge if no breaking changes

**For major version updates**:
1. Review breaking changes carefully
2. Test locally if needed
3. Update code to handle breaking changes
4. Merge when ready

### Skipping Updates
If an update isn't needed:
1. Close the PR with a comment explaining why
2. Dependabot will stop creating PRs for that version
3. Can reopen later if needed

### PR Title Format
Dependabot PRs follow conventional commits:
- `deps(python): update package-name from 1.0.0 to 1.1.0`
- `deps(npm): update package-name from 2.0.0 to 3.0.0`
- `deps(actions): update action-name from v1 to v2`

## Testing

### Running Tests Locally
```bash
# All tests
just test

# Backend unit tests only
just test-backend

# Frontend unit tests only
just test-frontend

# E2E tests with visible browser
just e2e-headed

# E2E tests with PDF report
just e2e-pdf
```

### Test Requirements
- All new features require tests
- Bug fixes should include regression tests using Gherkin format from issue
- Feature acceptance criteria should convert directly to E2E tests

## Questions?
For questions, ideas, or discussions, please open an issue using the appropriate template.
