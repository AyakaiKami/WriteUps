# Platform: HTB_CTF
# Category: Web
# Name: Full_Stack_Conf

Following the page we get to this page:

![page](img1.png)

![page2](img2.png)

Interesting comment :)

Let's test for XSS.

Payload:
```markdown
<script>alert("1");</script>
```

![page3](img3.png)

# We got the flag!