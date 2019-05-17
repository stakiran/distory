@echo off
setlocal
set todaydate=%date%
set todaydate=%todaydate:/=%
set todaydate=%todaydate:~2,6%

set PROFILE_NAME=XXXXXXXX.YYYYYYYY

python distory.py --bookmark -p %PROFILE_NAME% -d %todaydate%
python distory.py --bookmark -p %PROFILE_NAME% -d %todaydate% --md
python distory.py -p %PROFILE_NAME% -d %todaydate%
python distory.py -p %PROFILE_NAME% -d %todaydate% --md
