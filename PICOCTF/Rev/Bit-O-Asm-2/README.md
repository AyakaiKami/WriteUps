# Bit-O-Asm-2

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
<+15>:    mov    DWORD PTR [rbp-0x4],0x9fe1a
<+22>:    mov    eax,DWORD PTR [rbp-0x4]
<+25>:    pop    rbp
<+26>:    ret
```

We can backtrack from the last value that contains eax.

```
<+22>:    mov    eax,DWORD PTR [rbp-0x4]
```

This takes 4 bytes from that address and puts the value in eax.

```
<+15>:    mov    DWORD PTR [rbp-0x4],0x9fe1a
```

This sets the value of the variable to 0x9fe1a (654874), only works with the first 4 bytes.

So the value for eax is 654874.