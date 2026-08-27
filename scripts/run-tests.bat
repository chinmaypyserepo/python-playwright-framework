@echo off
setlocal

set "BROWSER=%~1"
if "%BROWSER%"=="" set "BROWSER=chromium"

set "MARKERS=%~2"
if "%MARKERS%"=="" set "MARKERS=smoke"

set "MODE=%~3"
if "%MODE%"=="" set "MODE=headed"

set "HEADLESS=false"
if /I "%MODE%"=="headless" set "HEADLESS=true"
set "BROWSER=%BROWSER%"
python -m pytest -m "%MARKERS%" --browser "%BROWSER%" --alluredir allure-results
