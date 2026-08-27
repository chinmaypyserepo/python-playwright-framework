@echo off
setlocal

set "BROWSER=%~1"
if "%BROWSER%"=="" set "BROWSER=chromium"

set "MARKERS=%~2"
if "%MARKERS%"=="" set "MARKERS=smoke"

set "HEADLESS=false"
set "BROWSER=%BROWSER%"
python -m pytest -m "%MARKERS%" --browser "%BROWSER%" --alluredir allure-results
