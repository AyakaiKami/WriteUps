# Bit-O-Asm-1

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
<+8>:     mov    DWORD PTR [rbp-0x4],edi
<+11>:    mov    QWORD PTR [rbp-0x10],rsi
<+15>:    mov    eax,0x30
<+20>:    pop    rbp
<+21>:    ret
```

We can follow the code and and see the only instruction that interacts with the eax register is <+15>. And that statement just puts the hex value 0x30 in eax.

From hex to integer, the value translates to 48. 