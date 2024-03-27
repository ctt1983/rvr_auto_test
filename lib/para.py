#!/usr/bin/env python
#  -*- coding:utf-8 -*-
import os
import configparser

class myPara:
    def __init__(self):
        print('')
    def read_para(self):
        global sta_port, sta_baudrate, sta_ip
        global sap_port, sap_baudrate, sap_ip, sap_ssid, sap_pwd
        global att_ip
        global att_start, att_stop, att_step, udp_tcp, ul_dl, iperf_time, wait_time

        parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) 
        #print(parent_dir)
        config_file_path = os.path.join(parent_dir, 'config.ini')
        conf = configparser.ConfigParser()
        conf.read(config_file_path, encoding = 'utf-8')
        # print(conf.sections())
        # print(conf.has_section('ap'))
        # print(conf.options('ap'))
        # print(conf.items('ap'))
        # print(conf.get('ap', 'sap_ip'))

        #读取station设定
        sta_port = conf.get('station','sta_port')
        sta_baudrate = conf.get('station','sta_baudrate')
        sta_ip = conf.get('station','sta_ip')
        #读取ap设定
        sap_port = conf.get('ap','sap_port')
        sap_baudrate = conf.get('ap','sap_baudrate')
        sap_ip = conf.get('ap','sap_ip')
        sap_ssid = conf.get('ap','sap_ssid')
        sap_pwd = conf.get('ap','sap_pwd')
        #读取att设定
        att_ip = conf.get('att','att_ip')
        #print(conf.get('att','att_ip'))
        #读取rvr设定
        att_start = conf.get('rvr', 'att_start')
        att_stop = conf.get('rvr', 'att_stop')
        att_step = conf.get('rvr', 'att_step')
        #list udp/tcp
        udp_tcp = [int(x.strip()) for x in conf['rvr']['udp_tcp'].split(',')]
        #print(udp_tcp)
        #list uplink/downlink
        ul_dl = [int(x.strip()) for x in conf['rvr']['ul_dl'].split(',')]   
        #print(ul_dl)
        iperf_time = conf.get('rvr', 'iperf_time')
        wait_time = conf.get('rvr', 'wait_time')
        #RVR曲线形式
        #att_rssi = conf.get('curve','att_rssi')
    def iperf_cases(self):
        global iperf_cmd_ap, iperf_cmd_sta
        iperf_cmd_ap = [
            ['',''],
            ['',''],
        ]
        iperf_cmd_sta = [
            ['',''],
            ['',''],
        ]
        for i in udp_tcp:
            #print('i={}'.format(i))
            for j in ul_dl:
                #print('j={}'.format(j))
                if i == 0 and j == 0:   #UDP Uplink
                    iperf_cmd_ap[i][j] = 'iperf -s -u -i 1\r'
                    iperf_cmd_sta[i][j] = 'iperf -c {} -u -i 1 -b 200m -t {}\r'.format(sap_ip, iperf_time)
                    print('>'*20,'{}{}: udp ul'.format(i,j))
                elif i == 0 and j == 1: #UDP Downlink
                    iperf_cmd_ap[i][j] = 'iperf -c {} -u -i 1 -b 200m -t {}\r'.format(sta_ip, iperf_time)
                    iperf_cmd_sta[i][j] = 'iperf -s -u -i 1\r' 
                    print('>'*20,'{}{}: udp dl'.format(i,j))                
                elif i == 1 and j == 1: #TCP Downlink
                    iperf_cmd_ap[i][j] = 'iperf -c {} -i 1 -t {} -p 5001\r'.format(sta_ip, iperf_time)    
                    iperf_cmd_sta[i][j] = 'iperf -s -i 1 -p 5001\r'     
                    print('>'*20,'{}{}: tcp dl'.format(i,j))              
                elif i == 1 and j == 0: #TCP Uplink
                    iperf_cmd_ap[i][j] = 'iperf -s -i 1 -p 5001\r'
                    iperf_cmd_sta[i][j] = 'iperf -c {} -i 1 -t {} -p 5001\r'.format(sap_ip, iperf_time)
                    print('>'*20,'{}{}: tcp ul'.format(i,j))
                else:
                    print('>'*20,'{}{}: unvalid'.format(i,j))
                    print('<<Please check config file, invalid case!>>')
                    break
            
if __name__ == '__main__':
    para = myPara()