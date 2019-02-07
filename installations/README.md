# How to turn bare Ubuntu machine into bbtest host 

## Prerequisite:
- Firewall ports should be allowed: 21 for FTP, 18812 for rpyc and 10090-10100 for FTP passive mode
```bash
sudo firewall-cmd --zone=public --add-port=21/tcp --permanent
sudo firewall-cmd --zone=public --add-port=18812/tcp --permanent
sudo firewall-cmd --zone=public --add-port=10090-10100/tcp --permanent
sudo firewall-cmd --reload
```
Important note - after copying files to the target host machine you might need to convert the files from dos to unix
format, if this is the case install and run dos2unis util.

## Install FTP
Install vsftpd:
```bash
apt install vsftpd
```
or
```bash
yum install vsftpd
```

Copy /etc/vsftpd.conf and /etc/vsftpd.userlist from here under /etc (debian) or /etc/vsftpd (fedora).

Edit the vsftpd.conf file and uncomment one of the options of the following settings (see instructions insdie the file). 
```bash
userlist_file
pam_service_name
```

Allow ftp user to ftp - make sure it does not appear in /etc/vsftpd/ftpusers

Restart vsftpd
```bash
systemctl restart vsftpd.service
```

### Notes about CentOS FTP:
- FTP: Enable putting files into ftp-home-directory:
```bash
sudo setsebool -P allow_ftpd_full_access 1
```

### Notes about Mac FTP:
1. Built-in FTP was removed in recent OSX versions (e.g. Mojave)
   We could not set up FTP on Mojave. Failed to setup vsftpd
2. Enable FTP on OSX Sierra:
```bash
sudo -s launchctl load -w /System/Library/LaunchDaemons/ftp.plist
```

## Python 3.7
Install python3.7 (Debian)
```bash
add-apt-repository ppa:deadsnakes/ppa
apt-get update
apt install python3.7
apt install python3.7-dev
apt install python3-pip
```

### Notes about CentOS Python3.7
There's currently no yum package for python3.7. We need to build it from source:

maybe redundant - need to check and update the doc:
```bash
yum install -y epel-release  
yum install -y centos-release-scl
yum install -y gcc openssl-devel bzip2-devel
```
must:
```bash
yum install -y libffi-devel
wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz
tar xzf Python-3.7.2.tgz
cd Python-3.7.2/
./configure --enable-optimizations
make
make install
```

### Notes about OSX Python3.7
```bash
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew install python3
```

## Install rpyc and bbtest
```bash
/usr/bin/python3.7 -m pip install rpyc
export username=name of devpi user name
/usr/bin/python3.7 -m pip install -UI -i http://172.16.57.40/$username/dev/ --trusted-host 172.16.57.40 bbtest
```

Start rpyc server
```bash
rpyc_classic.py --host 0.0.0.0
```

## Personalization Box preparation:
Machine should have python2 installed with protobuf package.


## Add bbtest user
```bash
useradd bbtest
chmod 777 /home/bbtest/
passwd bbtest # set to bbtest
usermod --shell /usr/bin/bash bbtest
usermod --shell /home/bbtest bbtest
```
Add bbtest user to vsftpd.conf and user_list, restart vsftpd service.

## Install rpycserver
Copy install_rpyc_as_linux_service.sh, rpycserver.service and rpycserver.sh from here under /home/bbtest.
```bash
cd /home/bbtest
install_rpyc_as_linux_service.sh
```
