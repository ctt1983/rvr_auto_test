import time
from telnetlib import Telnet

class myAtt(object):
    def __init__(self, host='192.168.1.118', port=0):
        self.host = host
        self.port = port
        self.att = None
        self.status = self.connect()

    def connect(self):
        self.att = Telnet(self.host, self.port, timeout=10)

    def read_Atten(self):
        cmd = 'ATT \n'
        cmd = bytes(cmd, encoding='utf-8')
        self.att.write(cmd)
        time.sleep(3)
        out = self.att.read_very_eager().decode('utf-8')
        print('Set Attenuator Response: {}'.format(out))

    def set_Atten(self, value, port=0):
        if port == 0:
            # cmd = 'ATT 2 {0} 3 {0} 4 {0} \n'.format(value)
            # cmd = 'ATT 1 {} \n'.format(value)
            cmd = 'ATT 1 {0} 2 {0} 3 {0} 4 {0} \n'.format(value)
        else:
            cmd = 'ATT {} {} \n'.format(port, value)
        print('ATT CMD: {}'.format(cmd))
        cmd = bytes(cmd, encoding='utf-8')
        self.att.write(cmd)
        time.sleep(3)
        out = self.att.read_very_eager().decode('utf-8')
        print('Set Attenuator Response: {}'.format(out))
        return out

    def close(self):
        self.att.close()
        print('Attenuator connection alreay disconnected!')


if __name__ == "__main__":
    # pte = myPTE('10.18.31.18')
    att = myAtt('192.168.1.118')
    # pte.read_Atten()
    att.set_Atten(40)
