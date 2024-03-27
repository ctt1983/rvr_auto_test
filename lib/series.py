#!/usr/bin/env python
#  -*- coding:utf-8 -*-
import serial
import os
import sys
import time
import re

class mySeries:
    def __init__(self, port='com3', baudrate=2000000, timeout=1):
        print(port, baudrate)
        self.ser = serial.Serial(port, baudrate=baudrate, bytesize=8, parity='N', stopbits=1, timeout=timeout)
        self.serial_togger()
        self.ser.flushInput()

    def serial_togger(self):
        """
        硬件流控
        :param board_class:
        :return:
        """
        self.ser.setDTR(1)
        time.sleep(0.5)
        self.ser.setRTS(1)
        time.sleep(0.5)
        self.ser.setRTS(0)
        time.sleep(0.5)

    def closeSer(self):
        self.ser.close()

    def reOpenSer(self,funcname="Func"):
        print("Func {} run failed, Reopen serial port!".format(funcname))
        self.ser.close()
        time.sleep(0.1)
        self.ser.open()

    def write(self, cmd):
        # remove newline
        cmd = cmd.rstrip('\r\n')
        # check cmd length
        try:
            self.ser.write(bytes(cmd + '\r\n', encoding='utf-8'))
        except Exception as e:
            print("send commands got Error:{}".format(e))
            self.reOpenSer("Write")

    def input(self, cmd, echo=1, wait_ms=1):
        out = ''
        #try:
        self.write(cmd)
        time.sleep(wait_ms*1e-3)
        for line in self.ser.readlines():
            try:
                #out += line.decode('utf-8')
                out += line.decode('utf-8', errors='ignore')
            except Exception as e:
                print("Input got Error:{}".format(e))
                self.reOpenSer("Input")
        if echo:
            print(out)
        return out
    
    def output(self, echo=1):
        out = ''
        #try:
        out = self.ser.readline().decode('utf-8').strip()
        if echo:
            print(out)
        return out
    
    def outputs(self, echo=1):
        out = []
        for line in self.ser.readlines():
            try:
                out.append(line.decode('utf-8', errors='ignore'))
            except Exception as e:
                print("Input got Error:{}".format(e))
                self.reOpenSer("Input")
        if echo:
            print(out)
        return out

    def query(self, cmd, wait=0.001,echo=1):
        self.write(cmd)
        time.sleep(wait)
        out = ''
        for line in self.ser.readlines():
            try:
                out += line.decode('utf-8', errors='ignore')
            except Exception as e:
                print("Input got Error:{}".format(e))
                self.reOpenSer("Input")
        if echo:
            print(out)
        return out

    def setup(self, reboot=True):
        if reboot:
            self.input('reboot\r')
            time.sleep(1)
        self.input('stack_wifi')
        time.sleep(0.5)

    def start_wifi(self):
        out = self.query('stack_wifi')
        if '[APP] [EVT] INIT DONE' in out:
            print("Start WiFi Success !")
            return True
        else:
            print("Start WiFi Failed !")
            return False

    def connect(self, ssid='test_wh_01', passwd='12345678', WiFiSecurityType='WPA2-PSK',  intf='wlan0', StaticIP=None):
        if ssid:
            print('>'*80)
            cmd = 'wifi_sta_connect {} {}'.format(ssid, passwd)
            print(cmd)
            out = self.query(cmd=cmd, wait=3)
            print(out)
            #if '[APP] [EVT] connected' in out:
            if '[APP] [EVT] event_cb_wifi_event, CODE_WIFI_ON_GOT_IP' in out:
                print('>' * 80)
                print('Connect AP: {} Success !'.format(ssid))
                print('<' * 80)
                return True
            else:
                print('>' * 80)
                print('Connect AP: {} Failed !'.format(ssid))
                print('<' * 80)
                return False
        else:
            print("AP name is None, please check and try again!")
            return False

    def disconnect(self, intf='wlan0', ssid='test_wh_01'):
        out = self.query(cmd='wifi_sta_disconnect\r', wait=1)
        if '[APP] [EVT] disconnect' in out:
            print("Disconnect AP Success !")
            return True
        else:
            print("Disconnect AP Failed !")
            return False

    def ping_test(self, ap_addr='192.168.3.1', times=10):
        cmd= "ping -c {} {}".format(times, ap_addr)
        out = self.query(cmd=cmd, wait=11)
        if out:
            return out
        else:
            return None

    def getDutIP(self, intf='wlan0', ssid='test_wh_01',clientIp='192.168.3.111'):
        ip_regx = re.compile('IP.*:.*(\d+\.){3}\d+', re.I)
        rssi_regx = re.compile('RSSI:.*(-\d+)dbm', re.I)
        out = self.query('wifi_sta_info\r')
        IP = ip_regx.search(out)
        rssi = rssi_regx.search(out)
        if rssi:
            rssi = rssi.group(0)
            print('Get RSSI: {} Success !'.format(rssi.split(':')[1].strip()))
            rssi = rssi.split(':')[1].strip()
        else:
            rssi = ''
        if IP:
            IP = IP.group(0)
            IP = IP.split(':')[1].strip()
            print('Get IP: {} Success !'.format(IP))
            return (IP, rssi)
        else:
            print('Get IP address Failed !')
            return (clientIp, '')


if __name__ == '__main__':
    dut = mySeries('com3',2000000)
    # dut.input('stack_wifi')
    # dut.input('wifi_sta_connect test_wh_01 12345678\r')
    # dut.query('wifi_sta_info\r', echo=1)
    # dut.disconnect()
    # dut.connect('test_wh_01', '12345678')
    # ip = dut.getDutIP()[0]
    # print(ip)
    # dut.setup()