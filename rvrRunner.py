#!/usr/bin/env python
#  -*- coding:utf-8 -*-
import re
import time
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

start_time = time.time()    #开始计时
start_time_1 = time.strftime("%Y-%m-%d_%H-%M-%S")

sys.path.extend([os.path.join(os.getcwd(), "lib")])

REPORT_PATH = os.path.join(os.getcwd(), "result")
REPORT_PATH = os.path.join(REPORT_PATH, time.strftime("%Y-%m-%d"))
if not os.path.exists(REPORT_PATH):
    os.makedirs(REPORT_PATH)

from att import myAtt
from series import mySeries
from para import myPara
import para  #para.py
from curve import readcsv
import curve #curve.py

reportTitle = "RVR_test"
reportName = os.path.join(REPORT_PATH, reportTitle+"_Test_Report_{}.html".format(time.strftime("%Y-%m-%d_%H-%M-%S")))
reportName1 = os.path.join(REPORT_PATH, reportTitle+"_Test_Report_RSSI{}.html".format(time.strftime("%Y-%m-%d_%H-%M-%S")))
LogFile = os.path.join(REPORT_PATH, reportTitle+"Log_{}.txt".format(time.strftime("%Y-%m-%d_%H-%M-%S")))
datafile = os.path.join(REPORT_PATH, reportTitle+"_rvr_data_{}.csv".format(time.strftime("%Y-%m-%d_%H-%M-%S")))    

print('Import parameters, preparing for test...')
paras = myPara()
paras.read_para()
paras.iperf_cases()

print('RvR test started!')
print('Init Programmable attenuator (ip:{}), setting to 0dB...'.format(para.att_ip))
#初始化att=0
att = myAtt(para.att_ip)
att.set_Atten(0)

#连接sta串口并下初始化命令（关闭ap mode,连接AP）
sta_series = mySeries(para.sta_port, para.sta_baudrate) #连接STA串口
time.sleep(0.1)
sta_series.input('wifi_ap_stop\r')
time.sleep(0.1)
#sta_series.input('wifi_sta_connect {} {}\r'.format(para.sap_ssid, para.sap_pwd))
#sta_series.connect(para.sap_ssid, para.sap_pwd)
time.sleep(0.1)

#连接sap串口并下初始化命令（固定速率）
sap_series = mySeries(para.sap_port, para.sap_baudrate) #连接SAP串口
time.sleep(0.1)
#sap_series.input('rc -f 28\r')   #force WiFi data rate
time.sleep(0.1)

# Atten_Set = list(range(10, 46, 5)) + list(range(47, 86, 2))
# Atten_Set = list(range(10, 20, 1))

def rvrRuner():
    iter = 0    #计算跑了几个case，方便数据记录
    rvr_data= {}    #初始化一个空的字典
    df = pd.DataFrame(rvr_data)
    fig1 = curve.figure('Attenuation(dB)','Throughput(Mbps)',0,101,1,0,51,5,0,110,0,50,1,5)
    fig2 = curve.figure('Absolute RSSI(dBm)','Throughput(Mbps)',-100,0,1,0,51,5,-100,0,0,50,1,5)
    for i in para.udp_tcp:
        for j in para.ul_dl:
            att_swp = []    #x轴
            tput_avg = []   #y轴
            test_case = ''
            rssi_list = []
            att.set_Atten(0)    #防止断开，测新的case时重新连接
            time.sleep(0.1)
            sta_series.input('wifi_sta_connect {} {}\r'.format(para.sap_ssid, para.sap_pwd))
            time.sleep(0.1)

            for k in range(int(para.att_start), int(para.att_stop), int(para.att_step)):
                tputs = []
                att.set_Atten(k)
                time.sleep(1)
                if i == 0 and j == 0:   #UDP Uplink
                    test_case = 'UDP_UL'
                    sap_series.input(para.iperf_cmd_ap[i][j])     #server端先下cmd
                    time.sleep(0.5)

                    sta_series.write('wifi_sta_info\r') #没有读取打印
                    time.sleep(0.1)
                    for line in sta_series.outputs(0):
                        if 'RSSI' in line:
                            match = re.search(r'-?\d+', line)
                            if match:
                                rssi = int(match.group())
                                rssi_list.append(rssi)
                                #print(rssi_list)
                            else:
                                print("no RSSI")

                    sta_series.input(para.iperf_cmd_sta[i][j])
                    time.sleep(1)
                elif i == 0 and j == 1:   #UDP Downlink
                    test_case = 'UDP_DL'

                    sta_series.write('wifi_sta_info\r') #没有读取打印
                    time.sleep(0.1)
                    for line in sta_series.outputs(0):
                        if 'RSSI' in line:
                            match = re.search(r'-?\d+', line)
                            if match:
                                rssi = int(match.group())
                                rssi_list.append(rssi)
                            else:
                                print("no RSSI")

                    sta_series.input(para.iperf_cmd_sta[i][j])     #server端先下cmd
                    time.sleep(0.5)
                    sap_series.input(para.iperf_cmd_ap[i][j])
                    time.sleep(1)
                elif i == 1 and j == 1:   #TCP Downlink
                    test_case = 'TCP_DL'
                    
                    sta_series.write('wifi_sta_info\r') #没有读取打印
                    time.sleep(0.1)
                    for line in sta_series.outputs(0):
                        if 'RSSI' in line:
                            match = re.search(r'-?\d+', line)
                            if match:
                                rssi = int(match.group())
                                rssi_list.append(rssi)
                            else:
                                print("no RSSI")

                    sta_series.input(para.iperf_cmd_sta[i][j])     #server端先下cmd
                    time.sleep(0.5)
                    sap_series.input(para.iperf_cmd_ap[i][j])
                    time.sleep(1)
                elif i == 1 and j == 0:   #TCP Uplink
                    test_case = 'TCP_UL'
                    sap_series.input(para.iperf_cmd_ap[i][j])     #server端先下cmd
                    time.sleep(0.5)
                    
                    sta_series.write('wifi_sta_info\r') #没有读取打印
                    time.sleep(0.1)
                    for line in sta_series.outputs(0):
                        if 'RSSI' in line:
                            match = re.search(r'-?\d+', line)
                            if match:
                                rssi = int(match.group())
                                rssi_list.append(rssi)
                            else:
                                print("no RSSI")

                    sta_series.input(para.iperf_cmd_sta[i][j])
                    time.sleep(1)
                else: 
                    print('invaild case')
                    break
                while True:
                    if j ==0:
                        line = sap_series.output(0) #读取Server端打印。Server端'iperf -s'命令下完后切到Client端串口所以server端iperf输出没有实时输出，正好可以只读取这一部分。
                    else:
                        line = sta_series.output(0)
                    if 'iperf exit' not in line:
                        if line.rstrip().endswith("Mbits/sec"):#有可能第一次执行不满足条件所以tputs为空，所有运算应该等遍历完成。
                            words = line.split()    #空格作为默认分隔符
                            words = [word for word in words if word] #去除空格，防止有两个空格
                            if len(words) >=2: 
                                tputs.append(float(words[-2]))                              
                            print(line)
                    else:
                        break
                #print(tputs)
                att_swp.append(k)
                if len(tputs):
                    tput_avg.append(round(sum(tputs)/len(tputs),2))
                else:
                    print('no tput value was got!')
                    tput_avg.append(0)
            #获得了RvR曲线的x(衰减dB)和y(吞吐量Mbps)
            #print(att_swp)
            #print(tput_avg)
            #将本轮rvr结果添加到dataframe:df
            df['Attenuation_{}'.format(test_case)] = att_swp
            df['RSSI_{}'.format(test_case)] = rssi_list
            df['Throughput_{}'.format(test_case)] = tput_avg    
            #之前犯了一个错误：[att_swp]等于搞了一个二维数组。错误的打印如下：
            #      Attenuation_UDP_UL                   Throughput_UDP_UL
            # 0  [10, 12, 14, 16, 18]  [32.3, 35.08, 33.83, 36.52, 36.92]
            #绘图
            curve.trace(fig1,test_case,att_swp,tput_avg)
            curve.trace(fig2,test_case,rssi_list,tput_avg)            
    print(df)
    df.to_csv(datafile,index=False)
    curve.wrfig(fig1,reportName)
    curve.wrfig(fig2,reportName1)

if __name__ == '__main__':
    rvrRuner()
    #readcsv(datafile,'UDP_UL',reportName)
    end_time = time.time()
    end_time_1 = time.strftime("%Y-%m-%d_%H-%M-%S")
    exe_time = end_time - start_time
    print('RvR test done<<<<<<<<<<<<<<<<<<<<<<<\n', 'cost time:',round(exe_time,1),'s, from ',start_time_1,' to ',end_time_1)
    att.set_Atten(0)

