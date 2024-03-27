title Iperf_serv
@echo off
setlocal ENABLEDELAYEDEXPANSION

set protocol=%1
set port=%2
echo protocol: %protocol%
echo port: %port%

if "%protocol%"=="udp" (
	iperf.exe -s -i 1 -u -p %port% | tee udps_%port%.txt
) else (
	iperf.exe -s -i 1 -p %port% | tee tcps_%port%.txt
)

