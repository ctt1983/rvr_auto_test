title Iperf_Multi_cs
@echo off
setlocal ENABLEDELAYEDEXPANSION

taskkill /f /im iperf.exe
taskkill /f /fi "WINDOWTITLE eq Iperf_client"
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
set /a port_1=%%i+5001
echo upload test_num is: %%i
echo test_port is: !port_1!
start cmd /k "cd D:\RVR_TEST\BuffaloTest\tools&&client.bat %protocol% !port_1! %ip% %run_time%"
)
ping -n 1 127.0.0.1 > null
for /L %%i in (1,1,%num%) do (
set /a port_2=%%i+!port_1!
echo download test_num is: %%i
echo test_port is: !port_2!
start cmd /k "cd D:\RVR_TEST\BuffaloTest\tools&&iperf_serv.bat %protocol% !port_2!"
)