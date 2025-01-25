# Platform: HTB_CTF
# Category: 
# Name: baby_todo_or_not_todo

We start on this page.

![img1](img1.png)

We can add tasks to our to do list.

![img2](img2.png)

This is a White Box challenge so I'll take a look at the source code.

I found a comment on one of the files.

![img3](img3.png)

We can see the name of the function being called. Let's find the function.

![img4](img4.png)

We can see the function returns the contents of the "todo" table.

We know this function can be accessed by all users but it reveals information about the other users as well. Let's call the function.

![img5](img5.png)

We can also see the flag.

![flag](img6.png)


## We got the flag!