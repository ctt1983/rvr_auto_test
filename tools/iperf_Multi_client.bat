title Iperf_Multi_client
@echo off
setlocal ENABLEDELAYEDEXPANSION

taskkill /f /im iperf.exe
taskkill /f /fi "WINDOWTITLE eq Iperf_client"
taskkill /f /fi "WINDOWTITLE eq Iperf_client_d"
taskkill /f /fi "WINDOWTITLE eq Iperf_serv"
del /f /s /q D:\RVR_TEST\BuffaloTest\tools\*.txt

set num=%1
set protocol=%2
set ip=%3
set run_time=%4

echo throughput_nums: %num%
echo protocol: %protocol%
echo ip: %ip%
echo run_time: %run_time%

for /L %%i in (1,1,%num%) do (
set /a port=%%i+5001
echo this test_num is: %%i
echo test_port is: !port!
start cmd /k "cd D:\RVR_TEST\BuffaloTest\tools&&client.bat %protocol% !port! %ip% %run_time%"
)
