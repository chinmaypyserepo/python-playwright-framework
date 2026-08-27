# PyPlaywrightFramework

An interview-ready example framework for [automationintesting.online](https://automationintesting.online/) using Python, Pytest, Playwright, Page Object Model, API checks, JSON data, Allure, SQLite, and GitHub Actions.

## Architecture

```text
conftest.py             shared fixtures and Allure/browser evidence
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

## Run tests (Windows)

Headed mode is the default:

```bat
python -m pytest -m smoke --browser chromium --alluredir allure-results
```

Headless mode:

```bat
python -m pytest -m smoke --browser chromium --headless --alluredir allure-results
```

Run by marker:

```bat
python -m pytest -m ui --browser chromium
python -m pytest -m api --browser chromium
python -m pytest -m smoke --browser chromium
```

Run all normal tests:

```bat
python -m pytest --browser chromium --alluredir allure-results
```

Run the intentional failure:

```bat
python -m pytest -m intentional_failure --browser chromium --headless --alluredir allure-results
```

Run one test:

```bat
python -m pytest tests/test_ui_home.py::test_runtime_contact_data_submission --browser chromium
```

Run Firefox or WebKit headlessly:

```bat
python -m pytest -m smoke --browser firefox --headless
python -m pytest -m smoke --browser webkit --headless
```

## Allure and artifacts

Every UI test creates a screenshot, video, and trace. Old artifacts are removed at the start of each run.

```bat
allure serve allure-results
playwright show-trace test-results\traces\<test-name>.zip
```

## Git

```bat
git status
git pull origin main
git add .
git commit -m "Describe your change"
git push origin main
git log --oneline -10
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
