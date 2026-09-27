@echo off

cd /d "C:\Users\rushi\OneDrive\Desktop\AIML PROJECT\stock-market-agent"

set PYTHONIOENCODING=utf-8

echo ======================================== >> task_scheduler.log
echo Run started at %date% %time% >> task_scheduler.log

"C:\Users\rushi\OneDrive\Desktop\AIML PROJECT\stock-market-agent\venv\Scripts\python.exe" run_daily_report.py >> task_scheduler.log 2>&1

echo Exit code: %ERRORLEVEL% >> task_scheduler.log
echo Run ended at %date% %time% >> task_scheduler.log
echo ======================================== >> task_scheduler.log