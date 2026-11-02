@echo off
cd /d "%~dp0"
start http://localhost:5175/
python -m http.server 5175
