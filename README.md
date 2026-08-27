# PyPlaywrightFramework

An interview-ready example framework for [automationintesting.online](https://automationintesting.online/) using Python, Pytest, Playwright, Page Object Model, API checks, JSON data, Allure, SQLite, and GitHub Actions.

## Architecture

```text
config/                 typed .env-backed settings
test_framework/         API client, retry, logging, SQLite persistence
pages/                  Page Object Model
data/                   JSON-driven test data
tests/                  UI/API, validation, date-picker and dialog tests
scripts/                Windows batch and bash entry points
.github/workflows/      Chromium, Firefox and WebKit CI matrix
```

## Setup

```text
python -m venv .venv
.venv\Scripts\activate.bat
pip install .
copy .env.example .env
playwright install
```

Run smoke tests:

```bat
scripts\run-tests.bat chromium smoke
scripts\run-tests.bat firefox smoke
scripts\run-tests.bat webkit smoke
```

```bash
./scripts/run-tests.sh chromium smoke
```

## Day-to-day commands

### Run tests on Windows

```bat
# Headed Chromium smoke tests
scripts\run-tests.bat chromium smoke

# Headless Chromium smoke tests
scripts\run-tests.bat chromium smoke headless

# Headed Firefox/WebKit smoke tests
scripts\run-tests.bat firefox smoke
scripts\run-tests.bat webkit smoke

# All tests, headed
scripts\run-tests.bat chromium all

# All tests, headless
scripts\run-tests.bat chromium all headless
```

Available markers are `smoke`, `ui`, `api`, or `all`.

### Allure report

```bat
# Generate results (the test runner already does this)
scripts\run-tests.bat chromium smoke headed

# Open the report
allure serve allure-results
```

### Git commands

```bat
# Check current branch and changes
git status
git branch

# Get latest GitHub changes
git pull origin main

# See changed files
git diff

# Save changes
git add .
git commit -m "Describe your change"

# Upload to GitHub
git push origin main

# View recent commits
git log --oneline -10
```

Useful diagnostics:

```bat
# Show collection without executing tests
scripts\run-tests.bat chromium smoke headed

# Open the latest Allure report
allure serve allure-results

# Inspect a failed Playwright trace
playwright show-trace test-results/traces/<test-name>.zip

# Remove generated local results
rmdir /s /q test-results 2>nul
rmdir /s /q allure-results 2>nul
```

On Linux/macOS, use the equivalent runner:

```bash
./scripts/run-tests.sh chromium smoke                 # headless
HEADLESS=false ./scripts/run-tests.sh chromium smoke # headed
python -m pytest -m ui --browser chromium -s
```

Run all tests and generate an Allure report:

```bat
python -m pytest --browser chromium --alluredir allure-results
allure serve allure-results
```

Failures produce a full-page screenshot, Playwright trace ZIP, video, log file, and SQLite row under `test-results/`. Open a trace with `playwright show-trace test-results/traces/<test>.zip`.

## Design choices

- **POM:** selectors and user actions stay in `pages/`; tests describe behavior.
- **Data separation:** mutable test values live in JSON and can be replaced by a data factory.
- **Fixtures:** browser contexts are isolated per test, with tracing/video configured centrally.
- **Reliability:** explicit timeouts, limited exponential retry for connection/timeouts, and no retry of assertions.
- **Observability:** standard logging, Allure attachments, failure artifacts, and SQLite run history.
- **Cross-browser:** the same suite runs against Chromium, Firefox, and WebKit via the Playwright plugin.
- **Interactions:** date-picker month navigation, server-side validation, native alert acceptance, and reusable dropdown selection are covered with readable POM methods.

## Honest demo-site limitations

This is a public demo application, not a test-owned environment. Data and copy can change, concurrent users can affect availability, and it may be rate-limited or temporarily unavailable. The API suite validates the room collection shape but does not make a dedicated room-detail lookup a gate because no room ID is a stable contract. The site currently uses a custom date picker and server-side validation; it does not expose a meaningful business dropdown or native alert in the tested flows, so the framework includes a reusable `select_option` helper and an isolated alert-handling capability test rather than pretending the demo has those controls. API endpoint availability and UI wording should be revalidated before using this as a production gate. A production framework should provision isolated data, use secrets from CI, and replace the demo with a controlled environment.

## Interview talking points

Explain fixture scopes, why contexts are isolated, why retries exclude assertion failures, how traces diagnose flakiness, why API tests complement UI tests, and how the SQLite repository could be replaced by a reporting service without changing tests.
