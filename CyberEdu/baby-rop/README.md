# baby-rop

Description:
```
This is a simple pwn challenge. You should get it in the lunch break.

Running on Ubuntu 20.04.
```

Running file on the binary reveals the following:
```bash
file pwn_baby_rop 
pwn_baby_rop: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=7065eaf6025143d7286e6b73427a82ed0d780904, for GNU/Linux 3.2.0, stripped
```

I'll use Ghidra to decompile the binary.

### entry
```c
void processEntry entry(undefined8 param_1,undefined8 param_2)
{
  undefined1 auStack_8 [8];
  
  __libc_start_main(FUN_0040145c,param_2,&stack0x00000008,FUN_00401600,FUN_00401670,param_1,
                    auStack_8);
  do {
                    /* WARNING: Do nothing block with infinite loop */
  } while( true );
}
```

We can see the main function is FUN_0040145c.

### FUN_0040145c ,the main function
```c
undefined8 FUN_0040145c(void)
{
  FUN_00401080(stdin,0,2,0);
  FUN_00401080(stdout,0,2,0);
  puts("Solve this challenge to prove your understanding to black magic.");
  FUN_00401176();
  return 0;
}
```

FUN_00401080 is just a wrapper for setvbuf.

### FUN_00401176
