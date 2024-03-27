title Iperf_client_d
@echo off
setlocal ENABLEDELAYEDEXPANSION

set protocol=%1
set port=%2
set ip=%3
set run_time=%4

echo protocol: %protocol%
echo port: %port%
echo ip: %ip%
echo run_time: %run_time%

if "%protocol%"=="udp" (
	iperf.exe -c %ip% -i 1 -u -b 20M -p %port% -t %run_time% -d | tee udpc_%port%.txt
) else (
	iperf.exe -c %ip% -i 1 -p %port% -t %run_time% -d | tee tcpc_%port%.txt
	
)

pause