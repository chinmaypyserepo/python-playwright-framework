#!/usr/bin/env bash
set -euo pipefail
BROWSER="${1:-chromium}"
MARKERS="${2:-smoke}"
BROWSER="$BROWSER" python -m pytest -m "$MARKERS" --browser "$BROWSER" --alluredir allure-results

