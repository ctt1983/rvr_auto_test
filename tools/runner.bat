title Throughput Test
start iperf_serv.bat
timeout 2
start client.bat
timeout 2
pause
python throughput.py
pause
timeout 5
taskkill /f /fi "WINDOWTITLE eq Iperf_client"
timeout 1
taskkill /f /fi "WINDOWTITLE eq  Iperf_serv"
timeout 1
wmic process where "CommandLine like '%%iperf%%-s%%5001%%'" call terminate
