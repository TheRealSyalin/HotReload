@echo off

if "%~1"=="run" @start HotReload.exe %2
if "%~1"=="stop" @taskkill /IM HotReload.exe