@ECHO OFF
REM Diamond-Patterns (c) Ian Dennis Miller
REM This is a Windows batch file for launching diamond-patterns
REM The script assumes you are using a python virtualenv.

REM First, we'll echo the command for debugging purposes
echo %VIRTUAL_ENV%\scripts\python.exe %VIRTUAL_ENV%\scripts\diamond %*

REM Finally, we will execute the command
%VIRTUAL_ENV%\scripts\python.exe %VIRTUAL_ENV%\scripts\diamond %*
