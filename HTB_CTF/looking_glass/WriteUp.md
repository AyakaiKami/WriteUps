# Platform: HTB_CTF
# Category: Web
# Name: looking_glass

Following the link we get to this page:

![pg](img1.png)

Looking at the request made when pressing the "Test" button makes me think at a command injection vulnerability.

![req](img2.png)

I'll try a simple adding address
```bash
;ls
```
to the ip field.

![rce](img3.png)

It works! Now let's see the root folder.

Payload:
```bash
;ls /
```

![ls](img4.png)

Now we just need to read the flag.

```bash
cat ../flag_y71Z6
```

![flag](img5.png)

## We got the flag!