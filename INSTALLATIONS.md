# How to turn bare Ubuntu machine into bbtest host 

Install fstpd:
```bash
apt install fstpd
```

Set password for ftp:
```bash
passwd ftp
```

Copy /etc/vsftpd.conf and /etc/vsftpd.userlist from here.

Restart vsftpd
```bash
systemctl restart vsftpd.service
```

Install python3.7
```bash
add-apt-repository ppa:deadsnakes/ppa
apt-get update
apt install python3.7
apt install python3.7-dev
apt install python3-pip
```

Install rpyc and bbtest
```bash
/usr/bin/python3.7 -m pip install rpyc
export username=name of devpi user name
/usr/bin/python3.7 -m pip install -UI -i http://172.16.57.40/$username/dev/ --trusted-host 172.16.57.40 bbtest
```

Start rpyc server
```bash
rpyc_classic.py --host 0.0.0.0
```
