#!/usr/bin/env bash
set -euo pipefail
BROWSER="${1:-chromium}"
MARKERS="${2:-smoke}"
HEADLESS="${HEADLESS:-true}" BROWSER="$BROWSER" python -m pytest -m "$MARKERS" --browser "$BROWSER" --alluredir allure-results
