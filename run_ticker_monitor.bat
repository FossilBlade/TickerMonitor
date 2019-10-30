@ECHO OFF

set PYTHONPATH=%PYTHONPATH%;%CD%

ECHO Running the ticker_monitor script.
venv\Scripts\python script\ticker_monitor.py