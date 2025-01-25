# Platform: HTB_CTF
# Category: Web
# Name: sanitize

Following the link we get to a login page.

![logIn](img1.png)

The title of the pages sugest an SQLi type vulnerability. So I'll try a simple SQLi payload.

```markdown
' or 1=1;--
```

![rez](img2.png)

## We got the flag!