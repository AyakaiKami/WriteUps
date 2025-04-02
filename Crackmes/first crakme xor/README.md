# web3ex's first crakme xor

Description:
```
XOR encryption and checksum validation challenge. get password
```

### File info:
```bash
file main.exe

main.exe: PE32 executable (console) Intel 80386, for MS Windows, 13 sections
```

We have a PE file. I'll use Ghidra to decompile it and take a look at the code.

### main
```c
int __cdecl _main(int _Argc,char **_Argv,char **_Env)
{
  char cVar1;
  ostream *poVar2;
  
  ___main();
  std::string::string((string *)&stack0xffffffd8);
  std::operator<<((ostream *)&_ZSt4cout,"Enter the password: ");
  std::operator>>((istream *)&_ZSt3cin,(string *)&stack0xffffffd8);
  cVar1 = validatePassword((string *)&stack0xffffffd8);
  if (cVar1 == '\0') {
    poVar2 = std::operator<<((ostream *)&_ZSt4cout,"Incorrect password!");
    std::ostream::operator<<(poVar2,std::endl<>);
  }
  else {
    poVar2 = std::operator<<((ostream *)&_ZSt4cout,"Correct password!");
    std::ostream::operator<<(poVar2,std::endl<>);
  }
  _Sleep@4(3000);
  std::string::~string((string *)&stack0xffffffd8);
  return 0;
}
```

We can see the program reads the password from the user and then calls the validatePassword function. If the function returns 0 that means the password was incorrect.

### validatePassword

```c
bool __cdecl validatePassword(string *param_1)
{
  int iVar1;
  bool bVar2;
  string local_54 [24];
  string local_3c [24];
  string local_24 [28];
  
  iVar1 = std::string::length();
  if (iVar1 == 8) {
    xorEncryptDecrypt(local_54,(char)param_1);
    xorEncryptDecrypt(local_3c,(char)local_54);
    std::string::operator=(local_54,local_3c);
    std::string::~string(local_3c);
    xorEncryptDecrypt(local_24,(char)local_54);
    std::string::operator=(local_54,local_24);
    std::string::~string(local_24);
    iVar1 = calculateChecksum(local_54);
    bVar2 = iVar1 == 300;
    std::string::~string(local_54);
  }
  else {
    bVar2 = false;
  }
  return bVar2;
}
```

The code reveals that the length of the password should be 8 characters. If it is, our text is passwd to the xorEncryptDecrypt and the output will be stored in local_54. The encrypted password will be encrypted again and that output will be placed in local_3c. The string in local_3c will be saved in local_54. So our password is encrypted 2 times. We then encrypt it again ad alculate it's checksum. For the password to be correct the checksum needs to be 300.

### xorEncryptDecrypt.
```c
string * __cdecl xorEncryptDecrypt(string *param_1,char param_2)
{
  uint uVar1;
  byte *pbVar2;
  byte *pbVar3;
  undefined3 in_stack_00000009;
  byte in_stack_0000000c;
  undefined4 local_10;
  
  std::string::string(param_1,_param_2);
  local_10 = 0;
  while( true ) {
    uVar1 = std::string::length();
    if (uVar1 <= local_10) break;
    pbVar2 = (byte *)std::string::operator[](local_10);
    pbVar3 = (byte *)std::string::operator[](local_10);
    *pbVar2 = *pbVar3 ^ in_stack_0000000c;
    local_10 = local_10 + 1;
  }
  return param_1;
}
```


