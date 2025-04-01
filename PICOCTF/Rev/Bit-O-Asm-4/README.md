# Bit-O-Asm-4

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
<+22>:    cmp    DWORD PTR [rbp-0x4],0x2710
<+29>:    jle    0x55555555514e <main+37>
<+31>:    sub    DWORD PTR [rbp-0x4],0x65
<+35>:    jmp    0x555555555152 <main+41>
<+37>:    add    DWORD PTR [rbp-0x4],0x65
<+41>:    mov    eax,DWORD PTR [rbp-0x4]
<+44>:    pop    rbp
<+45>:    ret
```

```
<+15>:    mov    DWORD PTR [rbp-0x4],0x9fe1a
```
The variable value is set to 654874.

```
<+22>:    cmp    DWORD PTR [rbp-0x4],0x2710
<+29>:    jle    0x55555555514e <main+37>
```
This jumps to main+37 if the variable is smaller than 10000. And it's not the there is no jump.

```
<+31>:    sub    DWORD PTR [rbp-0x4],0x65
```
The variable is decremented by 101. Now the variable is 654773

```
<+35>:    jmp    0x555555555152 <main+41>
<+37>:    add    DWORD PTR [rbp-0x4],0x65
```
This jumps the add instruction.

```
<+41>:    mov    eax,DWORD PTR [rbp-0x4]
```

This sets the eax register to the variable value, 654773.