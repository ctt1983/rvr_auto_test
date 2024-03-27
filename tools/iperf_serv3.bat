title Iperf3_serv
@echo off
setlocal ENABLEDELAYEDEXPANSION

set protocol=%1
set port=%2
echo protocol: %protocol%
echo port: %port%

if "%protocol%"=="udp" (
	iperf3.exe -s -i 1 -p %port% | tee udps_%port%.txt
) else (
	iperf3.exe -s -i1 -p %port% | tee tcps_%port%.txt
)

