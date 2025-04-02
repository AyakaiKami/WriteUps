# simple-keygen

Description:
```
I think this simple keygen won't stand a chance against your skills. Am I right?

When you finally manage to reverse engineer the algorithm you can simply send to us a solution and we will validate it for you.
```

We can run file on the binary to get mor info about it.
```bash
file keygen.bin 

keygen.bin: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=31aa75db4efe46ebb42e4117318a856779fd383a, stripped
```

I'll use Ghidra to decompile the binary. 

As I don't see any main function listed, I'll start with the entry function.
```c
void processEntry entry(undefined8 param_1,undefined8 param_2)
{
  undefined1 auStack_8 [8];
  
  __libc_start_main(FUN_00100ec9,param_2,&stack0x00000008,FUN_001010e0,FUN_00101150,param_1,
                    auStack_8);
  do {
                    /* WARNING: Do nothing block with infinite loop */
  } while( true );
}
```

We can see the main function is named FUN_00100ec9. I'll see what's that about.
```c
undefined4 FUN_00100ec9(void)
{
  int iVar1;
  ostream *poVar2;
  long in_FS_OFFSET;
  undefined4 local_70;
  string local_68 [32];
  string local_48 [40];
  long local_20;
  
  local_20 = *(long *)(in_FS_OFFSET + 0x28);
  poVar2 = std::operator<<((ostream *)std::cout,"Starting Warmup Keygen");
  std::ostream::operator<<(poVar2,std::endl<>);
  poVar2 = std::operator<<((ostream *)std::cout,"Enter serial: ");
  std::ostream::operator<<(poVar2,std::endl<>);
  std::string::string(local_68);
                    /* try { // try from 00100f52 to 00100fa3 has its CatchHandler @ 00101058 */
  std::operator>>((istream *)std::cin,local_68);
  poVar2 = std::operator<<((ostream *)std::cout,"Serial: ");
  poVar2 = std::operator<<(poVar2,local_68);
  std::ostream::operator<<(poVar2,std::endl<>);
  std::string::string(local_48,local_68);
                    /* try { // try from 00100fab to 00100faf has its CatchHandler @ 00101047 */
  iVar1 = FUN_00100e2a(local_48);
  std::string::~string(local_48);
  if (iVar1 == 0) {
                    /* try { // try from 00100fd3 to 0010101d has its CatchHandler @ 00101058 */
    poVar2 = std::operator<<((ostream *)std::cout,"Serial accepted. Send it to checker.");
    std::ostream::operator<<(poVar2,std::endl<>);
    local_70 = 0;
  }
  else {
    poVar2 = std::operator<<((ostream *)std::cout,"Invalid Serial. Try harder.");
    std::ostream::operator<<(poVar2,std::endl<>);
    local_70 = 0x1337;
  }
  std::string::~string(local_68);
  if (local_20 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return local_70;
}
```

The code section above reads a string(a serial key) that will be passed to FUN_00100e2a as the only argument. If the function returns 0 that means the input was accepted as the serial.

We can inspect that function next.
```c
undefined4 FUN_00100e2a(ulong param_1)
{
  char cVar1;
  int iVar2;
  char *pcVar3;
  undefined4 local_24;
  int local_20;
  
  iVar2 = std::string::length();
  if (iVar2 == 0x16) {
    for (local_20 = 0; local_20 < 0x16; local_20 = local_20 + 2) {
      pcVar3 = (char *)std::string::at(param_1);
      cVar1 = *pcVar3;
      pcVar3 = (char *)std::string::at(param_1);
      if ((int)cVar1 - (int)*pcVar3 != -2) {
        return 0x1337;
      }
    }
    local_24 = 0;
  }
  else {
    local_24 = 0x1337;
  }
  return local_24;
}
```

The code above verifies if the argument is the valid serial(the flag). We can already determine the length of the serial which is 0x16 (22).
If the length is validated, we iterate through the strings. I had to read the assembly code to figure out the std::string::at calls.
```bash
LAB_00100e53                                    XREF[1]:     00100ead(j)  
00100e53 8b 45 e8        MOV        EAX,dword ptr [RBP + local_20]
00100e56 3b 45 ec        CMP        EAX,dword ptr [RBP + local_1c]
00100e59 7d 54           JGE        LAB_00100eaf
00100e5b 8b 45 e8        MOV        EAX,dword ptr [RBP + local_20]
00100e5e 48 63 d0        MOVSXD     RDX,EAX
00100e61 48 8b 45 d8     MOV        RAX,qword ptr [RBP + local_30]
00100e65 48 89 d6        MOV        RSI,RDX
00100e68 48 89 c7        MOV        RDI,RAX
00100e6b e8 90 fe        CALL       <EXTERNAL>::std::string::at                      undefined at(ulong param_1)
         ff ff
00100e70 0f b6 00        MOVZX      EAX,byte ptr [RAX]
00100e73 0f be d8        MOVSX      EBX,AL
00100e76 8b 45 e8        MOV        EAX,dword ptr [RBP + local_20]
00100e79 83 c0 01        ADD        EAX,0x1
00100e7c 48 63 d0        MOVSXD     RDX,EAX
00100e7f 48 8b 45 d8     MOV        RAX,qword ptr [RBP + local_30]
00100e83 48 89 d6        MOV        RSI,RDX
00100e86 48 89 c7        MOV        RDI,RAX
00100e89 e8 72 fe        CALL       <EXTERNAL>::std::string::at                      undefined at(ulong param_1)
         ff ff
00100e8e 0f b6 00        MOVZX      EAX,byte ptr [RAX]
```

I didn't need to read line by line, I just wanted to make sure that eax will be incremented, and it is. So we know that cVar1 will have the value of param_1[i] and that *pcVar3 will have the value of param_1[i+1].

If cVar1 -*pcVar3 != -2 the function fails, the input is not a valid serial.

So a valid key should be a string of length 22 in which each string[i*2]-string[i*2+1]==-2.

### acacacacacacacacacacac