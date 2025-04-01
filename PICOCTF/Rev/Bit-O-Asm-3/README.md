# Bit-O-Asm-3

Description:
```
Can you figure out what is in the eax register? Put your answer in the picoCTF flag format: picoCTF{n} where n is the contents of the eax register in the decimal number base. If the answer was 0x11 your flag would be picoCTF{17}.
Download the assembly dump here.
```

Dump:
```
<+0>:     endbr64 
<+4>:     push   rbp
<+5>:     mov    rbp,rsp
<+8>:     mov    DWORD PTR [rbp-0x14],edi
<+11>:    mov    QWORD PTR [rbp-0x20],rsi
<+15>:    mov    DWORD PTR [rbp-0xc],0x9fe1a
<+22>:    mov    DWORD PTR [rbp-0x8],0x4
<+29>:    mov    eax,DWORD PTR [rbp-0xc]
<+32>:    imul   eax,DWORD PTR [rbp-0x8]
<+36>:    add    eax,0x1f5
<+41>:    mov    DWORD PTR [rbp-0x4],eax
<+44>:    mov    eax,DWORD PTR [rbp-0x4]
<+47>:    pop    rbp
<+48>:    ret
```

We can start with the last instruction that interacts with the eax register. 

```
<+44>:    mov    eax,DWORD PTR [rbp-0x4]
```

This just takes the 4 bytes from that address and puts them in the eax register.

```
<+41>:    mov    DWORD PTR [rbp-0x4],eax
```

This takes the value from the eax register and puts the first 4 bytes at that address of the stack.

```
<+36>:    add    eax,0x1f5
```

This adds the value 0x1f5 (501 as int) to the eax register.

```
<+32>:    imul   eax,DWORD PTR [rbp-0x8]
```

This multiplies the value in eax with the 4 bytes value at that specific stack address.

```
<+29>:    mov    eax,DWORD PTR [rbp-0xc]
```

This moves 4 bytes from that stack address into the eax register.

```
<+15>:    mov    DWORD PTR [rbp-0xc],0x9fe1a
```
This sets the first 4 bytes starting from that specific stack address to 0x9fe1a (654874)

```
<+22>:    mov    DWORD PTR [rbp-0x8],0x4
```
This sets the first 4 bytes starting from that specific stack address to 0x4 (4)

Now we can reconstructs the steps in pseudocode:
```
a=0 ///rbp-0x4
b=4 ///rbp-0x8
c=654874 ///rbp-0xc

eax=654874
eax*=4
eax+=501

eax= first 4 bytes of eax 
```

So eax is 2619997.