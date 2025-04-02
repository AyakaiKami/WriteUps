# Cappybara's BabyRev

Description:
```
You’ve just run across an old program, seemingly innocent at first. It asks for a password, and if you enter it correctly, you might think you've won. But there's more lurking beneath the surface. Something about this challenge doesn’t add up.

The program not only demands the correct password, but also a secret code—one that isn’t easily discovered. Is it hidden within the code? Or perhaps something you’ll have to figure out for yourself?
```

We start with a binary file.
```bash
file babyrev 

babyrev: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=50d41dbcf429e9cf909fa7fcf4472b296322fc12, for GNU/Linux 3.2.0, not stripped
```

I'll use Ghidra to decompile it.

I'll break the code of the main function and explain it.

### Variable declaration
```
  int iVar1;
  long in_FS_OFFSET;
  int local_40;
  uint local_3c;
  char local_38 [40];
  long local_10;
```

Just variable declarations.

### Reading input
```c
  puts("Welcome to baby rev challenge\nInput the password:\n");
  fgets(local_38,0x20,stdin);
  puts("Input the secret code now:\n");
  __isoc99_scanf(&DAT_0010211f,&local_40);
```
Reading a password and a pin code given by the user.

### Processing the input:
```c
  if (local_40 == 1337) {
    iVar1 = strcmp(local_38,"Sup3rS3cr3tP455W0rd\n");
    if (iVar1 == 0) {
      puts("Correct!\nHere is your flag\n");
      for (local_3c = 0; local_3c < 0x1b; local_3c = local_3c + 1) {
        putchar((int)(char)((char)local_3c + 0x69U ^
                           (byte)*(undefined4 *)(flag + (long)(int)local_3c * 4)));
      }
    }
    else {
      puts("Wrong password!");
    }
  }
  else {
    puts("Wrong code!");
  }
``` 

The pin code is verified. If it's the expected one the password is verified. If both conditions are respected the decrypted flag is printed.
As we can see the values for both the pin and the password we can run the binary and used them to get the flag.

But I'd like to get the flag without running the program. I can do this by following the for loop. 
```
for (local_3c = 0; local_3c < 0x1b; local_3c = local_3c + 1) {
        putchar((int)(char)((char)local_3c + 0x69U ^
                           (byte)*(undefined4 *)(flag + (long)(int)local_3c * 4)));
      }
```

This goes from 0 to 27. And prints the results of a bitwise XOR between i(iterator) + 105 (the u stands for unsigned) and the last byte at flag+i.

I'll make a simple python script to extract it.

```
hex_values=[0x2a,0x3e,0x2d,0x00,0x08,0x0f,0x1d,0x1e,0x0a,0x25,0x47,0x07,0x2a,0x47,0x23,0x27,0x2d,0x12,0x4f,0x28,0x22,0x36,0x4b,0xf2,0xe5,0xbd,0xfe,0x00]

rez=[]
for hv,i in zip(hex_values,range(0,len(hex_values))):
    rez+= chr(hv ^ (i+0x69))
print(''.join(rez))
```

This gives us the flag.