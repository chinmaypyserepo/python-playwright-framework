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

Windows runs headless by default:

```bat
scripts\run-tests.bat chromium smoke
```

To run headed, use this command:

```bat
set HEADLESS=false
python -m pytest -m smoke --browser chromium
```

Direct Pytest commands:

```bat
# Headless, all tests
set HEADLESS=true
python -m pytest --browser chromium --alluredir allure-results

# Headed, one test file
set HEADLESS=false
python -m pytest tests/test_ui_home.py --browser chromium -s

# Run by marker
python -m pytest -m ui --browser chromium
python -m pytest -m api --browser chromium

# Run one test by name
python -m pytest -k "contact_form_submission" --browser chromium -s

# Run Firefox or WebKit
python -m pytest -m smoke --browser firefox
python -m pytest -m smoke --browser webkit

# Run in parallel (use isolated test data for write-heavy suites)
python -m pytest -m smoke --browser chromium -n 2
```

Useful diagnostics:

```text
# Show collection without executing tests
python -m pytest --collect-only -q

# Open the latest Allure report
allure serve allure-results

# Inspect a failed Playwright trace
playwright show-trace test-results/traces/<test-name>.zip

# Remove generated local results
rmdir /s /q test-results
rmdir /s /q allure-results
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
